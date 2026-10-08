import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from pathlib import Path

for _path in (Path("test.db"), Path(__file__).resolve().parent.parent / "test.db"):
    if _path.exists():
        _path.unlink()

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session


def _seed(session: Session) -> None:
    from app.models import Course, Job, Lesson, Question, Quiz, Topic
    from app.services import achievements

    achievements.ensure_defaults(session)

    existing = session.scalar(select(Course).where(Course.slug == "quantitative-aptitude"))
    if existing is None:
        course = Course(
            title="Quantitative Aptitude",
            slug="quantitative-aptitude",
            category="government",
            description="Maths fundamentals for government exams",
            icon="calculator",
            level="Beginner",
            order=1,
            is_published=True,
        )
        session.add(course)
        session.flush()

        topic = Topic(
            course_id=course.id,
            title="Percentage",
            slug="percentage",
            description="Learn percentage calculations",
            order=1,
        )
        session.add(topic)
        session.flush()

        session.add(
            Lesson(
                topic_id=topic.id,
                title="Percentage Basics",
                order=1,
                content={
                    "notes": "A percent is a fraction of 100.",
                    "examples": ["20% of 50 = 10"],
                    "practice": ["Find 15% of 200"],
                },
            )
        )

        quiz_specs = [
            ("beginner", "Percentage Beginner Quiz", "percentage-basics", 10),
            ("intermediate", "Percentage Intermediate Quiz", "percentage-intermediate", 15),
            ("advanced", "Percentage Advanced Quiz", "percentage-advanced", 20),
        ]
        texts = [
            "What is 10% of 200?",
            "If a price rises from 50 to 60, the rise is what percent?",
            "What is 25% of 80?",
            "A number decreased by 20% gives 40. The number is?",
            "What is 15% of 300?",
        ]
        for difficulty, title, slug, minutes in quiz_specs:
            quiz = Quiz(
                title=title,
                slug=slug,
                quiz_type="topic",
                topic_id=topic.id,
                difficulty=difficulty,
                duration_minutes=minutes,
                negative_marks=0,
                total_questions=5,
                is_published=True,
                meta={"year": 2024, "exam": "SSC CGL"},
            )
            session.add(quiz)
            session.flush()
            for index, text in enumerate(texts):
                session.add(
                    Question(
                        quiz_id=quiz.id,
                        question_text=text,
                        options=[f"Option {i}" for i in range(4)],
                        correct_index=index % 4,
                        explanation=f"Explanation for question {index + 1}",
                        difficulty=difficulty,
                        order=index,
                        tags=["Percentage"],
                    )
                )

    if session.scalar(select(Job).where(Job.title == "SSC CGL Notification 2026")) is None:
        session.add(
            Job(
                title="SSC CGL Notification 2026",
                company="Staff Selection Commission",
                type="government",
                category="notification",
                description="Combined Graduate Level Examination 2026 vacancies",
                location="All India",
                salary="Level 4-8",
                apply_link="https://ssc.gov.in",
                source="ssc",
            )
        )
        session.add(
            Job(
                title="Python Intern",
                company="Acme Technologies",
                type="it",
                category="internship",
                description="Paid python internship for freshers",
                location="Remote",
                salary="₹20,000/month",
                apply_link="https://acme.example.com/careers",
                source="acme",
            )
        )
    session.commit()


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def db():
    from app.core.database import SessionLocal, Base, engine

    Base.metadata.create_all(engine)
    session = SessionLocal()
    _seed(session)
    yield session
    session.close()


@pytest.fixture(scope="session")
def auth_headers(client):
    token = client.post(
        "/api/auth/register",
        json={
            "full_name": "Quiz Runner",
            "email": "quiz.runner@example.com",
            "password": "Password123",
        },
    )
    assert token.status_code == 200, token.text
    return {"Authorization": f"Bearer {token.json()['access_token']}"}
