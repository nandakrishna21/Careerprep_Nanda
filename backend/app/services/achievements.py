from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Achievement, User, UserAchievement
from app.services.profiles import get_or_create_profile

DEFAULT_ACHIEVEMENTS: list[dict[str, Any]] = [
    {"code": "first_quiz", "title": "First Steps", "icon": "award", "xp_reward": 50,
     "description": "Completed your first quiz."},
    {"code": "quiz_streak_7", "title": "7-Day Streak", "icon": "flame", "xp_reward": 100,
     "description": "Maintained a study streak for 7 days."},
    {"code": "score_90", "title": "Sharpshooter", "icon": "target", "xp_reward": 100,
     "description": "Scored 90% or more on a quiz with at least 10 questions."},
    {"code": "mock_first", "title": "Mock Warrior", "icon": "file-check", "xp_reward": 150,
     "description": "Completed your first full mock test."},
    {"code": "interview_first", "title": "Interview Ready", "icon": "mic", "xp_reward": 150,
     "description": "Completed a mock interview session."},
    {"code": "resume_first", "title": "Resume Pro", "icon": "file-text", "xp_reward": 100,
     "description": "Analysed your first resume."},
    {"code": "xp_1000", "title": "XP Hunter", "icon": "star", "xp_reward": 200,
     "description": "Earned 1000 XP."},
    {"code": "quiz_master", "title": "Quiz Master", "icon": "crown", "xp_reward": 300,
     "description": "Attempted 50 quizzes."},
]


def ensure_defaults(db: Session) -> None:
    for spec in DEFAULT_ACHIEVEMENTS:
        exists = db.scalar(select(Achievement.id).where(Achievement.code == spec["code"]))
        if exists is None:
            db.add(
                Achievement(
                    code=spec["code"],
                    title=spec["title"],
                    description=spec["description"],
                    icon=spec["icon"],
                    xp_reward=spec["xp_reward"],
                    condition={},
                )
            )
    db.commit()


def achievement_dict(achievement: Achievement) -> dict[str, Any]:
    return {
        "code": achievement.code,
        "title": achievement.title,
        "icon": achievement.icon,
        "xp_reward": achievement.xp_reward,
    }


def _has_unlocked(db: Session, user_id: int, achievement_id: int) -> bool:
    row = db.scalar(
        select(UserAchievement.id).where(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement_id,
        )
    )
    return row is not None


def _grant(db: Session, user: User, achievement: Achievement) -> dict[str, Any] | None:
    if _has_unlocked(db, user.id, achievement.id):
        return None
    db.add(UserAchievement(user_id=user.id, achievement_id=achievement.id))
    profile = get_or_create_profile(db, user)
    profile.xp = (profile.xp or 0) + achievement.xp_reward
    profile.level = profile.xp // 500 + 1
    db.flush()
    return achievement_dict(achievement)


def unlock(db: Session, user: User, code: str) -> dict[str, Any] | None:
    achievement = db.scalar(select(Achievement).where(Achievement.code == code))
    if achievement is None:
        return None
    unlocked = _grant(db, user, achievement)
    if unlocked is not None:
        db.commit()
    return unlocked


def evaluate(db: Session, user: User, ctx: dict[str, Any]) -> list[dict[str, Any]]:
    unlocked: list[dict[str, Any]] = []

    def grant(code: str) -> None:
        achievement = db.scalar(select(Achievement).where(Achievement.code == code))
        if achievement is None:
            return
        result = _grant(db, user, achievement)
        if result is not None:
            unlocked.append(result)

    kind = ctx.get("kind")
    if kind == "interview":
        grant("interview_first")
        db.flush()
        return unlocked
    if kind == "resume":
        grant("resume_first")
        db.flush()
        return unlocked

    attempt = ctx.get("attempt") or {}
    quiz = ctx.get("quiz")
    profile = ctx.get("profile")
    accuracy = float(ctx.get("accuracy", attempt.get("accuracy", 0)) or 0)
    total_quizzes = int(ctx.get("total_quizzes", 0) or 0)

    if total_quizzes <= 1:
        grant("first_quiz")
    if profile is not None and (profile.streak_days or 0) >= 7:
        grant("quiz_streak_7")
    if accuracy >= 90 and int(attempt.get("total", 0) or 0) >= 10:
        grant("score_90")
    if quiz is not None and quiz.quiz_type == "mock":
        grant("mock_first")
    if profile is not None and (profile.xp or 0) >= 1000:
        grant("xp_1000")
    if total_quizzes >= 50:
        grant("quiz_master")

    db.flush()
    return unlocked
