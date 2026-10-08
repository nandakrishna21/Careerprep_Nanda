from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import DbSession
from app.models import Course, Exam, Lesson, Quiz, Topic
from app.services.common import course_brief, exam_brief, quiz_summary

router = APIRouter(tags=["catalog"])


def _topic_counts(db) -> tuple[dict[int, int], dict[int, int]]:
    lesson_counts = dict(
        db.execute(select(Lesson.topic_id, func.count(Lesson.id)).group_by(Lesson.topic_id)).all()
    )
    quiz_counts = dict(
        db.execute(
            select(Quiz.topic_id, func.count(Quiz.id))
            .where(Quiz.is_published.is_(True))
            .group_by(Quiz.topic_id)
        ).all()
    )
    return lesson_counts, quiz_counts


@router.get("/courses")
def list_courses(db: DbSession, category: str | None = None) -> list[dict]:
    topic_count = (
        select(func.count(Topic.id)).where(Topic.course_id == Course.id).correlate(Course).scalar_subquery()
    )
    stmt = select(Course, topic_count.label("topic_count")).where(Course.is_published.is_(True))
    if category:
        stmt = stmt.where(Course.category == category)
    stmt = stmt.order_by(Course.order, Course.id)
    rows = db.execute(stmt).all()
    return [{**course_brief(course), "topic_count": int(count or 0)} for course, count in rows]


@router.get("/courses/{slug}")
def get_course(slug: str, db: DbSession) -> dict:
    course = db.scalar(select(Course).where(Course.slug == slug, Course.is_published.is_(True)))
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    topics = db.scalars(
        select(Topic).where(Topic.course_id == course.id).order_by(Topic.order, Topic.id)
    ).all()
    lesson_counts, quiz_counts = _topic_counts(db)
    return {
        **course_brief(course),
        "topics": [
            {
                "id": topic.id,
                "title": topic.title,
                "slug": topic.slug,
                "description": topic.description or "",
                "order": topic.order,
                "lesson_count": int(lesson_counts.get(topic.id, 0)),
                "quiz_count": int(quiz_counts.get(topic.id, 0)),
            }
            for topic in topics
        ],
    }


@router.get("/topics/{slug}")
def get_topic(slug: str, db: DbSession) -> dict:
    topic = db.scalar(select(Topic).where(Topic.slug == slug))
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    course = topic.course
    lessons = db.scalars(
        select(Lesson).where(Lesson.topic_id == topic.id).order_by(Lesson.order, Lesson.id)
    ).all()
    quizzes = db.scalars(
        select(Quiz)
        .where(Quiz.topic_id == topic.id, Quiz.is_published.is_(True))
        .order_by(Quiz.id)
    ).all()
    return {
        "id": topic.id,
        "title": topic.title,
        "slug": topic.slug,
        "description": topic.description or "",
        "order": topic.order,
        "course": course_brief(course) if course is not None else None,
        "lessons": [{"id": lesson.id, "title": lesson.title, "order": lesson.order} for lesson in lessons],
        "quizzes": [quiz_summary(quiz) for quiz in quizzes],
    }


@router.get("/lessons/{id}")
def get_lesson(id: int, db: DbSession) -> dict:
    lesson = db.get(Lesson, id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    topic = lesson.topic
    course = topic.course if topic is not None else None
    return {
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content or {},
        "topic": {
            "id": topic.id,
            "title": topic.title,
            "slug": topic.slug,
            "course": course_brief(course) if course is not None else None,
        },
    }


@router.get("/exams")
def list_exams(db: DbSession) -> list[dict]:
    exams = db.scalars(
        select(Exam).where(Exam.is_published.is_(True)).order_by(Exam.id)
    ).all()
    return [exam_brief(exam) for exam in exams]


@router.get("/exams/{slug}")
def get_exam(slug: str, db: DbSession) -> dict:
    exam = db.scalar(select(Exam).where(Exam.slug == slug, Exam.is_published.is_(True)))
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    quizzes = db.scalars(
        select(Quiz).where(Quiz.exam_id == exam.id, Quiz.is_published.is_(True)).order_by(Quiz.id)
    ).all()
    course_ids: set[int] = set()
    for quiz in quizzes:
        if quiz.topic is not None:
            course_ids.add(quiz.topic.course_id)
    if course_ids:
        courses = db.scalars(
            select(Course)
            .where(Course.id.in_(course_ids), Course.is_published.is_(True))
            .order_by(Course.order, Course.id)
        ).all()
    else:
        courses = db.scalars(
            select(Course)
            .where(Course.category == exam.category, Course.is_published.is_(True))
            .order_by(Course.order, Course.id)
            .limit(6)
        ).all()
    return {
        **exam_brief(exam),
        "quizzes": [
            {
                **quiz_summary(quiz),
                "topic": {"id": quiz.topic.id, "title": quiz.topic.title} if quiz.topic else None,
            }
            for quiz in quizzes
        ],
        "courses": [course_brief(course) for course in courses],
    }
