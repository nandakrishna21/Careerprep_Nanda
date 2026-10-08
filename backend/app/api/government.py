from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, or_, select

from app.core.security import AdminUser, DbSession
from app.models import CurrentAffair, Exam, MockTest, Question, Quiz, Topic, QuizAttempt
from app.services.common import quiz_summary, unique_slug

router = APIRouter(tags=["government"])


def _maybe_id(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return -1


@router.get("/mock-tests")
def list_mock_tests(db: DbSession, category: str | None = None) -> list[dict]:
    stmt = select(MockTest).where(MockTest.is_published.is_(True))
    if category:
        stmt = stmt.where(MockTest.category == category)
    stmt = stmt.order_by(MockTest.id)
    tests = db.scalars(stmt).all()
    counts = dict(
        db.execute(
            select(QuizAttempt.quiz_id, func.count(QuizAttempt.id)).group_by(QuizAttempt.quiz_id)
        ).all()
    )
    return [
        {
            "id": test.id,
            "title": test.title,
            "slug": test.slug,
            "category": test.category,
            "description": test.description or "",
            "duration_minutes": test.duration_minutes,
            "total_questions": test.total_questions,
            "negative_marks": float(test.negative_marks or 0),
            "sections": test.sections or [],
            "exam_pattern": test.exam_pattern or {},
            "quiz_id": test.quiz_id,
            "attempts_count": int(counts.get(test.quiz_id, 0)) if test.quiz_id else 0,
        }
        for test in tests
    ]


@router.get("/mock-tests/{slug}")
def get_mock_test(slug: str, db: DbSession) -> dict:
    test = db.scalar(select(MockTest).where(MockTest.slug == slug, MockTest.is_published.is_(True)))
    if test is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mock test not found")
    count = 0
    if test.quiz_id:
        count = (
            db.scalar(
                select(func.count(QuizAttempt.id)).where(QuizAttempt.quiz_id == test.quiz_id)
            )
            or 0
        )
    return {
        "id": test.id,
        "title": test.title,
        "slug": test.slug,
        "category": test.category,
        "description": test.description or "",
        "duration_minutes": test.duration_minutes,
        "total_questions": test.total_questions,
        "negative_marks": float(test.negative_marks or 0),
        "sections": test.sections or [],
        "exam_pattern": test.exam_pattern or {},
        "quiz_id": test.quiz_id,
        "attempts_count": int(count),
    }


@router.get("/pyqs")
def list_pyqs(
    db: DbSession,
    exam: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
) -> list[dict]:
    stmt = select(Quiz).where(Quiz.quiz_type == "pyq", Quiz.is_published.is_(True))
    if difficulty:
        stmt = stmt.where(Quiz.difficulty == difficulty)
    if exam:
        value = exam.strip().lower()
        stmt = stmt.join(Exam, Exam.id == Quiz.exam_id).where(
            or_(func.lower(Exam.slug) == value, func.lower(Exam.name).contains(value), Exam.id == _maybe_id(exam))
        )
    if topic:
        value = topic.strip().lower()
        stmt = stmt.join(Topic, Topic.id == Quiz.topic_id).where(
            or_(func.lower(Topic.slug) == value, func.lower(Topic.title).contains(value), Topic.id == _maybe_id(topic))
        )
    stmt = stmt.order_by(Quiz.id)
    quizzes = db.scalars(stmt).all()
    items = []
    for quiz in quizzes:
        items.append(
            {
                **quiz_summary(quiz),
                "exam": {"id": quiz.exam.id, "title": quiz.exam.name} if quiz.exam else None,
                "topic": {"id": quiz.topic.id, "title": quiz.topic.title} if quiz.topic else None,
            }
        )
    return items


@router.get("/current-affairs")
def list_current_affairs(db: DbSession, period: str | None = None) -> list[dict]:
    stmt = select(CurrentAffair).where(CurrentAffair.is_published.is_(True))
    if period:
        stmt = stmt.where(CurrentAffair.period == period)
    stmt = stmt.order_by(CurrentAffair.date.desc(), CurrentAffair.id.desc())
    rows = db.scalars(stmt).all()
    return [
        {
            "id": row.id,
            "title": row.title,
            "slug": row.slug,
            "period": row.period,
            "date": row.date,
            "summary": row.summary or "",
        }
        for row in rows
    ]


@router.get("/current-affairs/{slug}")
def get_current_affair(slug: str, db: DbSession) -> dict:
    row = db.scalar(
        select(CurrentAffair).where(CurrentAffair.slug == slug, CurrentAffair.is_published.is_(True))
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current affair not found")
    quiz = db.scalar(
        select(Quiz)
        .where(Quiz.current_affair_id == row.id, Quiz.is_published.is_(True))
        .order_by(Quiz.id.desc())
    )
    return {
        "id": row.id,
        "title": row.title,
        "slug": row.slug,
        "period": row.period,
        "date": row.date,
        "summary": row.summary or "",
        "content": row.content or "",
        "ai_content": row.ai_content or {},
        "quiz_id": quiz.id if quiz else None,
        "quiz": quiz_summary(quiz) if quiz else None,
        "created_at": row.created_at,
    }


@router.post("/current-affairs/{id}/generate-quiz")
def generate_current_affair_quiz(id: int, admin: AdminUser, db: DbSession) -> dict:
    affair = db.get(CurrentAffair, id)
    if affair is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current affair not found")
    mcqs = (affair.ai_content or {}).get("mcqs") or []
    if not isinstance(mcqs, list) or not mcqs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This current affair has no MCQs to convert into a quiz",
        )
    questions: list[dict] = []
    for index, mcq in enumerate(mcqs):
        if not isinstance(mcq, dict) or not mcq.get("question") or not mcq.get("options"):
            continue
        try:
            correct_index = int(mcq.get("correct_index", 0))
        except (TypeError, ValueError):
            continue
        questions.append(
            {
                "question_text": str(mcq["question"]),
                "options": [str(option) for option in mcq["options"]],
                "correct_index": correct_index,
                "explanation": str(mcq.get("explanation") or ""),
                "difficulty": str(mcq.get("difficulty") or "intermediate"),
                "order": index,
            }
        )
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid MCQs found in ai_content.mcqs",
        )

    slug = unique_slug(db, Quiz, f"{affair.slug}-quiz")
    quiz = Quiz(
        title=f"{affair.title} — MCQ Quiz"[:255],
        slug=slug,
        quiz_type="current_affair",
        current_affair_id=affair.id,
        difficulty="intermediate",
        duration_minutes=max(5, len(questions)),
        negative_marks=0,
        total_questions=len(questions),
        is_published=True,
        meta={"source": "current_affairs", "date": str(affair.date)},
    )
    db.add(quiz)
    db.flush()
    for item in questions:
        db.add(
            Question(
                quiz_id=quiz.id,
                question_text=item["question_text"],
                options=item["options"],
                correct_index=item["correct_index"],
                explanation=item["explanation"],
                difficulty=item["difficulty"],
                order=item["order"],
                tags=["Current Affairs"],
            )
        )
    db.commit()
    db.refresh(quiz)
    return {**quiz_summary(quiz), "questions_created": len(questions)}
