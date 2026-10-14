"""Daily current-affairs auto-update from free public sources (no API keys).

Why this exists: the seed ships 3 static 2023 editions, so ``/current-affairs``
goes stale. This module fetches fresh headlines every day from free,
key-less sources, builds a revision-friendly daily edition with MCQs,
short questions + revision notes, and upserts it (plus weekly/monthly
roll-ups) so the section is always current.

Free sources (public HTTP, no keys, exam-relevant):
* Inshorts public API — JSON per category (national, business, sports,
  world, politics, technology, science). Fast, stable, no auth.
* PIB releases RSS — official govt releases, ideal for UPSC/SSC.
* The Hindu national RSS — fallback editorial coverage.

Pattern mirrors ``job_sync``: concurrent fetch, per-source failure
isolation, upsert by slug, cooldown guard, cron-friendly scheduled entry.
"""
from __future__ import annotations

import html
import random
import re
import threading
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from typing import Any

import httpx
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import CurrentAffair, Question, Quiz

_UA = {"User-Agent": "CareerPrepHub/1.0 (+current-affairs-sync)"}
_TIMEOUT = httpx.Timeout(30.0)

INSHORTS_BASE = "https://inshortsapi.vercel.app/news"
INSHORTS_CATEGORIES = ("national", "business", "sports", "world", "politics", "technology", "science")

PIB_RSS = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"
HINDU_RSS = "https://www.thehindu.com/news/national/feeder/default.rss"

_WS = re.compile(r"\s+")
_TAG = re.compile(r"<[^>]+>")


def _clean(value: Any, limit: int = 500) -> str:
    if value is None:
        return ""
    text = _WS.sub(" ", html.unescape(_TAG.sub(" ", str(value)))).strip()
    return text[:limit]


def _client() -> httpx.Client:
    return httpx.Client(timeout=_TIMEOUT, follow_redirects=True, headers=_UA)


# ---------------------------------------------------------------------------
# fetchers (each returns list of {title, content, source, url, category})
# ---------------------------------------------------------------------------

def _fetch_inshorts_category(client: httpx.Client, category: str, limit: int = 8) -> list[dict]:
    resp = client.get(INSHORTS_BASE, params={"category": category})
    resp.raise_for_status()
    payload = resp.json()
    raw = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for entry in raw[:limit]:
        if not isinstance(entry, dict):
            continue
        title = _clean(entry.get("title"), 300)
        content = _clean(entry.get("content"), 800)
        if not title or not content:
            continue
        out.append(
            {
                "title": title,
                "content": content,
                "source": "Inshorts",
                "url": _clean(entry.get("readMoreUrl") or entry.get("url") or "", 1000),
                "category": category,
                "published": _clean(entry.get("date") or entry.get("time") or "", 120),
            }
        )
    return out


def _fetch_inshorts(client: httpx.Client) -> list[dict]:
    out: list[dict] = []
    with ThreadPoolExecutor(max_workers=min(6, len(INSHORTS_CATEGORIES))) as pool:
        futures = {pool.submit(_fetch_inshorts_category, client, cat): cat for cat in INSHORTS_CATEGORIES}
        for fut in as_completed(futures):
            try:
                out.extend(fut.result())
            except Exception:
                continue  # one dead category must not kill the sync
    return out


def _parse_rss_items(xml_text: str, limit: int = 12) -> list[dict]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    out: list[dict] = []
    for item in root.findall("./channel/item")[:limit]:
        def _tag(name: str) -> str:
            node = item.find(name)
            return (node.text or "") if node is not None else ""

        title = _clean(_tag("title"), 300)
        desc = _clean(_tag("description"), 800)
        link = _clean(_tag("link"), 1000)
        pub = _clean(_tag("pubDate"), 120)
        if not title:
            continue
        out.append({"title": title, "content": desc or title, "url": link, "published": pub})
    return out


def _fetch_rss(client: httpx.Client, url: str, source: str, category: str) -> list[dict]:
    resp = client.get(url)
    resp.raise_for_status()
    items = _parse_rss_items(resp.text)
    for it in items:
        it["source"] = source
        it["category"] = category
    return items


def fetch_all_headlines(client: httpx.Client | None = None) -> tuple[list[dict], dict[str, str]]:
    """Fetch from every free source concurrently. Returns (items, source_status)."""
    own_client = client is None
    client = client or _client()
    try:
        jobs = [
            ("inshorts", lambda: _fetch_inshorts(client)),
            ("pib", lambda: _fetch_rss(client, PIB_RSS, "PIB", "government")),
            ("the-hindu", lambda: _fetch_rss(client, HINDU_RSS, "The Hindu", "national")),
        ]
        items: list[dict] = []
        status: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
            futures = {pool.submit(fn): name for name, fn in jobs}
            for fut in as_completed(futures):
                name = futures[fut]
                try:
                    got = fut.result()
                    status[name] = f"ok ({len(got)})"
                    items.extend(got)
                except Exception as exc:  # noqa: BLE001 - per-source isolation
                    status[name] = f"failed: {type(exc).__name__}"
        # Dedupe by normalised title, keep first (Inshorts first = fastest).
        seen: set[str] = set()
        deduped: list[dict] = []
        for it in items:
            key = _WS.sub(" ", it["title"].lower()).strip()
            if not key or key in seen:
                continue
            seen.add(key)
            deduped.append(it)
        return deduped, status
    finally:
        if own_client:
            client.close()


# ---------------------------------------------------------------------------
# edition builders (pure — easy to unit test, no DB)
# ---------------------------------------------------------------------------

def _pretty_day(day: date) -> str:
    return day.strftime("%d %B %Y").lstrip("0")


def daily_slug(day: date) -> str:
    return f"daily-current-affairs-{day.isoformat()}"


def build_mcqs_fallback(items: list[dict], day: date, count: int = 5) -> list[dict]:
    """Rule-based MCQs when Gemini is unavailable.

    Each Q asks which description matches a headline; distractors are
    descriptions of *other* headlines, shuffled deterministically so the
    correct answer is not always option A.
    """
    pool = [it for it in items if it.get("title") and it.get("content")][: max(count * 3, 12)]
    if len(pool) < 4:
        return []
    mcqs: list[dict] = []
    for i in range(min(count, len(pool))):
        correct = pool[i]
        distractors = [p for j, p in enumerate(pool) if j != i][:8]
        # deterministic shuffle per edition+index
        rng = random.Random(f"{day.isoformat()}-{i}-{correct['title'][:40]}")
        options = [correct["content"][:220]] + [d["content"][:220] for d in distractors[:3]]
        # ensure 4 distinct options
        uniq: list[str] = []
        for opt in options:
            if opt and opt not in uniq:
                uniq.append(opt)
        while len(uniq) < 4:
            uniq.append(f"None of the above (round-up {day.isoformat()})")
        order = list(range(4))
        rng.shuffle(order)
        # correct was at index 0 before shuffle; find where it landed
        shuffled = [""] * 4
        for new_pos, old_pos in enumerate(order):
            shuffled[new_pos] = uniq[old_pos]
        correct_index = order.index(0)
        q_title = correct["title"]
        if len(q_title) > 160:
            q_title = q_title[:157] + "..."
        mcqs.append(
            {
                "question": f'On {_pretty_day(day)}, "{q_title}" was in the news. Which description matches?',
                "options": shuffled,
                "correct_index": correct_index,
                "explanation": f"{correct['title']} — {correct['content'][:220]} (Source: {correct.get('source', 'round-up')}).",
            }
        )
    return mcqs


