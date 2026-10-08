from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import AdminUser, DbSession
from app.models import Course, Lesson, Question, Quiz, Topic
from app.schemas.admin import (
    CourseCreate,
    CourseUpdate,
    LessonCreate,
    LessonUpdate,
    QuestionCreate,
    QuestionUpdate,
    QuizCreate,
    QuizUpdate,
    TopicCreate,
    TopicUpdate,
)
from app.services.common import course_brief, quiz_summary, unique_slug

router = APIRouter(tags=["admin"])


def _page_params(page: int, page_size: int) -> tuple[int, int, int]:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    return page, page_size, (page - 1) * page_size


def _apply(obj, payload) -> None:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.get("/courses")
def admin_list_courses(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, q: str | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Course)
    if q:
        stmt = stmt.where(func.lower(Course.title).contains(q.lower()))
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Course.order, Course.id).offset(offset).limit(page_size)).all()
    items = [{**course_brief(row), "level": row.level, "is_published": row.is_published} for row in rows]
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


@router.post("/courses")
def admin_create_course(payload: CourseCreate, admin: AdminUser, db: DbSession) -> dict:
    slug = unique_slug(db, Course, payload.slug or payload.title)
    course = Course(**payload.model_dump(exclude={"slug"}), slug=slug)
    db.add(course)
    db.commit()
    db.refresh(course)
    return {**course_brief(course), "level": course.level, "is_published": course.is_published}


@router.put("/courses/{id}")
def admin_update_course(id: int, payload: CourseUpdate, admin: AdminUser, db: DbSession) -> dict:
    course = db.get(Course, id)
    if course is None:
        raise _not_found("Course not found")
    data = payload.model_dump(exclude_unset=True)
    if "slug" in data and data["slug"]:
        data["slug"] = unique_slug(db, Course, data["slug"], exclude_id=course.id)
    for field, value in data.items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return {**course_brief(course), "level": course.level, "is_published": course.is_published}


@router.delete("/courses/{id}")
def admin_delete_course(id: int, admin: AdminUser, db: DbSession) -> dict:
    course = db.get(Course, id)
    if course is None:
        raise _not_found("Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}


@router.get("/topics")
def admin_list_topics(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, course_id: int | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Topic)
    if course_id is not None:
        stmt = stmt.where(Topic.course_id == course_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Topic.order, Topic.id).offset(offset).limit(page_size)).all()
    items = [
        {
            "id": row.id,
            "course_id": row.course_id,
            "title": row.title,
            "slug": row.slug,
            "description": row.description or "",
            "order": row.order,
        }
        for row in rows
    ]
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


@router.post("/topics")
def admin_create_topic(payload: TopicCreate, admin: AdminUser, db: DbSession) -> dict:
    if db.get(Course, payload.course_id) is None:
        raise _not_found("Course not found")
    slug = unique_slug(db, Topic, payload.slug or payload.title)
    topic = Topic(**payload.model_dump(exclude={"slug"}), slug=slug)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return {
        "id": topic.id,
        "course_id": topic.course_id,
        "title": topic.title,
        "slug": topic.slug,
        "description": topic.description,
        "order": topic.order,
    }


@router.put("/topics/{id}")
def admin_update_topic(id: int, payload: TopicUpdate, admin: AdminUser, db: DbSession) -> dict:
    topic = db.get(Topic, id)
    if topic is None:
        raise _not_found("Topic not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("course_id") is not None and db.get(Course, data["course_id"]) is None:
        raise _not_found("Course not found")
    if "slug" in data and data["slug"]:
        data["slug"] = unique_slug(db, Topic, data["slug"], exclude_id=topic.id)
    for field, value in data.items():
        setattr(topic, field, value)
    db.commit()
    db.refresh(topic)
    return {
        "id": topic.id,
        "course_id": topic.course_id,
        "title": topic.title,
        "slug": topic.slug,
        "description": topic.description,
        "order": topic.order,
    }


@router.delete("/topics/{id}")
def admin_delete_topic(id: int, admin: AdminUser, db: DbSession) -> dict:
    topic = db.get(Topic, id)
    if topic is None:
        raise _not_found("Topic not found")
    db.delete(topic)
    db.commit()
    return {"message": "Topic deleted"}


@router.get("/lessons")
def admin_list_lessons(
    admin: AdminUser, db: DbSession, page: int = 1, page_size: int = 20, topic_id: int | None = None
) -> dict:
    page, page_size, offset = _page_params(page, page_size)
    stmt = select(Lesson)
    if topic_id is not None:
        stmt = stmt.where(Lesson.topic_id == topic_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.order_by(Lesson.order, Lesson.id).offset(offset).limit(page_size)).all()
    items = [
        {"id": row.id, "topic_id": row.topic_id, "title": row.title, "order": row.order}
        for row in rows
    ]
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


@router.post("/lessons")
def admin_create_lesson(payload: LessonCreate, admin: AdminUser, db: DbSession) -> dict:
    if db.get(Topic, payload.topic_id) is None:
        raise _not_found("Topic not found")
    lesson = Lesson(**payload.model_dump())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return {"id": lesson.id, "topic_id": lesson.topic_id, "title": lesson.title, "order": lesson.order}


@router.put("/lessons/{id}")
def admin_update_lesson(id: int, payload: LessonUpdate, admin: AdminUser, db: DbSession) -> dict:
    lesson = db.get(Lesson, id)
    if lesson is None:
        raise _not_found("Lesson not found")
    data = payload.model_dump(exclude_unset=True)
    if data.get("topic_id") is not None and db.get(Topic, data["topic_id"]) is None:
        raise _not_found("Topic not found")
    for field, value in data.items():
        setattr(lesson, field, value)
    db.commit()
    db.refresh(lesson)
    return {"id": lesson.id, "topic_id": lesson.topic_id, "title": lesson.title, "order": lesson.order}


@router.delete("/lessons/{id}")
def admin_delete_lesson(id: int, admin: AdminUser, db: DbSession) -> dict:
    lesson = db.get(Lesson, id)
    if lesson is None:
        raise _not_found("Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}
