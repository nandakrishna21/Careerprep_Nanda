from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Profile, User


def get_or_create_profile(db: Session, user: User) -> Profile:
    profile = db.scalar(select(Profile).where(Profile.user_id == user.id))
    if profile is None:
        profile = Profile(user_id=user.id)
        db.add(profile)
        db.flush()
    return profile


def apply_daily_streak(profile: Profile, today: date | None = None) -> None:
    today = today or datetime.now(timezone.utc).date()
    last = profile.last_active_date
    if last == today:
        pass
    elif last is not None and last == today - timedelta(days=1):
        profile.streak_days = (profile.streak_days or 0) + 1
    else:
        profile.streak_days = 1
    profile.last_active_date = today


def award_xp(profile: Profile, points: int) -> int:
    profile.xp = (profile.xp or 0) + int(points)
    profile.level = profile.xp // 500 + 1
    return profile.xp