def build_daily_edition(items: list[dict], day: date) -> dict:
    top = items[:14]
    if top:
        summary_bits = [t["title"] for t in top[:3]]
        summary = "; ".join(summary_bits)
        if len(summary) > 280:
            summary = summary[:277] + "..."
    else:
        summary = f"Daily round-up for {_pretty_day(day)}."
    lines = [
        f"Daily current-affairs round-up for {_pretty_day(day)} — key national, "
        "economy, science-tech, sports and world developments relevant for SSC, "
        "Banking, Railway and UPSC preparation.",
        "",
    ]
    for idx, it in enumerate(top, start=1):
        cat = (it.get("category") or "general").title()
        lines.append(f"{idx}. [{cat}] {it['title']}")
        lines.append(f"   {it['content']}")
        if it.get("source"):
            src = it["source"] + (f" ({it['url']})" if it.get("url") else "")
            lines.append(f"   Source: {src}")
        lines.append("")
    if not top:
        lines.append("No fresh items could be fetched today — showing the latest available edition. Please sync again later.")
        lines.append("")
    content = "\n".join(lines).strip()
    mcqs = build_mcqs_fallback(top, day)
    short_qs = [f"Discuss the significance of: {it['title']}" for it in top[:3]]
    revision = "\n".join(f"• {it['title']} — {it['content'][:140]}" for it in top[:10])
    sources = [
        {"label": it.get("source") or "Source", "url": it.get("url") or "", "title": it["title"][:120]}
        for it in top[:10]
    ]
    return {
        "slug": daily_slug(day),
        "title": f"Daily Current Affairs — {_pretty_day(day)}",
        "period": "daily",
        "date": day,
        "summary": summary,
        "content": content,
        "ai_content": {
            "mcqs": mcqs,
            "short_questions": short_qs,
            "revision_notes": revision or f"Round-up for {_pretty_day(day)}.",
            "sources": sources,
            "generated_from": "free-public-feeds",
        },
    }


def _try_gemini_upgrade(spec: dict) -> None:
    """Best-effort: replace fallback MCQs with Gemini ones when configured."""
    if not settings.gemini_api_key:
        return
    try:
        from app.services import gemini as _gemini

        articles = "\n".join(
            f"- {it['title']}: {it['content'][:300]}"
            for it in spec.pop("_raw_items", [])[:12]
        ) or spec["content"][:4000]
        prompt = (
            f"Prepare current affairs content dated {spec['date']} for competitive exam aspirants.\n"
            f"Source notes/articles:\n\"\"\"\n{articles}\n\"\"\"\n"
            "Respond with strict JSON: {\"mcqs\": [{\"question\": <string>, \"options\": [<4 strings>], "
            "\"correct_index\": <0-3>, \"explanation\": <string>}], \"short_questions\": [<strings>], "
            "\"revision_notes\": <string>}. Include 5 MCQs."
        )
        generated: Any = _gemini.generate_json(
            prompt,
            system="You are an editor preparing daily current affairs for competitive exam aspirants. You always answer with strict, valid JSON only.",
            temperature=0.7,
        )
        if isinstance(generated, dict):
            ai = spec["ai_content"]
            if isinstance(generated.get("mcqs"), list) and generated["mcqs"]:
                ai["mcqs"] = generated["mcqs"][:5]
            if isinstance(generated.get("short_questions"), list) and generated["short_questions"]:
                ai["short_questions"] = generated["short_questions"][:3]
            if isinstance(generated.get("revision_notes"), str) and generated["revision_notes"]:
                ai["revision_notes"] = generated["revision_notes"]
            ai["generated_from"] = "gemini+free-feeds"
    except Exception:
        pass  # fallback content already in place


# ---------------------------------------------------------------------------
# DB upsert + quiz link
# ---------------------------------------------------------------------------

def _ensure_quiz_for_affair(db: Session, row: CurrentAffair) -> int | None:
    from app.services.common import unique_slug as _unique_slug

    mcqs = (row.ai_content or {}).get("mcqs") or []
    if not isinstance(mcqs, list) or not mcqs:
        return None
    slug = f"ca-{row.slug}"
    quiz = db.scalar(select(Quiz).where(Quiz.slug == slug))
    questions_payload: list[dict] = []
    for index, mcq in enumerate(mcqs):
        if not isinstance(mcq, dict) or not mcq.get("question") or not mcq.get("options"):
            continue
        try:
            correct = int(mcq.get("correct_index", 0))
        except (TypeError, ValueError):
            continue
        options = [str(o) for o in mcq["options"]][:4]
        if len(options) < 2:
            continue
        questions_payload.append(
            {
                "question_text": str(mcq["question"]),
                "options": options,
                "correct_index": max(0, min(correct, len(options) - 1)),
                "explanation": str(mcq.get("explanation") or ""),
                "difficulty": "intermediate",
                "order": index,
            }
        )
    if not questions_payload:
        return None
    if quiz is None:
        quiz = Quiz(
            title=f"Quiz — {row.title}"[:255],
            slug=_unique_slug(db, Quiz, slug),
            quiz_type="current_affair",
            current_affair_id=row.id,
            difficulty="intermediate",
            duration_minutes=max(5, len(questions_payload) * 2),
            negative_marks=0,
            total_questions=len(questions_payload),
            is_published=True,
            meta={"period": row.period},
        )
        db.add(quiz)
        db.flush()
    else:
        quiz.current_affair_id = row.id
        quiz.total_questions = len(questions_payload)
        quiz.is_published = True
        # Replace stale questions so the quiz always matches today's MCQs.
        db.query(Question).filter(Question.quiz_id == quiz.id).delete()
        db.flush()
    for item in questions_payload:
        db.add(
            Question(
                quiz_id=quiz.id,
                question_text=item["question_text"],
                options=list(item["options"]),
                correct_index=int(item["correct_index"]),
                explanation=item["explanation"],
                difficulty=item["difficulty"],
                order=item["order"],
                tags=["Current Affairs"],
            )
        )
    db.flush()
    ai = dict(row.ai_content or {})
    ai["quiz_id"] = quiz.id
    row.ai_content = ai
    return quiz.id


