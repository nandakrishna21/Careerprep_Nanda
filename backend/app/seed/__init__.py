"""Idempotent database seeder: `python -m app.seed` from the backend directory."""
from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models import (
    Course,
    CurrentAffair,
    Exam,
    Job,
    Lesson,
    MockTest,
    Profile,
    Question,
    Quiz,
    QuizAttempt,
    Topic,
    User,
)
from app.seed import extras, gov, it
from app.seed.it_paths import CAREER_PATHS
from app.services import achievements, scoring

DIFFICULTIES = ("beginner", "intermediate", "advanced")

TRACKED_MODELS = {
    "courses": Course,
    "topics": Topic,
    "lessons": Lesson,
    "quizzes": Quiz,
    "questions": Question,
    "exams": Exam,
    "mock_tests": MockTest,
    "current_affairs": CurrentAffair,
    "jobs": Job,
    "users": User,
    "attempts": QuizAttempt,
}


def _table_counts(db: Session) -> dict[str, int]:
    return {name: int(db.scalar(select(func.count(model.id))) or 0) for name, model in TRACKED_MODELS.items()}


def _existing_slug(db: Session, model: type, slug: str):
    return db.scalar(select(model).where(model.slug == slug))


def _ensure_admin(db: Session) -> None:
    admin_email = settings.admin_email.strip().lower()
    found = db.scalar(select(User).where(func.lower(User.email) == admin_email))
    if found is not None:
        return
    admin = User(
        email=admin_email,
        hashed_password=hash_password(settings.admin_password),
        full_name="Administrator",
        role="admin",
        is_active=True,
    )
    db.add(admin)
    db.flush()
    db.add(Profile(user_id=admin.id, headline="Platform Administrator"))


def _ensure_demo_student(db: Session) -> User:
    spec = extras.DEMO_STUDENT
    found = db.scalar(select(User).where(User.email == spec["email"]))
    if found is not None:
        return found
    user = User(
        email=spec["email"],
        hashed_password=hash_password(spec["password"]),
        full_name=spec["full_name"],
        role="student",
        is_active=True,
    )
    db.add(user)
    db.flush()
    db.add(
        Profile(
            user_id=user.id,
            headline=spec["headline"],
            education=spec["education"],
            skills=spec["skills"],
            target_exams=spec["target_exams"],
        )
    )
    return user


def _create_quiz(
    db: Session,
    *,
    title: str,
    slug: str,
    quiz_type: str,
    questions: list[dict[str, Any]],
    difficulty: str,
    duration_minutes: int,
    negative_marks: float,
    default_tags: list[str],
    topic_id: int | None = None,
    exam_id: int | None = None,
    current_affair_id: int | None = None,
    sections: list[dict] | None = None,
    meta: dict | None = None,
) -> Quiz:
    existing = _existing_slug(db, Quiz, slug)
    if existing is not None:
        return existing
    quiz = Quiz(
        title=title,
        slug=slug,
        quiz_type=quiz_type,
        topic_id=topic_id,
        exam_id=exam_id,
        current_affair_id=current_affair_id,
        difficulty=difficulty,
        duration_minutes=duration_minutes,
        negative_marks=negative_marks,
        sections=sections,
        total_questions=len(questions),
        is_published=True,
        meta=meta or {},
    )
    db.add(quiz)
    db.flush()
    for order, item in enumerate(questions):
        db.add(
            Question(
                quiz_id=quiz.id,
                question_text=item["question_text"],
                options=list(item["options"]),
                correct_index=int(item["correct_index"]),
                explanation=item.get("explanation", ""),
                difficulty=item.get("difficulty", difficulty),
                order=order,
                tags=list(item.get("tags") or default_tags),
            )
        )
    db.flush()
    return quiz


def _seed_lesson(db: Session, topic: Topic, lesson_spec: dict) -> None:
    has_lesson = db.scalar(select(Lesson.id).where(Lesson.topic_id == topic.id))
    if has_lesson is not None:
        return
    content: dict[str, Any] = {
        "notes": lesson_spec["notes"],
        "examples": list(lesson_spec.get("examples", [])),
        "practice": list(lesson_spec.get("practice", [])),
    }
    if lesson_spec.get("code"):
        content["code"] = lesson_spec["code"]
    db.add(Lesson(topic_id=topic.id, title=lesson_spec["title"], order=1, content=content))


