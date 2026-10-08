from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.security import CurrentUser, DbSession
from app.models import Resume, User
from app.schemas.misc import ResumeCreate, ResumeUpdate
from app.services import achievements, gemini

router = APIRouter(tags=["resumes"])

_ANALYSIS_SYSTEM = "You are an expert ATS resume reviewer. You always answer with strict, valid JSON only."


def _serialize_resume(data: dict) -> str:
    personal = data.get("personal") or {}
    lines = [
        f"Name: {personal.get('name', '')}",
        f"Email: {personal.get('email', '')}",
        f"Phone: {personal.get('phone', '')}",
        f"Location: {personal.get('location', '')}",
        f"Summary: {personal.get('summary', '')}",
        "",
        "SKILLS",
        ", ".join(str(skill) for skill in (data.get("skills") or [])),
        "",
        "EDUCATION",
    ]
    for item in data.get("education") or []:
        lines.append(
            f"- {item.get('degree', '')} at {item.get('school', '')} ({item.get('year', '')})"
        )
    lines.append("")
    lines.append("PROJECTS")
    for item in data.get("projects") or []:
        lines.append(f"- {item.get('name', '')}: {item.get('description', '')} {item.get('link', '')}")
    lines.append("")
    lines.append("EXPERIENCE")
    for item in data.get("experience") or []:
        lines.append(
            f"- {item.get('role', '')} at {item.get('company', '')} ({item.get('period', '')}): "
            f"{item.get('description', '')}"
        )
    return "\n".join(line for line in lines if line is not None).strip()


def _resume_out(resume: Resume) -> dict:
    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "title": resume.title,
        "template": resume.template,
        "data": resume.data or {},
        "ats_score": resume.ats_score,
        "analysis": resume.analysis,
        "created_at": resume.created_at,
        "updated_at": resume.updated_at,
    }


def _owned_resume(db, resume_id: int, user: User) -> Resume:
    resume = db.get(Resume, resume_id)
    if resume is None or resume.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return resume


@router.post("")
def create_resume(payload: ResumeCreate, user: CurrentUser, db: DbSession) -> dict:
    resume = Resume(
        user_id=user.id,
        title=payload.title,
        template=payload.template,
        data=payload.data,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return _resume_out(resume)


@router.get("/mine")
def list_my_resumes(user: CurrentUser, db: DbSession) -> list[dict]:
    rows = db.scalars(
        select(Resume).where(Resume.user_id == user.id).order_by(Resume.updated_at.desc())
    ).all()
    return [_resume_out(row) for row in rows]


@router.get("/{id}")
def get_resume(id: int, user: CurrentUser, db: DbSession) -> dict:
    return _resume_out(_owned_resume(db, id, user))


@router.put("/{id}")
def update_resume(id: int, payload: ResumeUpdate, user: CurrentUser, db: DbSession) -> dict:
    resume = _owned_resume(db, id, user)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        if value is None:
            continue
        setattr(resume, field, value)
    if "data" in updates:
        resume.ats_score = None
        resume.analysis = None
    db.commit()
    db.refresh(resume)
    return _resume_out(resume)


@router.delete("/{id}")
def delete_resume(id: int, user: CurrentUser, db: DbSession) -> dict:
    resume = _owned_resume(db, id, user)
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted"}


@router.post("/{id}/analyze")
def analyze_stored_resume(id: int, user: CurrentUser, db: DbSession) -> dict:
    resume = _owned_resume(db, id, user)
    text = _serialize_resume(resume.data or {})
    prompt = (
        "Analyse this resume for ATS readiness.\n"
        f"Resume:\n\"\"\"\n{text}\n\"\"\"\n"
        "Respond with strict JSON: {\"ats_score\": <integer 0-100>, "
        "\"missing_keywords\": [<strings>], \"suggestions\": [<strings>], "
        "\"job_recommendations\": [{\"title\": <string>, \"reason\": <string>}]}."
    )
    result = gemini.generate_json(prompt, system=_ANALYSIS_SYSTEM, temperature=0.4)
    if not isinstance(result, dict):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    try:
        ats_score = int(round(float(result.get("ats_score", 0))))
    except (TypeError, ValueError):
        ats_score = 0
    ats_score = max(0, min(100, ats_score))
    analysis = {
        "ats_score": ats_score,
        "missing_keywords": [str(item) for item in (result.get("missing_keywords") or [])],
        "suggestions": [str(item) for item in (result.get("suggestions") or [])],
        "job_recommendations": [
            {
                "title": str(item.get("title") or ""),
                "reason": str(item.get("reason") or ""),
            }
            for item in (result.get("job_recommendations") or [])
            if isinstance(item, dict)
        ],
    }
    resume.ats_score = ats_score
    resume.analysis = analysis
    db.commit()
    achievements.unlock(db, user, "resume_first")
    return {"ats_score": ats_score, "analysis": analysis}
