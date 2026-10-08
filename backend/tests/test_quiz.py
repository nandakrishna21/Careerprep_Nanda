from sqlalchemy import select

from app.models import Question, Quiz, QuizAttempt


def _topic_payload(client, slug="percentage"):
    res = client.get(f"/api/topics/{slug}")
    assert res.status_code == 200, res.text
    return res.json()


def test_courses_listing(client, db):
    res = client.get("/api/courses?category=government")
    assert res.status_code == 200
    courses = res.json()
    assert isinstance(courses, list)
    slugs = {c["slug"] for c in courses}
    assert "quantitative-aptitude" in slugs


def test_course_detail_has_topics(client, db):
    res = client.get("/api/courses/quantitative-aptitude")
    assert res.status_code == 200
    body = res.json()
    assert len(body["topics"]) >= 1
    assert any(t["slug"] == "percentage" for t in body["topics"])


def test_topic_detail_lessons_and_quizzes(client, db):
    body = _topic_payload(client)
    assert body["lessons"], "topic should have lessons"
    assert len(body["quizzes"]) >= 3
    difficulties = {q["difficulty"] for q in body["quizzes"]}
    assert {"beginner", "intermediate", "advanced"} <= difficulties


def test_quiz_meta_hides_answers(client, db):
    topic = _topic_payload(client)
    quiz_id = topic["quizzes"][0]["id"]

    meta = client.get(f"/api/quizzes/{quiz_id}").json()
    assert "questions" not in meta
    assert meta["duration_minutes"] > 0

    questions = client.get(f"/api/quizzes/{quiz_id}/questions").json()
    assert questions
    for q in questions:
        assert "correct_index" not in q
        assert "explanation" not in q
        assert len(q["options"]) >= 2


def test_attempt_flow_full_report(client, db, auth_headers):
    topic = _topic_payload(client)
    quiz_id = next(q["id"] for q in topic["quizzes"] if q["difficulty"] == "beginner")

    questions = client.get(f"/api/quizzes/{quiz_id}/questions").json()
    db_questions = db.scalars(select(Question).where(Question.quiz_id == quiz_id)).all()
    correct_by_id = {q.id: q.correct_index for q in db_questions}

    answers = {str(q["id"]): correct_by_id[q["id"]] for q in questions}

    res = client.post(
        f"/api/quizzes/{quiz_id}/attempt",
        json={"answers": answers, "time_taken_seconds": 120, "mode": "practice"},
        headers=auth_headers,
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert set(body) >= {"attempt", "report", "achievements_unlocked"}

    attempt = body["attempt"]
    assert attempt["total"] == len(questions)
    assert attempt["correct"] == len(questions)
    assert attempt["wrong"] == 0
    assert attempt["accuracy"] == 100
    assert isinstance(attempt["rank"], int)
    assert attempt["xp_awarded"] > 0

    report = body["report"]
    assert "weak_areas" in report
    assert "strong_areas" in report
    assert "topic_breakdown" in report
    assert len(report["questions"]) == len(questions)
    for review in report["questions"]:
        assert review["is_correct"] is True
        assert review["explanation"]
        assert review["correct_index"] >= 0

    unlocked_codes = {a["code"] for a in body["achievements_unlocked"]}
    assert "first_quiz" in unlocked_codes


def test_attempts_history(client, auth_headers):
    res = client.get("/api/attempts/mine", headers=auth_headers)
    assert res.status_code == 200
    attempts = res.json()
    assert attempts
    assert "quiz_title" in attempts[0]

    attempt_id = attempts[0]["id"]
    detail = client.get(f"/api/attempts/{attempt_id}", headers=auth_headers)
    assert detail.status_code == 200
    assert "report" in detail.json()
    assert "questions" in detail.json()["report"]


def test_wrong_answers_score(client, db, auth_headers):
    quiz = db.scalar(select(Quiz).where(Quiz.slug == "percentage-basics"))
    assert quiz is not None
    questions = db.scalars(select(Question).where(Question.quiz_id == quiz.id)).all()

    wrong = 0
    answers = {}
    for q in questions:
        bad = (q.correct_index + 1) % len(q.options)
        answers[str(q.id)] = bad
        wrong += 1

    res = client.post(
        f"/api/quizzes/{quiz.id}/attempt",
        json={"answers": answers, "time_taken_seconds": 60, "mode": "practice"},
        headers=auth_headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["attempt"]["correct"] == 0
    assert body["attempt"]["wrong"] == wrong
    assert body["attempt"]["accuracy"] == 0
    assert body["report"]["weak_areas"], "all-wrong attempt must surface weak areas"

    stored = db.get(QuizAttempt, body["attempt"]["id"])
    assert stored is not None