def _seed_courses(db: Session) -> None:
    for spec in gov.GOV_COURSES:
        course = _existing_slug(db, Course, spec["slug"])
        if course is None:
            course = Course(
                title=spec["title"],
                slug=spec["slug"],
                category="government",
                description=spec["description"],
                icon=spec["icon"],
                level=spec["level"],
                order=spec.get("order", 0),
                is_published=True,
                career_path=False,
            )
            db.add(course)
            db.flush()
        for order, (slug, title, description) in enumerate(spec["topics"], start=1):
            topic = _existing_slug(db, Topic, slug)
            if topic is None:
                topic = Topic(course_id=course.id, title=title, slug=slug, description=description, order=order)
                db.add(topic)
                db.flush()
            _seed_lesson(db, topic, gov.LESSONS[slug])
            for difficulty in DIFFICULTIES:
                questions = gov.questions_for(slug, difficulty)
                _create_quiz(
                    db,
                    title=f"{title} — {difficulty.title()}",
                    slug=f"{slug}-{difficulty}",
                    quiz_type="topic",
                    questions=questions,
                    difficulty=difficulty,
                    duration_minutes=max(10, len(questions)),
                    negative_marks=0.25,
                    default_tags=[title],
                    topic_id=topic.id,
                )

    for order, spec in enumerate(it.IT_COURSES, start=1):
        course = _existing_slug(db, Course, spec["slug"])
        if course is None:
            course = Course(
                title=spec["title"],
                slug=spec["slug"],
                category="it",
                description=spec["description"],
                icon=spec["icon"],
                level=spec["level"],
                order=order,
                is_published=True,
                career_path=False,
            )
            db.add(course)
            db.flush()
        for topic_order, (slug, title, difficulty, description) in enumerate(spec["topics"], start=1):
            topic = _existing_slug(db, Topic, slug)
            if topic is None:
                topic = Topic(course_id=course.id, title=title, slug=slug, description=description, order=topic_order)
                db.add(topic)
                db.flush()
            _seed_lesson(db, topic, it.IT_LESSONS[slug])
            questions = it.questions_for(slug, difficulty)
            _create_quiz(
                db,
                title=f"{title} Quiz",
                slug=slug,
                quiz_type="topic",
                questions=questions,
                difficulty=difficulty,
                duration_minutes=max(10, len(questions)),
                negative_marks=0,
                default_tags=[title],
                topic_id=topic.id,
            )

    for path_index, path in enumerate(CAREER_PATHS):
        course = _existing_slug(db, Course, path["slug"])
        if course is None:
            course = Course(
                title=path["title"],
                slug=path["slug"],
                category="it",
                description=path["description"],
                icon=path["icon"],
                level=path["level"],
                order=6 + path_index,
                is_published=True,
                career_path=True,
            )
            db.add(course)
            db.flush()
        for topic_order, spec in enumerate(path["topics"], start=1):
            topic = _existing_slug(db, Topic, spec["slug"])
            if topic is None:
                topic = Topic(
                    course_id=course.id,
                    title=spec["title"],
                    slug=spec["slug"],
                    description=spec["description"],
                    order=topic_order,
                )
                db.add(topic)
                db.flush()
            _seed_lesson(db, topic, spec["lesson"])
            _create_quiz(
                db,
                title=f"{spec['title']} Quiz",
                slug=spec["slug"],
                quiz_type="topic",
                questions=it.career_questions(spec["slug"], limit=10),
                difficulty="intermediate",
                duration_minutes=15,
                negative_marks=0,
                default_tags=[spec["title"]],
                topic_id=topic.id,
            )


def _seed_exams(db: Session) -> dict[str, int]:
    ids: dict[str, int] = {}
    for spec in extras.EXAMS:
        exam = _existing_slug(db, Exam, spec["slug"])
        if exam is None:
            exam = Exam(
                name=spec["name"],
                slug=spec["slug"],
                category=spec["category"],
                description=spec["description"],
                pattern=spec["pattern"],
                is_published=True,
            )
            db.add(exam)
            db.flush()
        ids[spec["slug"]] = exam.id
    return ids


def _seed_pyqs(db: Session, exam_ids: dict[str, int]) -> None:
    for spec in extras.PYQ_SPECS:
        topic = _existing_slug(db, Topic, spec["topic_slug"])
        if topic is None:
            continue
        questions = extras.build_pyq_questions(spec)
        _create_quiz(
            db,
            title=spec["title"],
            slug=spec["slug"],
            quiz_type="pyq",
            questions=questions,
            difficulty="intermediate",
            duration_minutes=20,
            negative_marks=0.25,
            default_tags=[topic.title],
            topic_id=topic.id,
            exam_id=exam_ids[spec["exam_slug"]],
            meta={"year": spec["year"], "exam": spec["exam_slug"]},
        )


def _seed_current_affairs(db: Session) -> None:
    for spec in extras.CURRENT_AFFAIRS:
        row = _existing_slug(db, CurrentAffair, spec["slug"])
        if row is None:
            row = CurrentAffair(
                title=spec["title"],
                slug=spec["slug"],
                period=spec["period"],
                date=spec["date"],
                summary=spec["summary"],
                content=spec["content"],
                ai_content=dict(spec["ai_content"]),
                is_published=True,
            )
            db.add(row)
            db.flush()
        ai_content = dict(row.ai_content or {})
        if not ai_content.get("quiz_id") and ai_content.get("mcqs"):
            questions = [
                {
                    "question_text": item["question"],
                    "options": list(item["options"]),
                    "correct_index": int(item["correct_index"]),
                    "explanation": item.get("explanation", ""),
                    "difficulty": "intermediate",
                    "tags": ["Current Affairs"],
                }
                for item in ai_content["mcqs"]
            ]
            quiz = _create_quiz(
                db,
                title=f"Quiz — {spec['title']}",
                slug=f"ca-{spec['slug']}",
                quiz_type="current_affair",
                questions=questions,
                difficulty="intermediate",
                duration_minutes=max(5, len(questions) * 2),
                negative_marks=0,
                default_tags=["Current Affairs"],
                current_affair_id=row.id,
                meta={"period": spec["period"]},
            )
            ai_content["quiz_id"] = quiz.id
            row.ai_content = ai_content


