from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.api.deps import OptionalUser
from app.core.security import CurrentUser, DbSession
from app.models import Job, SavedJob, User
from app.schemas.misc import SaveJobRequest
from app.services.common import job_brief
from app.services.job_taxonomy import locations_with_counts, roles_with_counts

router = APIRouter(tags=["jobs"])

_PAGE_SIZE_MAX = 100


def _title_case(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").title()


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
    q: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    page, page_size, offset = _paginate(page, page_size)
    stmt = select(Job).where(Job.is_published.is_(True))
    stmt = _applied_filters(stmt, type, category, role, location, q)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(
        stmt.order_by(
            Job.posted_at.is_(None).asc(),
            Job.posted_at.desc(),
            Job.created_at.desc(),
            Job.id.desc(),
        )
        .offset(offset)
        .limit(page_size)
    ).all()
    saved = _saved_statuses(db, user)
    return {
        "items": [_job_item(job, saved) for job in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


def _facet_counts(db: Session, type: str | None = None) -> dict:
    stmt = select(Job.role, Job.city, Job.category).where(Job.is_published.is_(True))
    if type:
        stmt = stmt.where(Job.type == type)
    rows = db.execute(stmt).all()
    return {
        "roles": roles_with_counts(role for role, _city, _category in rows),
        "locations": locations_with_counts(city for _role, city, _category in rows),
        "categories": _counted(category for _role, _city, category in rows),
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
    }


@router.get("/{id}")
def get_job(id: int, db: DbSession, user: OptionalUser) -> dict:
    job = _get_job(db, id)
    saved = _saved_statuses(db, user)
    return _job_item(job, saved)


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