def upsert_edition(db: Session, spec: dict) -> tuple[CurrentAffair, bool]:
    """Insert or refresh an edition by slug. Returns (row, created)."""
    row = db.scalar(select(CurrentAffair).where(CurrentAffair.slug == spec["slug"]))
    if row is None:
        row = CurrentAffair(
            title=spec["title"],
            slug=spec["slug"],
            period=spec["period"],
            date=spec["date"],
            summary=spec.get("summary", ""),
            content=spec.get("content", ""),
            ai_content=dict(spec.get("ai_content", {})),
            is_published=True,
        )
        db.add(row)
        db.flush()
        created = True
    else:
        row.title = spec["title"]
        row.period = spec["period"]
        row.date = spec["date"]
        row.summary = spec.get("summary", "")
        row.content = spec.get("content", "")
        # Preserve an existing quiz_id link across refreshes.
        old_quiz = (row.ai_content or {}).get("quiz_id")
        row.ai_content = dict(spec.get("ai_content", {}))
        if old_quiz and not (row.ai_content or {}).get("quiz_id"):
            ai = dict(row.ai_content or {})
            ai["quiz_id"] = old_quiz
            row.ai_content = ai
        row.is_published = True
        db.flush()
        created = False
    _ensure_quiz_for_affair(db, row)
    return row, created


# ---------------------------------------------------------------------------
# sync orchestration + cooldown guard
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_LAST_OK: float = 0.0
_LAST_REPORT: dict = {}
_COOLDOWN_SECONDS = 60.0


def cooldown_remaining() -> float:
    with _lock:
        remaining = _COOLDOWN_SECONDS - (time.monotonic() - _LAST_OK)
        return max(0.0, remaining)


def last_report() -> dict:
    with _lock:
        return dict(_LAST_REPORT)


def sync_daily(db: Session, day: date | None = None, preloaded: list[dict] | None = None) -> dict:
    """Fetch free feeds and upsert today's daily edition (+ weekly/monthly roll-ups).

    Never raises on source failure — worst case it upserts a stub edition so
    the section still shows today's date instead of 2023 samples.
    """
    day = day or date.today()
    items: list[dict] = list(preloaded) if preloaded is not None else []
    source_status: dict[str, str] = {"mode": "preloaded" if preloaded is not None else "live"}
    if preloaded is None:
        try:
            items, source_status = fetch_all_headlines()
        except Exception as exc:  # noqa: BLE001 - offline dev must still work
            source_status = {"error": f"{type(exc).__name__}: {exc}"}
            items = []
    spec = build_daily_edition(items, day)
    spec["_raw_items"] = items
    _try_gemini_upgrade(spec)
    spec.pop("_raw_items", None)

    row, created = upsert_edition(db, spec)

    # Weekly roll-up (Monday) + monthly roll-up (1st) keep those tabs fresh too.
    extras: list[str] = []
    if day.weekday() == 0:
        week_start = day - timedelta(days=6)
        extras.append(_ensure_weekly(db, week_start, day))
    if day.day == 1:
        extras.append(_ensure_monthly(db, day))

    db.commit()
    report = {
        "ok": True,
        "date": day.isoformat(),
        "slug": row.slug,
        "created": created,
        "items_fetched": len(items),
        "mcqs": len((row.ai_content or {}).get("mcqs") or []),
        "sources": source_status,
        "rollups": [e for e in extras if e],
    }
    with _lock:
        global _LAST_OK, _LAST_REPORT
        _LAST_OK = time.monotonic()
        _LAST_REPORT = report
    return report


