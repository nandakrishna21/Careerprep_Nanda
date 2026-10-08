from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, or_, select

from app.core.security import AdminUser, DbSession
from app.models import (
    Course,
    CurrentAffair,
    Job,
    Profile,
    Quiz,
    QuizAttempt,
    User,
)
from app.schemas.admin import (
    AdminUserUpdate,
    CurrentAffairCreate,
    CurrentAffairUpdate,
    JobAdminCreate,
    JobAdminUpdate,
)
from app.services.common import job_brief, naive_utc_now, profile_brief, unique_slug, user_brief
from app.services.job_sync import sync_jobs, sync_remote_jobs, sync_status

router = APIRouter(tags=["admin"])

_WINDOW_DAYS = 14


def _page_params(page: int, page_size: int) -> tuple[int, int, int]:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    return page, page_size, (page - 1) * page_size


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def _as_utc_naive(value: datetime) -> datetime:
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def _affair_out(row: CurrentAffair) -> dict:
    return {
        "id": row.id,
        "title": row.title,
        "slug": row.slug,
        "period": row.period,
        "date": row.date,
        "summary": row.summary or "",
        "content": row.content or "",
        "ai_content": row.ai_content or {},
        "is_published": row.is_published,
        "created_at": row.created_at,
    }


@router.get("/current-affairs")
def admin_list_current_affairs(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, period: str | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(CurrentAffair)
    if period:
        stmt = stmt.where(CurrentAffair.period == period)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(
        stmt.order_by(CurrentAffair.date.desc(), CurrentAffair.id.desc()).offset(offset).limit(page_size)
    ).all()
    return {
        "items": [_affair_out(row) for row in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


@router.post("/current-affairs")
def admin_create_current_affair(payload: CurrentAffairCreate, admin: AdminUser, db: DbSession) -> dict:
    slug = unique_slug(db, CurrentAffair, payload.slug or payload.title)
    row = CurrentAffair(**payload.model_dump(exclude={"slug"}), slug=slug)
    db.add(row)
    db.commit()
    db.refresh(row)
    return _affair_out(row)


@router.put("/current-affairs/{id}")
def admin_update_current_affair(
    id: int, payload: CurrentAffairUpdate, admin: AdminUser, db: DbSession
) -> dict:
    row = db.get(CurrentAffair, id)
    if row is None:
        raise _not_found("Current affair not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("slug"):
        data["slug"] = unique_slug(db, CurrentAffair, data["slug"], exclude_id=row.id)
    for field, value in data.items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return _affair_out(row)


@router.delete("/current-affairs/{id}")
def admin_delete_current_affair(id: int, admin: AdminUser, db: DbSession) -> dict:
    row = db.get(CurrentAffair, id)
    if row is None:
        raise _not_found("Current affair not found")
    db.delete(row)
    db.commit()
    return {"message": "Current affair deleted"}


@router.get("/jobs")
def admin_list_jobs(
    admin: AdminUser,
    db: DbSession,
    page: int = 1,
    page_size: int = 20,
    type: str | None = None,
    q: str | None = None,
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Job)
    if type:
        stmt = stmt.where(Job.type == type)
    if q:
        needle = q.lower()
        stmt = stmt.where(
            or_(func.lower(Job.title).contains(needle), func.lower(Job.company).contains(needle))
        )
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Job.id.desc()).offset(offset).limit(page_size)).all()
    return {
        "items": [{**job_brief(row), "is_published": row.is_published} for row in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


@router.post("/jobs")
def admin_create_job(payload: JobAdminCreate, admin: AdminUser, db: DbSession) -> dict:
    job = Job(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return {**job_brief(job), "is_published": job.is_published}


@router.put("/jobs/{id}")
def admin_update_job(id: int, payload: JobAdminUpdate, admin: AdminUser, db: DbSession) -> dict:
    job = db.get(Job, id)
    if job is None:
        raise _not_found("Job not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return {**job_brief(job), "is_published": job.is_published}


@router.delete("/jobs/{id}")
def admin_delete_job(id: int, admin: AdminUser, db: DbSession) -> dict:
    job = db.get(Job, id)
    if job is None:
        raise _not_found("Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}


@router.get("/jobs/sync/status")
def admin_jobs_sync_status(admin: AdminUser, db: DbSession) -> dict:
    return sync_status(db)


@router.post("/jobs/sync")
def admin_sync_jobs(
    admin: AdminUser, db: DbSession, track: str | None = None
) -> dict:
    """Run the live job crawl. Blocks until every source has finished or failed."""
    tracks: list[str] | None = None
    if track:
        tracks = [part.strip() for part in track.split(",") if part.strip()]
        unknown = sorted(set(tracks) - {"government", "it", "remote"})
        if unknown:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown track(s): {', '.join(unknown)}",
            )
        if "remote" in tracks and len(tracks) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Run the 'remote' track on its own: ?track=remote.",
            )
    try:
        if tracks == ["remote"]:
            return sync_remote_jobs(db)
        return sync_jobs(db, tracks)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/users")
def admin_list_users(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, q: str | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(User)
    if q:
        needle = q.lower()
        stmt = stmt.where(
            or_(func.lower(User.email).contains(needle), func.lower(User.full_name).contains(needle))
        )
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(User.created_at.desc(), User.id.desc()).offset(offset).limit(page_size)).all()
    profile_map = {}
    if rows:
        profiles = db.scalars(
            select(Profile).where(Profile.user_id.in_([row.id for row in rows]))
        ).all()
        profile_map = {profile.user_id: profile for profile in profiles}
    items = []
    for row in rows:
        profile = profile_map.get(row.id)
        items.append(
            {
                **user_brief(row),
                "is_active": row.is_active,
                "created_at": row.created_at,
                "profile": {
                    "xp": profile.xp if profile else 0,
                    "level": profile.level if profile else 1,
                    "streak_days": profile.streak_days if profile else 0,
                    "headline": profile.headline if profile else "",
                    "avatar_color": profile.avatar_color if profile else "indigo",
                },
            }
        )
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


@router.patch("/users/{id}")
def admin_update_user(id: int, payload: AdminUserUpdate, admin: AdminUser, db: DbSession) -> dict:
    target = db.get(User, id)
    if target is None:
        raise _not_found("User not found")
    data = payload.model_dump(exclude_unset=True)
    if target.id == admin.id:
        if "role" in data and data["role"] != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot remove your own admin role",
            )
        if data.get("is_active") is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot deactivate your own account",
            )
    for field, value in data.items():
        setattr(target, field, value)
    db.commit()
    db.refresh(target)
    profile = db.scalar(select(Profile).where(Profile.user_id == target.id))
    return {**user_brief(target), "is_active": target.is_active, "profile": profile_brief(profile)}


@router.delete("/users/{id}")
def admin_delete_user(id: int, admin: AdminUser, db: DbSession) -> dict:
    target = db.get(User, id)
    if target is None:
        raise _not_found("User not found")
    if target.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account"
        )
    db.delete(target)
    db.commit()
    return {"message": "User deleted"}


@router.get("/analytics")
def admin_analytics(admin: AdminUser, db: DbSession) -> dict:
    today = datetime.now(timezone.utc).date()
    window_start = today - timedelta(days=_WINDOW_DAYS - 1)
    window_datetime = datetime.combine(window_start, datetime.min.time())

    users_total = db.scalar(select(func.count(User.id))) or 0
    quizzes_total = db.scalar(select(func.count(Quiz.id))) or 0
    attempts_total = db.scalar(select(func.count(QuizAttempt.id))) or 0
    jobs_total = db.scalar(select(func.count(Job.id))) or 0
    courses_total = db.scalar(select(func.count(Course.id))) or 0

    users = db.scalars(select(User).where(User.created_at >= window_datetime)).all()
    signup_counts: dict[str, int] = {}
    for user in users:
        day = _as_utc_naive(user.created_at).date()
        if day >= window_start:
            signup_counts[day.isoformat()] = signup_counts.get(day.isoformat(), 0) + 1

    new_7d_cutoff = datetime.combine(today - timedelta(days=6), datetime.min.time())
    users_new_7d = (
        db.scalar(select(func.count(User.id)).where(User.created_at >= new_7d_cutoff)) or 0
    )

    attempts = db.scalars(
        select(QuizAttempt).where(QuizAttempt.created_at >= window_datetime)
    ).all()
    accuracy_by_day: dict[str, list[float]] = {}
    for attempt in attempts:
        day = _as_utc_naive(attempt.created_at).date()
        if day < window_start:
            continue
        accuracy_by_day.setdefault(day.isoformat(), []).append(float(attempt.accuracy or 0))

    signup_rows = []
    score_rows = []
    for offset in range(_WINDOW_DAYS):
        day = (window_start + timedelta(days=offset)).isoformat()
        signup_rows.append({"date": day, "count": signup_counts.get(day, 0)})
        values = accuracy_by_day.get(day, [])
        score_rows.append(
            {"date": day, "avg": round(sum(values) / len(values), 2) if values else 0.0}
        )

    quiz_counts = dict(
        db.execute(
            select(QuizAttempt.quiz_id, func.count(QuizAttempt.id)).group_by(QuizAttempt.quiz_id)
        ).all()
    )
    top_quizzes = []
    if quiz_counts:
        quiz_rows = db.scalars(
            select(Quiz).where(Quiz.id.in_(list(quiz_counts.keys()))).order_by(Quiz.id)
        ).all()
        ranked = sorted(
            ({"title": quiz.title, "attempts": int(quiz_counts.get(quiz.id, 0))} for quiz in quiz_rows),
            key=lambda item: -item["attempts"],
        )
        top_quizzes = ranked[:10]

    return {
        "users_total": int(users_total),
        "users_new_7d": int(users_new_7d),
        "quizzes_total": int(quizzes_total),
        "attempts_total": int(attempts_total),
        "jobs_total": int(jobs_total),
        "courses_total": int(courses_total),
        "top_quizzes": top_quizzes,
        "signups_by_day": signup_rows,
        "avg_score_by_day": score_rows,
    }
