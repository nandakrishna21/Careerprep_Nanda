"""Daily current-affairs auto-update from free public feeds (no network in tests)."""
from datetime import date

import pytest


def _sample_items(n: int = 8) -> list[dict]:
    cats = ["national", "business", "sports", "world", "politics", "science"]
    return [
        {
            "title": f"Sample headline {i + 1} on infra push",
            "content": f"Detailed description of sample event {i + 1} with exam-relevant facts and figures.",
            "source": "Inshorts",
            "url": f"https://example.com/{i + 1}",
            "category": cats[i % len(cats)],
        }
        for i in range(n)
    ]


def test_build_daily_edition_has_mcqs_sources():
    from app.services import current_affairs_sync as ca

    day = date(2026, 10, 14)
    spec = ca.build_daily_edition(_sample_items(), day)
    assert spec["slug"] == "daily-current-affairs-2026-10-14"
    assert spec["period"] == "daily"
    assert "14 October 2026" in spec["title"]
    assert len(spec["ai_content"]["mcqs"]) == 5
    for mcq in spec["ai_content"]["mcqs"]:
        assert len(mcq["options"]) == 4
        assert 0 <= mcq["correct_index"] < 4
        assert mcq["explanation"]
    assert len(spec["ai_content"]["short_questions"]) == 3
    assert spec["ai_content"]["revision_notes"]
    assert len(spec["ai_content"]["sources"]) == 8
    # deterministic: same input -> same correct_index layout
    again = ca.build_daily_edition(_sample_items(), day)
    assert [m["correct_index"] for m in again["ai_content"]["mcqs"]] == [
        m["correct_index"] for m in spec["ai_content"]["mcqs"]
    ]


def test_build_daily_edition_empty_offline():
    from app.services import current_affairs_sync as ca

    day = date(2026, 10, 14)
    spec = ca.build_daily_edition([], day)
    assert spec["slug"] == "daily-current-affairs-2026-10-14"
    assert spec["ai_content"]["mcqs"] == []


def test_sync_daily_preloaded_upserts_and_links_quiz(db):
    from sqlalchemy import select

    from app.models import CurrentAffair, Quiz
    from app.services import current_affairs_sync as ca

    day = date(2026, 10, 14)
    report = ca.sync_daily(db, day=day, preloaded=_sample_items())
    assert report["ok"] is True
    assert report["slug"] == "daily-current-affairs-2026-10-14"
    assert report["mcqs"] == 5

    row = db.scalar(select(CurrentAffair).where(CurrentAffair.slug == report["slug"]))
    assert row is not None
    assert row.is_published is True
    assert (row.ai_content or {}).get("quiz_id")

    quiz = db.scalar(select(Quiz).where(Quiz.slug == f"ca-{report['slug']}"))
    assert quiz is not None
    assert quiz.quiz_type == "current_affair"

    # idempotent re-sync keeps one row + one quiz
    report2 = ca.sync_daily(db, day=day, preloaded=_sample_items())
    assert report2["created"] is False
    rows = db.scalars(select(CurrentAffair).where(CurrentAffair.slug == report["slug"])).all()
    assert len(rows) == 1


def test_sync_status_reports_today(db):
    from app.services import current_affairs_sync as ca

    day = date(2026, 10, 14)
    ca.sync_daily(db, day=day, preloaded=_sample_items())
    status = ca.sync_status(db)
    assert status["today"] == date.today().isoformat()
    assert status["counts"]["daily"] >= 1


def test_rss_parser_tolerates_feeds():
    from app.services import current_affairs_sync as ca

    xml = """<rss><channel>
      <item><title>PIB release on railways</title><link>https://pib.gov.in/x</link><pubDate>Mon, 13 Oct 2026</pubDate><description>New trains announced.</description></item>
      <item><title></title><link>https://x</link><description>skip me</description></item>
    </channel></rss>"""
    items = ca._parse_rss_items(xml)
    assert len(items) == 1
    assert items[0]["title"] == "PIB release on railways"


def test_scheduled_ca_sync_requires_token(client, monkeypatch):
    from app.core.config import settings
    from app.services import current_affairs_sync as ca

    monkeypatch.setattr(settings, "cron_secret", "s3cr3t")
    # Avoid real network in the background task.
    monkeypatch.setattr(ca, "fetch_all_headlines", lambda client=None: (_sample_items(), {"mock": "ok"}))
    monkeypatch.setattr(settings, "gemini_api_key", "")
    res = client.post("/api/current-affairs/sync/scheduled", params={"token": "wrong"})
    assert res.status_code == 403
    # correct token starts background job instantly (runs with mocked feeds).
    res = client.post("/api/current-affairs/sync/scheduled", params={"token": "s3cr3t"})
    assert res.status_code == 200
    assert res.json().get("started") is True
