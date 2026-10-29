from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import CurrentUser, DbSession
from app.models import Job, MyJob
from app.schemas.myjobs import MyJobCreate, MyJobUpdate
from app.seed import myjobs_templates

router = APIRouter(tags=["my-jobs"])

_VALID_STATUSES = {"wishlist", "applied", "preparing", "exam", "interview", "selected", "rejected"}


def _out(row: MyJob, job: Job | None = None) -> dict:
    return {
        "id": row.id,
        "job_id": row.job_id,
        "template_key": row.template_key,
        "title": row.title,
        "organization": row.organization or "",
        "role_name": row.role_name or "",
        "status": row.status,
        "applied_date": row.applied_date,
        "exam_date": row.exam_date,
        "deadline": row.deadline,
        "notification_link": row.notification_link or "",
        "apply_link": row.apply_link or "",
        "syllabus": list(row.syllabus or []),
        "exam_pattern": list(row.exam_pattern or []),
        "strategy": row.strategy or "",
        "preparation_plan": list(row.preparation_plan or []),
        "resources": list(getattr(row, "resources", None) or []),
        "notes": row.notes or "",
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "job": (
            {"id": job.id, "title": job.title, "company": job.company} if job is not None else None
        ),
    }


def _get_owned(db: DbSession, user, my_job_id: int) -> MyJob:
    row = db.scalar(select(MyJob).where(MyJob.id == my_job_id, MyJob.user_id == user.id))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="My job not found")
    return row


@router.get("/templates")
def list_my_job_templates(user: CurrentUser) -> dict:
    """Starter pack: the applied roles with syllabus + strategy (UIICL AO, EPFO APFC)."""
    items = [
        {
            "template_key": t["template_key"],
            "title": t["title"],
            "organization": t["organization"],
            "role_name": t["role_name"],
            "sections": len(t.get("syllabus", [])),
            "phases": len(t.get("preparation_plan", [])),
            "resource_groups": len(t.get("resources", [])),
        }
        for t in myjobs_templates.TEMPLATES
    ]
    return {"items": items}


@router.get("/templates/{key}")
def get_my_job_template(key: str, user: CurrentUser) -> dict:
    tpl = myjobs_templates.get_template(key)
    if tpl is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return tpl


@router.get("")
def list_my_jobs(user: CurrentUser, db: DbSession, status: str | None = None) -> dict:
    stmt = select(MyJob).where(MyJob.user_id == user.id)
    if status:
        if status not in _VALID_STATUSES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
        stmt = stmt.where(MyJob.status == status)
    stmt = stmt.order_by(MyJob.updated_at.desc(), MyJob.id.desc())
    rows = db.scalars(stmt).all()
    job_map: dict[int, Job] = {}
    ids = [r.job_id for r in rows if r.job_id]
    if ids:
        for job in db.scalars(select(Job).where(Job.id.in_(ids))).all():
            job_map[job.id] = job
    total = db.scalar(select(func.count(MyJob.id)).where(MyJob.user_id == user.id)) or 0
    return {"items": [_out(r, job_map.get(r.job_id) if r.job_id else None) for r in rows], "total": int(total)}


@router.get("/{my_job_id}")
def get_my_job(my_job_id: int, user: CurrentUser, db: DbSession) -> dict:
    row = _get_owned(db, user, my_job_id)
    job = db.get(Job, row.job_id) if row.job_id else None
    return _out(row, job)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_my_job(payload: MyJobCreate, user: CurrentUser, db: DbSession) -> dict:
    if payload.status not in _VALID_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    job = None
    if payload.job_id is not None:
        job = db.get(Job, payload.job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        # "Track application" is idempotent: clicking twice must not create a
        # second row for the same job.
        existing = db.scalar(
            select(MyJob).where(MyJob.user_id == user.id, MyJob.job_id == job.id)
        )
        if existing is not None:
            return _out(existing, job)
    row = MyJob(
        user_id=user.id,
        job_id=payload.job_id,
        template_key=payload.template_key,
        title=payload.title.strip(),
        organization=(payload.organization or "").strip(),
        role_name=(payload.role_name or "").strip(),
        status=payload.status,
        applied_date=payload.applied_date,
        exam_date=payload.exam_date,
        deadline=payload.deadline,
        notification_link=payload.notification_link or "",
        apply_link=payload.apply_link or "",
        syllabus=list(payload.syllabus or []),
        exam_pattern=list(payload.exam_pattern or []),
        strategy=payload.strategy or "",
        preparation_plan=list(payload.preparation_plan or []),
        resources=list(payload.resources or []),
        notes=payload.notes or "",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _out(row, job)


@router.post("/from-template/{key}", status_code=status.HTTP_201_CREATED)
def create_my_job_from_template(key: str, user: CurrentUser, db: DbSession) -> dict:
    """One-click add: UIICL AO or EPFO APFC with full syllabus/strategy/plan."""
    tpl = myjobs_templates.get_template(key)
    if tpl is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    existing = db.scalar(
        select(MyJob).where(MyJob.user_id == user.id, MyJob.template_key == key)
    )
    if existing is not None:
        job = db.get(Job, existing.job_id) if existing.job_id else None
        return _out(existing, job)
    row = MyJob(
        user_id=user.id,
        job_id=None,
        template_key=tpl["template_key"],
        title=tpl["title"],
        organization=tpl["organization"],
        role_name=tpl["role_name"],
        status="applied",
        notification_link=tpl.get("notification_link", ""),
        apply_link=tpl.get("apply_link", ""),
        syllabus=list(tpl.get("syllabus", [])),
        exam_pattern=list(tpl.get("exam_pattern", [])),
        strategy=tpl.get("strategy", ""),
        preparation_plan=list(tpl.get("preparation_plan", [])),
        resources=list(tpl.get("resources", [])),
        notes="",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _out(row, None)


@router.post("/{my_job_id}/refresh-template")
def refresh_my_job_from_template(my_job_id: int, user: CurrentUser, db: DbSession) -> dict:
    """Pull the latest syllabus/pattern/strategy/plan/resources from the template.

    Personal fields (status, dates, notes, links) are preserved — only the
    study material is refreshed. Used when templates gain new content (e.g.
    free YouTube/practice links) after the job was already added.
    """
    row = _get_owned(db, user, my_job_id)
    if not row.template_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This job was not added from a template")
    tpl = myjobs_templates.get_template(row.template_key)
    if tpl is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    row.syllabus = list(tpl.get("syllabus", []))
    row.exam_pattern = list(tpl.get("exam_pattern", []))
    row.strategy = tpl.get("strategy", "")
    row.preparation_plan = list(tpl.get("preparation_plan", []))
    row.resources = list(tpl.get("resources", []))
    db.commit()
    db.refresh(row)
    job = db.get(Job, row.job_id) if row.job_id else None
    return _out(row, job)


@router.put("/{my_job_id}")
def update_my_job(my_job_id: int, payload: MyJobUpdate, user: CurrentUser, db: DbSession) -> dict:
    row = _get_owned(db, user, my_job_id)
    data = payload.model_dump(exclude_unset=True)
    if "status" in data and data["status"] not in _VALID_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    if data.get("job_id") is not None:
        job = db.get(Job, data["job_id"])
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    for field, value in data.items():
        if field in {"title", "organization", "role_name"} and isinstance(value, str):
            value = value.strip()
            if field == "title" and not value:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title required")
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    job = db.get(Job, row.job_id) if row.job_id else None
    return _out(row, job)


@router.delete("/{my_job_id}")
def delete_my_job(my_job_id: int, user: CurrentUser, db: DbSession) -> dict:
    row = _get_owned(db, user, my_job_id)
    db.delete(row)
    db.commit()
    return {"message": "Removed from My Jobs List"}
