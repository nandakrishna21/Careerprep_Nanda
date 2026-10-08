from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func, or_, select

from app.core.security import DbSession
from app.models import Course, CurrentAffair, Job, Lesson, MockTest, Quiz, Topic

router = APIRouter(tags=["search"])

_LIMIT = 5


def func_lower_contains(column, term: str):
    return func.lower(column).contains(term)


def _item(type_: str, title: str, subtitle: str, url: str) -> dict:
    return {"type": type_, "title": title, "subtitle": subtitle or "", "url": url}


def _needle(q: str) -> str:
    return q.strip().lower()


@router.get("/search")
def search(q: str, db: DbSession) -> dict:
    term = _needle(q)
    if not term:
        return {
            "courses": [],
            "topics": [],
            "lessons": [],
            "quizzes": [],
            "mock_tests": [],
            "jobs": [],
            "current_affairs": [],
        }

    courses = db.scalars(
        select(Course)
        .where(
            Course.is_published.is_(True),
            or_(
                func_lower_contains(Course.title, term),
                func_lower_contains(Course.description, term),
            ),
        )
        .order_by(Course.id)
        .limit(_LIMIT)
    ).all()

    topics = db.scalars(
        select(Topic)
        .where(
            or_(
                func_lower_contains(Topic.title, term),
                func_lower_contains(Topic.description, term),
            )
        )
        .order_by(Topic.id)
        .limit(_LIMIT)
    ).all()

    lessons = db.scalars(
        select(Lesson).where(func_lower_contains(Lesson.title, term)).order_by(Lesson.id).limit(_LIMIT)
    ).all()

    quizzes = db.scalars(
        select(Quiz)
        .where(
            Quiz.is_published.is_(True),
            Quiz.quiz_type != "mock",
            func_lower_contains(Quiz.title, term),
        )
        .order_by(Quiz.id)
        .limit(_LIMIT)
    ).all()

    mock_tests = db.scalars(
        select(MockTest)
        .where(
            MockTest.is_published.is_(True),
            or_(
                func_lower_contains(MockTest.title, term),
                func_lower_contains(MockTest.description, term),
            ),
        )
        .order_by(MockTest.id)
        .limit(_LIMIT)
    ).all()

    jobs = db.scalars(
        select(Job)
        .where(
            Job.is_published.is_(True),
            or_(
                func_lower_contains(Job.title, term),
                func_lower_contains(Job.company, term),
                func_lower_contains(Job.description, term),
            ),
        )
        .order_by(Job.id)
        .limit(_LIMIT)
    ).all()

    affairs = db.scalars(
        select(CurrentAffair)
        .where(
            CurrentAffair.is_published.is_(True),
            or_(
                func_lower_contains(CurrentAffair.title, term),
                func_lower_contains(CurrentAffair.summary, term),
                func_lower_contains(CurrentAffair.content, term),
            ),
        )
        .order_by(CurrentAffair.date.desc())
        .limit(_LIMIT)
    ).all()

    course_items = []
    for course in courses:
        if course.category == "it":
            url = f"/it/path/{course.slug}" if course.career_path else f"/it/learn/{course.slug}"
        else:
            url = "/gov"
        course_items.append(_item("course", course.title, course.category, url))

    topic_items = []
    lesson_items = []
    for topic in topics:
        course = topic.course
        if course is not None and course.category == "it":
            url = f"/it/learn/{course.slug}"
        else:
            url = f"/gov/topic/{topic.slug}"
        topic_items.append(_item("topic", topic.title, course.title if course else "", url))
    for lesson in lessons:
        topic = lesson.topic
        course = topic.course if topic is not None else None
        if course is not None and course.category == "it":
            url = f"/it/learn/{course.slug}"
        else:
            url = f"/gov/topic/{topic.slug}" if topic is not None else "/gov"
        lesson_items.append(
            _item("lesson", lesson.title, topic.title if topic else "", url)
        )

    quiz_items = []
    for quiz in quizzes:
        if quiz.quiz_type == "pyq":
            url = "/gov/pyqs"
        elif quiz.topic is not None and quiz.topic.course is not None:
            if quiz.topic.course.category == "it":
                url = f"/it/quizzes/{quiz.id}"
            else:
                url = f"/gov/quizzes/{quiz.id}"
        else:
            url = f"/gov/quizzes/{quiz.id}"
        subtitle = quiz.meta.get("exam") if isinstance(quiz.meta, dict) else ""
        quiz_items.append(_item("quiz", quiz.title, str(subtitle or quiz.difficulty), url))

    mock_items = [
        _item("mock_test", test.title, test.category, f"/gov/mock/{test.slug}")
        for test in mock_tests
    ]
    job_items = [_item("job", job.title, job.company or job.type, "/jobs") for job in jobs]
    affair_items = [
        _item("current_affair", row.title, row.period, f"/gov/current-affairs/{row.slug}")
        for row in affairs
    ]

    return {
        "courses": course_items,
        "topics": topic_items,
        "lessons": lesson_items,
        "quizzes": quiz_items,
        "mock_tests": mock_items,
        "jobs": job_items,
        "current_affairs": affair_items,
    }