def _ensure_weekly(db: Session, week_start: date, week_end: date) -> str | None:
    slug = f"weekly-current-affairs-{week_end.isoformat()}"
    if db.scalar(select(CurrentAffair).where(CurrentAffair.slug == slug)) is not None:
        return None
    dailies = db.scalars(
        select(CurrentAffair)
        .where(CurrentAffair.period == "daily", CurrentAffair.date >= week_start, CurrentAffair.date <= week_end)
        .order_by(CurrentAffair.date)
    ).all()
    if dailies:
        highlights = "\n".join(f"• {d.title} — {d.summary}" for d in dailies[:7])
        content = (
            f"Weekly round-up {week_start.isoformat()} to {week_end.isoformat()} — "
            f"{len(dailies)} daily editions.\n\n{highlights}"
        )
        mcqs: list[dict] = []
        for d in dailies[:5]:
            for m in ((d.ai_content or {}).get("mcqs") or [])[:1]:
                if isinstance(m, dict) and m.get("question"):
                    mcqs.append(m)
                if len(mcqs) >= 5:
                    break
    else:
        content = f"Weekly round-up ending {week_end.isoformat()}."
        mcqs = []
    spec = {
        "slug": slug,
        "title": f"Weekly Current Affairs — {week_start.strftime('%d %b')} to {week_end.strftime('%d %b %Y')}",
        "period": "weekly",
        "date": week_end,
        "summary": f"Top developments {week_start.isoformat()} to {week_end.isoformat()}.",
        "content": content,
        "ai_content": {
            "mcqs": mcqs,
            "short_questions": [f"Summarise the key events of the week ending {week_end.isoformat()}."],
            "revision_notes": content[:1500],
            "sources": [],
            "generated_from": "weekly-rollup",
        },
    }
    row, created = upsert_edition(db, spec)
    return row.slug if created else None


def _ensure_monthly(db: Session, day: date) -> str | None:
    month_start = day.replace(day=1)
    slug = f"monthly-current-affairs-{day.strftime('%Y-%m')}"
    if db.scalar(select(CurrentAffair).where(CurrentAffair.slug == slug)) is not None:
        return None
    dailies = db.scalars(
        select(CurrentAffair)
        .where(CurrentAffair.period == "daily", CurrentAffair.date >= month_start, CurrentAffair.date <= day)
        .order_by(CurrentAffair.date)
    ).all()
    content = (
        f"Monthly compilation for {day.strftime('%B %Y')} — {len(dailies)} daily editions. "
        + "\n".join(f"• {d.title}" for d in dailies[:15])
    )
    spec = {
        "slug": slug,
        "title": f"Monthly Current Affairs — {day.strftime('%B %Y')}",
        "period": "monthly",
        "date": day,
        "summary": f"Month's essential revisions for {day.strftime('%B %Y')}.",
        "content": content,
        "ai_content": {
            "mcqs": [],
            "short_questions": [f"List the five most important events of {day.strftime('%B %Y')} and why they matter."],
            "revision_notes": content[:1500],
            "sources": [],
            "generated_from": "monthly-rollup",
        },
    }
    row, created = upsert_edition(db, spec)
    return row.slug if created else None


def sync_status(db: Session) -> dict:
    today = date.today()
    today_row = db.scalar(select(CurrentAffair).where(CurrentAffair.slug == daily_slug(today)))
    latest = db.scalar(select(func.max(CurrentAffair.date)))
    counts = {
        period: int(db.scalar(select(func.count(CurrentAffair.id)).where(CurrentAffair.period == period)) or 0)
        for period in ("daily", "weekly", "monthly")
    }
    return {
        "today": today.isoformat(),
        "today_slug": daily_slug(today),
        "today_exists": today_row is not None,
        "latest_date": latest.isoformat() if latest else None,
        "counts": counts,
        "cooldown_remaining_seconds": round(cooldown_remaining(), 1),
        "last_report": last_report(),
    }
