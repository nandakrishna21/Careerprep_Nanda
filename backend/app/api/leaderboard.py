from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.security import CurrentUser, DbSession
from app.models import Achievement, Notification, Profile, User, UserAchievement, XpEvent
from app.schemas.misc import NotificationReadRequest
from app.services.common import naive_utc_now

router = APIRouter(tags=["gamification"])


def _achievement_row(row: UserAchievement) -> dict:
    achievement = row.achievement
    return {
        "id": achievement.id,
        "code": achievement.code,
        "title": achievement.title,
        "description": achievement.description or "",
        "icon": achievement.icon,
        "xp_reward": achievement.xp_reward,
        "unlocked": True,
        "unlocked_at": row.unlocked_at,
    }


@router.get("/leaderboard")
def leaderboard(
    db: DbSession,
    period: Literal["weekly", "monthly", "all_time"] = "weekly",
    exam: str | None = None,
) -> list[dict]:
    rows = db.execute(
        select(Profile, User)
        .join(User, User.id == Profile.user_id)
        .where(User.is_active.is_(True))
    ).all()

    points: dict[int, int] = defaultdict(int)
    if period != "all_time":
        days = 7 if period == "weekly" else 30
        cutoff = naive_utc_now() - timedelta(days=days)
        events = db.scalars(select(XpEvent).where(XpEvent.created_at >= cutoff)).all()
        for event in events:
            points[event.user_id] += event.points or 0

    entries: list[dict] = []
    for profile, user in rows:
        if exam and exam not in (profile.target_exams or []):
            continue
        xp = (profile.xp or 0) if period == "all_time" else points.get(profile.user_id, 0)
        entries.append(
            {
                "id": user.id,
                "full_name": user.full_name,
                "avatar_color": profile.avatar_color or "indigo",
                "xp": int(xp),
                "streak_days": profile.streak_days or 0,
                "level": profile.level or 1,
            }
        )
    entries.sort(key=lambda entry: (-entry["xp"], entry["id"]))
    top = entries[:50]
    return [{**entry, "rank": index} for index, entry in enumerate(top, start=1)]


@router.get("/achievements")
def list_achievements(user: CurrentUser, db: DbSession) -> list[dict]:
    achievements = db.scalars(select(Achievement).order_by(Achievement.id)).all()
    unlocked_rows = db.scalars(
        select(UserAchievement).where(UserAchievement.user_id == user.id)
    ).all()
    unlocked = {row.achievement_id: row for row in unlocked_rows}
    items = []
    for achievement in achievements:
        row = unlocked.get(achievement.id)
        items.append(
            {
                "id": achievement.id,
                "code": achievement.code,
                "title": achievement.title,
                "description": achievement.description or "",
                "icon": achievement.icon,
                "xp_reward": achievement.xp_reward,
                "unlocked": row is not None,
                "unlocked_at": row.unlocked_at if row else None,
            }
        )
    return items


@router.get("/achievements/mine")
def my_achievements(user: CurrentUser, db: DbSession) -> list[dict]:
    rows = db.scalars(
        select(UserAchievement).where(UserAchievement.user_id == user.id).order_by(
            UserAchievement.unlocked_at.desc()
        )
    ).all()
    return [_achievement_row(row) for row in rows]


@router.get("/notifications")
def list_notifications(user: CurrentUser, db: DbSession) -> list[dict]:
    rows = db.scalars(
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc(), Notification.id.desc())
    ).all()
    return [
        {
            "id": row.id,
            "title": row.title,
            "body": row.body or "",
            "type": row.type or "info",
            "is_read": row.is_read,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.post("/notifications/read")
def mark_notifications_read(
    payload: NotificationReadRequest, user: CurrentUser, db: DbSession
) -> dict:
    stmt = select(Notification).where(
        Notification.user_id == user.id, Notification.is_read.is_(False)
    )
    if payload.ids is not None:
        if not payload.ids:
            return {"message": "No notifications updated", "updated": 0}
        stmt = stmt.where(Notification.id.in_(payload.ids))
    rows = db.scalars(stmt).all()
    for row in rows:
        row.is_read = True
    db.commit()
    return {"message": "Notifications marked as read", "updated": len(rows)}
