from __future__ import annotations

import re
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.job_taxonomy import experience_label, role_label

_SLUG_RE = re.compile(r"[^a-z0-9]+")

_SHORT_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def short_code(job_id: int) -> str:
    """Compact base62 id for share links (``/s/a3f9``). No storage needed."""
    if job_id <= 0:
        raise ValueError("job id must be positive")
    digits: list[str] = []
    value = job_id
    while value:
        value, remainder = divmod(value, 62)
        digits.append(_SHORT_ALPHABET[remainder])
    return "".join(reversed(digits))


def decode_short_code(code: str) -> int | None:
    """Reverse of :func:`short_code`; ``None`` when malformed."""
    text = (code or "").strip()
    if not text or len(text) > 11 or any(ch not in _SHORT_ALPHABET for ch in text):
        return None
    value = 0
    for ch in text:
        value = value * 62 + _SHORT_ALPHABET.index(ch)
    return value if value > 0 else None


def share_url(job_id: int | None) -> str:
    from app.core.config import settings

    if not job_id:
        return ""
    base = (settings.frontend_url or "http://localhost:5173").rstrip("/")
    return f"{base}/s/{short_code(job_id)}"


def slugify(value: str) -> str:
    slug = _SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "item"


def unique_slug(db: Session, model: type, base: str, exclude_id: int | None = None) -> str:
    root = slugify(base)
    slug = root
    counter = 1
    while True:
        existing = db.scalar(select(model.id).where(model.slug == slug))
        if existing is None or (exclude_id is not None and existing == exclude_id):
            return slug
        counter += 1
        slug = f"{root}-{counter}"


def naive_utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def utc_date() -> date:
    return naive_utc_now().date()


def quiz_summary(quiz) -> dict:
    return {
        "id": quiz.id,
        "title": quiz.title,
        "slug": quiz.slug,
        "quiz_type": quiz.quiz_type,
        "difficulty": quiz.difficulty,
        "duration_minutes": quiz.duration_minutes,
        "total_questions": quiz.total_questions,
        "negative_marks": float(quiz.negative_marks or 0),
        "sections": quiz.sections,
        "meta": quiz.meta or {},
        "is_published": quiz.is_published,
    }


def course_brief(course) -> dict:
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "category": course.category,
        "description": course.description or "",
        "icon": course.icon or "book",
        "level": course.level or "Beginner",
        "career_path": bool(course.career_path),
    }


def exam_brief(exam) -> dict:
    return {
        "id": exam.id,
        "name": exam.name,
        "slug": exam.slug,
        "category": exam.category,
        "description": exam.description or "",
        "pattern": exam.pattern or {},
    }


def job_brief(job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company or "",
        "type": job.type,
        "category": job.category,
        "description": job.description or "",
        "location": job.location or "",
        "salary": job.salary or "",
        "apply_link": job.apply_link or "#",
        "deadline": job.deadline,
        "source": job.source or "",
        "role": role_label(job.role) if job.role else "",
        "city": job.city or "",
        "experience": experience_label(job.exp_min, job.exp_max),
        "posted_at": job.posted_at,
        "created_at": job.created_at,
        "share_url": share_url(job.id),
    }


def profile_brief(profile) -> dict | None:
    if profile is None:
        return None
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "headline": profile.headline or "",
        "bio": profile.bio or "",
        "phone": profile.phone or "",
        "education": profile.education or "",
        "skills": list(profile.skills or []),
        "target_exams": list(profile.target_exams or []),
        "avatar_color": profile.avatar_color or "indigo",
        "xp": profile.xp or 0,
        "level": profile.level or 1,
        "streak_days": profile.streak_days or 0,
        "last_active_date": profile.last_active_date,
    }


def user_brief(user) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }
