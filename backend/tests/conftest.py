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


def _owner_headers(client):
    """Log in as the superadmin, registering first if needed (auto-approved)."""
    from app.core.config import settings

    email = settings.superadmin_email
    reg = client.post(
        "/api/auth/register",
        json={"full_name": "Owner", "email": email, "password": "Secret123"},
    )
    if reg.status_code == 200:
        body = reg.json()
        assert body["approved"] is True
        assert body["access_token"]
        return {"Authorization": f"Bearer {body['access_token']}"}
    assert reg.status_code == 409, reg.text
    login = client.post("/api/auth/login", json={"email": email, "password": "Secret123"})
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def approve_user(client, owner_headers, user_id):
    res = client.patch(
        f"/api/admin/users/{user_id}", json={"is_approved": True}, headers=owner_headers
    )
    assert res.status_code == 200, res.text
    return res.json()


def signup_approve_login(client, email, name="Approved User", password="Secret123"):
    """Full signup funnel: register (pending), approve, log in."""
    owner = _owner_headers(client)
    reg = client.post(
        "/api/auth/register",
        json={"full_name": name, "email": email, "password": password},
    )
    if reg.status_code == 200:
        body = reg.json()
        assert body["approved"] is False
        assert "access_token" not in body
        approve_user(client, owner, body["user_id"])
    else:
        assert reg.status_code == 409, reg.text
    login = client.post("/api/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


@pytest.fixture(scope="session")
def owner_headers(client):
    return _owner_headers(client)


@pytest.fixture(scope="session")
def auth_headers(client):
    return signup_approve_login(client, "quiz.runner@example.com", "Quiz Runner", "Password123")
