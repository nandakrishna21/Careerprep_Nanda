from __future__ import annotations

import html
import secrets
from datetime import date, timedelta

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.api.deps import OptionalUser
from app.core.config import settings
from app.core.security import CurrentUser, DbSession
from app.models import Job, MyJob, SavedJob, User
from app.schemas.misc import SaveJobRequest
from app.services.common import decode_short_code, job_brief, share_url
from app.services.job_taxonomy import (
    experience_options,
    locations_with_counts,
    roles_with_counts,
)
from app.services.job_sync import (
    MANUAL_REMOTE_COOLDOWN_SECONDS,
    REMOTE_SITES,
    last_remote_sync_at,
    remote_cooldown_remaining,
    run_scheduled_sync,
    sync_guard,
    sync_remote_jobs,
)

router = APIRouter(tags=["jobs"])

_PAGE_SIZE_MAX = 100


def _title_case(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").title()


def _days_ago(days: int) -> date:
    return date.today() - timedelta(days=max(1, min(365, days)))


def _paginate(page: int, page_size: int) -> tuple[int, int, int]:
    page = max(1, page)
    page_size = max(1, min(_PAGE_SIZE_MAX, page_size))
    return page, page_size, (page - 1) * page_size


def _saved_statuses(db: Session, user: User | None) -> dict[int, str]:
    if user is None:
        return {}
    rows = db.scalars(select(SavedJob).where(SavedJob.user_id == user.id)).all()
    return {row.job_id: row.status for row in rows}


def _job_item(job: Job, saved: dict[int, str]) -> dict:
    return {
        **job_brief(job),
        "is_saved": job.id in saved,
        "save_status": saved.get(job.id),
    }


def _get_job(db: Session, job_id: int) -> Job:
    job = db.get(Job, job_id)
    if job is None or not job.is_published:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.get("/saved")
def list_saved_jobs(
    user: CurrentUser, db: DbSession, page: int = 1, page_size: int = 20
) -> dict:
    page, page_size, offset = _paginate(page, page_size)
    stmt = (
        select(SavedJob)
        .where(SavedJob.user_id == user.id)
        .order_by(SavedJob.created_at.desc(), SavedJob.id.desc())
    )
    total = (
        db.scalar(select(func.count(SavedJob.id)).where(SavedJob.user_id == user.id)) or 0
    )
    rows = db.scalars(stmt.offset(offset).limit(page_size)).all()
    items = []
    for row in rows:
        job = db.get(Job, row.job_id)
        if job is None:
            continue
        items.append({**job_brief(job), "is_saved": True, "save_status": row.status})
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


def _applied_filters(
    stmt,
    type: str | None,
    category: str | None,
    role: str | None,
    location: str | None,
    experience: int | None,
    posted_within: int | None,
    q: str | None,
):
    if type:
        stmt = stmt.where(Job.type == type)
    if category:
        stmt = stmt.where(Job.category == category)
    if role:
        stmt = stmt.where(Job.role == role)
    if location:
        stmt = stmt.where(Job.city == location)
    if experience is not None:
        stmt = stmt.where(Job.exp_min <= experience)
    if posted_within:
        stmt = stmt.where(Job.posted_at >= _days_ago(posted_within))
    if q:
        needle = q.lower()
        stmt = stmt.where(
            or_(
                func.lower(Job.title).contains(needle),
                func.lower(Job.company).contains(needle),
                func.lower(Job.description).contains(needle),
            )
        )
    return stmt


@router.get("")
def list_jobs(
    db: DbSession,
    user: OptionalUser,
    type: str | None = None,
    category: str | None = None,
    role: str | None = None,
    location: str | None = None,
    experience: int | None = None,
    posted_within: int | None = None,
    sort: str | None = None,
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    page, page_size, offset = _paginate(page, page_size)
    stmt = select(Job).where(Job.is_published.is_(True))
    stmt = _applied_filters(stmt, type, category, role, location, experience, posted_within, q)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    if sort == "deadline":
        ordering = (
            Job.deadline.is_(None).asc(),
            Job.deadline.asc(),
            Job.created_at.desc(),
            Job.id.desc(),
        )
    else:
        ordering = (
            Job.posted_at.is_(None).asc(),
            Job.posted_at.desc(),
            Job.created_at.desc(),
            Job.id.desc(),
        )
    rows = db.scalars(stmt.order_by(*ordering).offset(offset).limit(page_size)).all()
    saved = _saved_statuses(db, user)
    return {
        "items": [_job_item(job, saved) for job in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


def _facet_counts(db: Session, type: str | None = None, category: str | None = None) -> dict:
    stmt = select(Job.role, Job.city, Job.category, Job.exp_min).where(Job.is_published.is_(True))
    if type:
        stmt = stmt.where(Job.type == type)
    if category:
        stmt = stmt.where(Job.category == category)
    rows = db.execute(stmt).all()
    return {
        "roles": roles_with_counts(role for role, _city, _category, _exp in rows),
        "locations": locations_with_counts(city for _role, city, _category, _exp in rows),
        "categories": _counted(category for _role, _city, category, _exp in rows),
        "experience": experience_options(exp for _role, _city, _category, exp in rows),
    }


def _counted(values) -> list[dict]:
    counts: dict[str, int] = {}
    for value in values:
        if value:
            counts[value] = counts.get(value, 0) + 1
    return [
        {"value": value, "label": _title_case(value), "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


@router.get("/categories")
def list_job_categories(db: DbSession) -> dict:
    """Distinct categories actually present, so filters match live data."""
    rows = db.execute(
        select(Job.type, Job.category)
        .where(Job.is_published.is_(True))
        .distinct()
        .order_by(Job.type, Job.category)
    ).all()
    grouped: dict[str, list[str]] = {}
    for job_type, category in rows:
        grouped.setdefault(job_type, []).append(category)
    return {"government": grouped.get("government", []), "it": grouped.get("it", [])}


@router.get("/facets")
def job_facets(db: DbSession) -> dict:
    """Role, location and category options derived from the live board."""
    return {
        "all": _facet_counts(db),
        "government": _facet_counts(db, "government"),
        "it": _facet_counts(db, "it"),
        "remote": _facet_counts(db, "it", "remote"),
    }


@router.get("/remote-sites")
def remote_job_sites() -> dict:
    """Every remote job website: crawled boards plus directory links."""
    return {"sites": REMOTE_SITES}


@router.get("/sync/status")
def job_sync_status(db: DbSession) -> dict:
    """Freshness snapshot for the Remote tab (public: no sensitive data)."""
    last_remote = last_remote_sync_at(db)
    last_any = db.scalar(select(func.max(Job.synced_at)).where(Job.external_id.is_not(None)))
    return {
        "last_remote_synced_at": last_remote.isoformat() if last_remote else None,
        "last_synced_at": last_any.isoformat() if last_any else None,
        "manual_cooldown_hours": MANUAL_REMOTE_COOLDOWN_SECONDS // 3600,
        "auto_sync": {"schedule": "daily", "time": "11:00 AM IST"},
    }


@router.post("/sync/remote")
def user_sync_remote_jobs(db: DbSession, user: CurrentUser) -> dict:
    """Let learners refresh remote listings; rate-limited so credits survive."""
    if not settings.apify_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Live sync is not configured yet."
        )
    remaining = remote_cooldown_remaining(db)
    if remaining > 0:
        hours = remaining / 3600
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Remote jobs were synced recently - try again in about {hours:.1f} hours "
                "(listings auto-sync daily at 11:00 AM IST)."
            ),
        )
    try:
        with sync_guard():
            return sync_remote_jobs(db)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


def _run_scheduled_sync() -> None:
    try:
        report = run_scheduled_sync()
    except Exception as exc:  # noqa: BLE001 - background failures belong in logs, not tracebacks
        print(f"[scheduled-sync] failed: {exc}")
    else:
        phases = ", ".join(
            f"{name}={'ok' if item.get('ok') else 'FAILED'}" for name, item in report.get("reports", {}).items()
        )
        print(f"[scheduled-sync] done: ok={report.get('ok')} ({phases})")


@router.post("/sync/scheduled")
def scheduled_job_sync(
    background_tasks: BackgroundTasks,
    token: str | None = None,
    x_cron_token: str | None = Header(default=None),
) -> dict:
    """cron-job.org pings this daily at 11 AM IST; the crawl runs in background
    so the ping returns instantly instead of timing out mid-crawl."""
    expected = settings.cron_secret
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Scheduled sync is not configured (CRON_SECRET missing).",
        )
    provided = x_cron_token or token or ""
    if not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid cron token.")
    try:
        with sync_guard():
            pass
    except RuntimeError:
        return {"started": False, "reason": "a sync is already running"}
    background_tasks.add_task(_run_scheduled_sync)
    return {"started": True}


@router.get("/share/{code}", response_class=HTMLResponse)
def share_job_page(code: str, db: DbSession) -> HTMLResponse:
    """Short share target (``/s/<code>`` via the frontend rewrite).

    Returns crawler-friendly Open Graph tags so Instagram/WhatsApp/Telegram
    render a rich preview, then redirects humans to the job page. Public.
    """
    job_id = decode_short_code(code)
    job = db.get(Job, job_id) if job_id else None
    if job is None or not job.is_published:
        return HTMLResponse(_share_html(None), status_code=404)
    return HTMLResponse(_share_html(job))


def _share_html(job) -> str:
    from app.core.config import settings

    home = (settings.frontend_url or "http://localhost:5173").rstrip("/")
    if job is None:
        title, description, target = (
            "Job not found",
            "This posting may have closed or been removed. Browse all openings on CareerPrep Hub.",
            f"{home}/jobs",
        )
    else:
        bits = [bit for bit in (job.company or "", job.location or "", job.salary or "") if bit]
        posted = job.posted_at.isoformat()[:10] if job.posted_at else ""
        if posted:
            bits.append(f"posted {posted}")
        title = f"{job.title} at {job.company}" if job.company else job.title
        description = " · ".join(bits) or (job.description or "")[:200]
        target = f"{home}/jobs/{job.id}"
    escape = html.escape
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{escape(title)} | CareerPrep Hub</title>
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description[:300])}">
<meta property="og:type" content="article">
<meta name="theme-color" content="#4f46e5">
<link rel="canonical" href="{escape(target)}">
<meta http-equiv="refresh" content="0;url={escape(target)}">
</head>
<body>
<p>Opening job&hellip; <a href="{escape(target)}">Continue</a></p>
<script>location.replace({target!r});</script>
</body>
</html>"""


@router.get("/{id}")
def get_job(id: int, db: DbSession, user: OptionalUser) -> dict:
    job = _get_job(db, id)
    saved = _saved_statuses(db, user)
    tracked_id = None
    if user is not None:
        tracked_id = db.scalar(
            select(MyJob.id).where(MyJob.user_id == user.id, MyJob.job_id == job.id)
        )
    return {
        **_job_item(job, saved),
        "is_tracked": tracked_id is not None,
        "my_job_id": tracked_id,
    }


@router.post("/{id}/save")
def save_job(id: int, user: CurrentUser, db: DbSession) -> dict:
    job = _get_job(db, id)
    row = db.scalar(
        select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == job.id)
    )
    if row is None:
        row = SavedJob(user_id=user.id, job_id=job.id, status="saved")
        db.add(row)
    db.commit()
    return {"job_id": job.id, "status": row.status, "is_saved": True}


@router.patch("/{id}/save")
def update_saved_job(
    id: int, payload: SaveJobRequest, user: CurrentUser, db: DbSession
) -> dict:
    job = _get_job(db, id)
    row = db.scalar(
        select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == job.id)
    )
    if row is None:
        row = SavedJob(user_id=user.id, job_id=job.id, status=payload.status)
        db.add(row)
    else:
        row.status = payload.status
    db.commit()
    return {"job_id": job.id, "status": row.status, "is_saved": True}


@router.delete("/{id}/save")
def unsave_job(id: int, user: CurrentUser, db: DbSession) -> dict:
    job = db.get(Job, id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    row = db.scalar(
        select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == job.id)
    )
    if row is not None:
        db.delete(row)
        db.commit()
    return {"job_id": job.id, "status": None, "is_saved": False}