def _seed_mocks(db: Session) -> None:
    for spec in extras.MOCK_SPECS:
        if _existing_slug(db, MockTest, spec["slug"]) is not None:
            continue
        sections, questions = extras.build_mock_sections(spec)
        quiz = _create_quiz(
            db,
            title=spec["title"],
            slug=f"quiz-{spec['slug']}",
            quiz_type="mock",
            questions=questions,
            difficulty="intermediate",
            duration_minutes=spec["duration_minutes"],
            negative_marks=0.25,
            default_tags=["Mock Test"],
            sections=sections,
            meta={"category": spec["category"]},
        )
        db.add(
            MockTest(
                title=spec["title"],
                slug=spec["slug"],
                category=spec["category"],
                description=spec["description"],
                duration_minutes=spec["duration_minutes"],
                total_questions=spec["total_questions"],
                negative_marks=0.25,
                sections=sections,
                exam_pattern={
                    "mode": "Online",
                    "medium": "English / Hindi",
                    "marks_per_question": spec["marks_per_question"],
                    "negative_marks": 0.25,
                    "duration_minutes": spec["duration_minutes"],
                    "total_marks": spec["total_questions"] * spec["marks_per_question"],
                },
                is_published=True,
                quiz_id=quiz.id,
            )
        )
    for spec in extras.IT_MOCK_SPECS:
        if _existing_slug(db, MockTest, spec["slug"]) is not None:
            continue
        sections, questions = extras.build_it_mock_sections(spec)
        total = sum(s["question_count"] for s in sections)
        quiz = _create_quiz(
            db,
            title=spec["title"],
            slug=f"quiz-{spec['slug']}",
            quiz_type="mock",
            questions=questions,
            difficulty="intermediate",
            duration_minutes=spec["duration_minutes"],
            negative_marks=0,
            default_tags=["IT Mock Test"],
            sections=sections,
            meta={"category": "it"},
        )
        db.add(
            MockTest(
                title=spec["title"],
                slug=spec["slug"],
                category="it",
                description=spec["description"],
                duration_minutes=spec["duration_minutes"],
                total_questions=total,
                negative_marks=0,
                sections=sections,
                exam_pattern={
                    "mode": "Online",
                    "medium": "English",
                    "marks_per_question": 1,
                    "negative_marks": 0,
                    "duration_minutes": spec["duration_minutes"],
                    "total_marks": total,
                },
                is_published=True,
                quiz_id=quiz.id,
            )
        )


def _seed_jobs(db: Session) -> None:
    for spec in extras.JOBS:
        exists = db.scalar(select(Job.id).where(Job.title == spec["title"], Job.company == spec["company"]))
        if exists is not None:
            continue
        db.add(Job(**spec, is_published=True))


def _seed_demo_attempts(db: Session, user: User) -> None:
    existing = db.scalar(select(func.count(QuizAttempt.id)).where(QuizAttempt.user_id == user.id))
    if int(existing or 0) > 0:
        return
    plan = [
        ("percentage-beginner", "practice", 12_600),
        ("coding-decoding-intermediate", "practice", 9_400),
        ("python-basics", "practice", 7_200),
        ("quiz-ssc-cgl-mock-1", "exam", 3_300),
    ]
    for slug, mode, seconds in plan:
        quiz = _existing_slug(db, Quiz, slug)
        if quiz is None:
            continue
        answers: dict[int, int] = {}
        for index, question in enumerate(scoring.load_questions(db, quiz.id)):
            if index % 6 == 5:
                continue
            answers[question.id] = (question.correct_index + 1) % 4 if index % 8 == 3 else question.correct_index
        scoring.submit_attempt(db, user, quiz, answers, seconds, mode)


def run(db: Session) -> dict[str, int]:
    before = _table_counts(db)
    achievements.ensure_defaults(db)
    _ensure_admin(db)
    student = _ensure_demo_student(db)
    _seed_courses(db)
    exam_ids = _seed_exams(db)
    _seed_pyqs(db, exam_ids)
    _seed_current_affairs(db)
    _seed_mocks(db)
    _seed_jobs(db)
    _seed_demo_attempts(db, student)
    db.commit()
    after = _table_counts(db)
    return {name: after[name] - before[name] for name in after}
