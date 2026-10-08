from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.security import CurrentUser, DbSession
from app.models import Quiz, QuizAttempt, UserAchievement
from app.schemas.quiz import AttemptRequest
from app.services import scoring

router = APIRouter(tags=["quiz"])


def _get_published_quiz(db, quiz_id: int) -> Quiz:
    quiz = db.get(Quiz, quiz_id)
    if quiz is None or not quiz.is_published:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return quiz


@router.get("/quizzes/{id}")
def get_quiz(id: int, db: DbSession) -> dict:
    quiz = _get_published_quiz(db, id)
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
        "topic": {"id": quiz.topic.id, "title": quiz.topic.title} if quiz.topic else None,
        "exam": {"id": quiz.exam.id, "title": quiz.exam.name} if quiz.exam else None,
        "meta": quiz.meta or {},
        "mode_options": {"practice": True, "exam": True},
    }


@router.get("/quizzes/{id}/questions")
def get_quiz_questions(id: int, db: DbSession) -> list[dict]:
    _get_published_quiz(db, id)
    questions = scoring.load_questions(db, id)
    return [
        {
            "id": question.id,
            "question_text": question.question_text,
            "options": list(question.options or []),
            "order": question.order,
        }
        for question in questions
    ]


@router.post("/quizzes/{id}/attempt")
def submit_quiz_attempt(id: int, payload: AttemptRequest, user: CurrentUser, db: DbSession) -> dict:
    quiz = _get_published_quiz(db, id)
    answers: dict[int, int] = {}
    for key, value in payload.answers.items():
        try:
            answers[int(key)] = int(value)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid answer entry: {key}",
            )
    return scoring.submit_attempt(
        db=db,
        user=user,
        quiz=quiz,
        answers=answers,
        time_taken_seconds=payload.time_taken_seconds,
        mode=payload.mode,
    )


@router.get("/attempts/mine")
def my_attempts(user: CurrentUser, db: DbSession, quiz_id: int | None = None) -> list[dict]:
    stmt = select(QuizAttempt).where(QuizAttempt.user_id == user.id)
    if quiz_id is not None:
        stmt = stmt.where(QuizAttempt.quiz_id == quiz_id)
    stmt = stmt.order_by(QuizAttempt.created_at.desc(), QuizAttempt.id.desc())
    attempts = db.scalars(stmt).all()
    items: list[dict] = []
    for attempt in attempts:
        data = scoring.attempt_payload(attempt)
        quiz = db.get(Quiz, attempt.quiz_id)
        data["quiz_title"] = quiz.title if quiz else None
        items.append(data)
    return items


@router.get("/attempts/{id}")
def get_attempt(id: int, user: CurrentUser, db: DbSession) -> dict:
    attempt = db.get(QuizAttempt, id)
    if attempt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    if attempt.user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    rows = db.scalars(select(UserAchievement).where(UserAchievement.user_id == user.id)).all()
    unlocked = [
        {
            "code": row.achievement.code,
            "title": row.achievement.title,
            "icon": row.achievement.icon,
            "xp_reward": row.achievement.xp_reward,
        }
        for row in rows
    ]
    return {
        "attempt": scoring.attempt_payload(attempt),
        "report": scoring.build_report(db, attempt),
        "achievements_unlocked": unlocked,
    }
