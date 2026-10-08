from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import CurrentUser, DbSession
from app.models import Quiz, QuizAttempt, StudySession, Topic, UserAchievement, XpEvent
from app.schemas.misc import StudySessionCreate
from app.services.profiles import apply_daily_streak, award_xp, get_or_create_profile

router = APIRouter(tags=["progress"])


def _entry_date(value: datetime) -> date:
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def _topic_accuracy(entries: list[dict]) -> dict[str, list[int]]:
    totals: dict[str, list[int]] = {}
    for entry in entries:
        name = entry.get("name")
        if not name:
            continue
        bucket = totals.setdefault(str(name), [0, 0])
        bucket[0] += int(entry.get("total", 0) or 0)
        bucket[1] += int(entry.get("correct", 0) or 0)
    return totals


@router.get("/dashboard")
def dashboard(user: CurrentUser, db: DbSession) -> dict:
    profile = get_or_create_profile(db, user)
    db.commit()

    attempts = db.scalars(
        select(QuizAttempt).where(QuizAttempt.user_id == user.id).order_by(QuizAttempt.id)
    ).all()
    sessions = db.scalars(
        select(StudySession).where(StudySession.user_id == user.id)
    ).all()
    weekly_cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=7)
    events = db.scalars(
        select(XpEvent).where(XpEvent.user_id == user.id, XpEvent.created_at >= weekly_cutoff)
    ).all()

    total_quizzes = len(attempts)
    average_score = (
        round(sum(float(attempt.accuracy or 0) for attempt in attempts) / total_quizzes, 2)
        if total_quizzes
        else 0.0
    )
    total_study_hours = round(sum(session.minutes or 0 for session in sessions) / 60, 2)
    weekly_xp = sum(event.points or 0 for event in events)

    breakdown_totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for attempt in attempts:
        entries = (attempt.analysis or {}).get("topic_breakdown") or []
        for name, pair in _topic_accuracy(entries).items():
            bucket = breakdown_totals[name]
            bucket[0] += pair[0]
            bucket[1] += pair[1]

    topic_rows: list[dict] = []
    if breakdown_totals:
        for name, (total, correct) in breakdown_totals.items():
            accuracy = round(correct / total * 100, 2) if total else 0.0
            topic_rows.append({"name": name, "accuracy": accuracy})
    else:
        fallback: dict[str, list[float]] = defaultdict(list)
        for attempt in attempts:
            quiz = db.get(Quiz, attempt.quiz_id)
            if quiz is not None and quiz.topic is not None:
                fallback[quiz.topic.title].append(float(attempt.accuracy or 0))
        for name, values in fallback.items():
            topic_rows.append(
                {"name": name, "accuracy": round(sum(values) / len(values), 2) if values else 0.0}
            )

    strong_topics = sorted(
        [row for row in topic_rows if row["accuracy"] >= 80], key=lambda row: -row["accuracy"]
    )
    weak_topics = sorted(
        [row for row in topic_rows if row["accuracy"] < 60], key=lambda row: row["accuracy"]
    )

    mock_tests_taken = (
        db.scalar(
            select(func.count(QuizAttempt.id))
            .join(Quiz, Quiz.id == QuizAttempt.quiz_id)
            .where(QuizAttempt.user_id == user.id, Quiz.quiz_type == "mock")
        )
        or 0
    )
    badges_unlocked = (
        db.scalar(select(func.count(UserAchievement.id)).where(UserAchievement.user_id == user.id))
        or 0
    )

    today = datetime.now(timezone.utc).date()
    window = [today - timedelta(days=offset) for offset in range(13, -1, -1)]
    minutes_by_day: dict[datetime, float] = defaultdict(float)
    for session in sessions:
        minutes_by_day[_entry_date(session.created_at).date()] += session.minutes or 0
    quizzes_by_day: dict[datetime, int] = defaultdict(int)
    accuracy_by_day: dict[datetime, list[float]] = defaultdict(list)
    for attempt in attempts:
        day = _entry_date(attempt.created_at).date()
        quizzes_by_day[day] += 1
        accuracy_by_day[day].append(float(attempt.accuracy or 0))

    daily_activity = [
        {
            "date": day.isoformat(),
            "hours": round(minutes_by_day.get(day, 0) / 60, 2),
            "quizzes": int(quizzes_by_day.get(day, 0)),
        }
        for day in window
    ]
    performance_trend = [
        {
            "date": day.isoformat(),
            "score": round(
                sum(accuracy_by_day.get(day, [])) / len(accuracy_by_day.get(day, [])), 2
            )
            if accuracy_by_day.get(day)
            else 0.0,
        }
        for day in window
    ]

    mock_rows: list[dict] = []
    for attempt in reversed(attempts):
        quiz = db.get(Quiz, attempt.quiz_id)
        if quiz is None or quiz.quiz_type != "mock":
            continue
        mock_rows.append(
            {
                "title": quiz.title,
                "score": float(attempt.score or 0),
                "accuracy": round(float(attempt.accuracy or 0), 2),
                "date": _entry_date(attempt.created_at).date().isoformat(),
            }
        )
        if len(mock_rows) >= 10:
            break

    return {
        "total_study_hours": total_study_hours,
        "total_quizzes": int(total_quizzes),
        "average_score": average_score,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "streak_days": profile.streak_days or 0,
        "xp": profile.xp or 0,
        "level": profile.level or 1,
        "weekly_xp": int(weekly_xp),
        "mock_tests_taken": int(mock_tests_taken),
        "badges_unlocked": int(badges_unlocked),
        "daily_activity": daily_activity,
        "performance_trend": performance_trend,
        "mock_performance": mock_rows,
    }


@router.post("/study-session")
def create_study_session(
    payload: StudySessionCreate, user: CurrentUser, db: DbSession
) -> dict:
    if payload.topic_id is not None and db.get(Topic, payload.topic_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    session = StudySession(
        user_id=user.id,
        minutes=payload.minutes,
        activity_type=payload.activity_type,
        topic_id=payload.topic_id,
    )
    db.add(session)
    db.flush()
    profile = get_or_create_profile(db, user)
    apply_daily_streak(profile)
    points = payload.minutes // 5
    award_xp(profile, points)
    db.add(XpEvent(user_id=user.id, points=points, kind="study", ref_id=session.id))
    db.commit()
    db.refresh(session)
    return {
        "study_session": {
            "id": session.id,
            "minutes": session.minutes,
            "activity_type": session.activity_type,
            "topic_id": session.topic_id,
            "created_at": session.created_at,
        },
        "streak_days": profile.streak_days or 0,
    }
