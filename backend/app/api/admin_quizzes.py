from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import AdminUser, DbSession
from app.models import Question, Quiz
from app.schemas.admin import QuestionCreate, QuestionUpdate, QuizCreate, QuizUpdate
from app.services.common import quiz_summary, unique_slug

router = APIRouter(tags=["admin"])


def _page_params(page: int, page_size: int) -> tuple[int, int, int]:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    return page, page_size, (page - 1) * page_size


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def _quiz_admin_out(quiz: Quiz) -> dict:
    return {**quiz_summary(quiz), "topic_id": quiz.topic_id, "exam_id": quiz.exam_id,
            "current_affair_id": quiz.current_affair_id, "created_by": quiz.created_by}


def _question_out(question: Question) -> dict:
    return {
        "id": question.id,
        "quiz_id": question.quiz_id,
        "question_text": question.question_text,
        "options": list(question.options or []),
        "correct_index": question.correct_index,
        "explanation": question.explanation or "",
        "difficulty": question.difficulty,
        "order": question.order,
        "tags": list(question.tags or []),
    }


@router.get("/quizzes")
def admin_list_quizzes(
    admin: AdminUser,
    db: DbSession,
    page: int = 1,
    page_size: int = 20,
    quiz_type: str | None = None,
    q: str | None = None,
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Quiz)
    if quiz_type:
        stmt = stmt.where(Quiz.quiz_type == quiz_type)
    if q:
        stmt = stmt.where(func.lower(Quiz.title).contains(q.lower()))
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Quiz.id.desc()).offset(offset).limit(page_size)).all()
    return {
        "items": [_quiz_admin_out(row) for row in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


@router.post("/quizzes")
def admin_create_quiz(payload: QuizCreate, admin: AdminUser, db: DbSession) -> dict:
    data = payload.model_dump()
    slug = unique_slug(db, Quiz, data.pop("slug") or payload.title)
    quiz = Quiz(**data, slug=slug, created_by=admin.id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return _quiz_admin_out(quiz)


@router.put("/quizzes/{id}")
def admin_update_quiz(id: int, payload: QuizUpdate, admin: AdminUser, db: DbSession) -> dict:
    quiz = db.get(Quiz, id)
    if quiz is None:
        raise _not_found("Quiz not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("slug"):
        data["slug"] = unique_slug(db, Quiz, data["slug"], exclude_id=quiz.id)
    for field, value in data.items():
        setattr(quiz, field, value)
    db.commit()
    db.refresh(quiz)
    return _quiz_admin_out(quiz)


@router.delete("/quizzes/{id}")
def admin_delete_quiz(id: int, admin: AdminUser, db: DbSession) -> dict:
    quiz = db.get(Quiz, id)
    if quiz is None:
        raise _not_found("Quiz not found")
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted"}


@router.post("/quizzes/{id}/publish")
def admin_toggle_publish(id: int, admin: AdminUser, db: DbSession) -> dict:
    quiz = db.get(Quiz, id)
    if quiz is None:
        raise _not_found("Quiz not found")
    quiz.is_published = not quiz.is_published
    db.commit()
    db.refresh(quiz)
    return _quiz_admin_out(quiz)


@router.get("/questions")
def admin_list_questions(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, quiz_id: int | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Question)
    if quiz_id is not None:
        stmt = stmt.where(Question.quiz_id == quiz_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Question.order, Question.id).offset(offset).limit(page_size)).all()
    return {
        "items": [_question_out(row) for row in rows],
        "total": int(total),
        "page": page,
        "page_size": page_size,
    }


@router.post("/questions")
def admin_create_question(payload: QuestionCreate, admin: AdminUser, db: DbSession) -> dict:
    quiz = db.get(Quiz, payload.quiz_id)
    if quiz is None:
        raise _not_found("Quiz not found")
    if payload.correct_index >= len(payload.options):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="correct_index is out of range for options",
        )
    question = Question(**payload.model_dump())
    db.add(question)
    db.flush()
    quiz.total_questions = (
        db.scalar(select(func.count(Question.id)).where(Question.quiz_id == quiz.id)) or 0
    )
    db.commit()
    db.refresh(question)
    return _question_out(question)


@router.put("/questions/{id}")
def admin_update_question(id: int, payload: QuestionUpdate, admin: AdminUser, db: DbSession) -> dict:
    question = db.get(Question, id)
    if question is None:
        raise _not_found("Question not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("quiz_id") is not None and db.get(Quiz, data["quiz_id"]) is None:
        raise _not_found("Quiz not found")
    options = data.get("options", question.options or [])
    correct_index = data.get("correct_index", question.correct_index)
    if correct_index is not None and correct_index >= len(options):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="correct_index is out of range for options",
        )
    for field, value in data.items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return _question_out(question)


@router.delete("/questions/{id}")
def admin_delete_question(id: int, admin: AdminUser, db: DbSession) -> dict:
    question = db.get(Question, id)
    if question is None:
        raise _not_found("Question not found")
    quiz_id = question.quiz_id
    db.delete(question)
    db.flush()
    quiz = db.get(Quiz, quiz_id)
    if quiz is not None:
        quiz.total_questions = (
            db.scalar(select(func.count(Question.id)).where(Question.quiz_id == quiz.id)) or 0
        )
    db.commit()
    return {"message": "Question deleted"}
