from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Question, Quiz, QuizAttempt, User, XpEvent
from app.services import achievements
from app.services.profiles import apply_daily_streak, award_xp, get_or_create_profile

DIFFICULTY_MULTIPLIERS: dict[str, float] = {"beginner": 1.0, "intermediate": 1.5, "advanced": 2.0}


def load_questions(db: Session, quiz_id: int) -> list[Question]:
    stmt = (
        select(Question)
        .where(Question.quiz_id == quiz_id)
        .order_by(Question.order, Question.id)
    )
    return list(db.scalars(stmt).all())


def topic_name(question: Question, quiz: Quiz) -> str:
    if question.tags:
        return str(question.tags[0])
    if quiz.topic is not None:
        return quiz.topic.title
    return quiz.title


def _build_topic_analysis(quiz: Quiz, questions: list[Question], verdicts: dict[int, bool | None]) -> dict[str, Any]:
    groups: dict[str, dict[str, Any]] = {}
    for question in questions:
        name = topic_name(question, quiz)
        group = groups.setdefault(name, {"name": name, "total": 0, "correct": 0})
        group["total"] += 1
        if verdicts.get(question.id):
            group["correct"] += 1

    breakdown: list[dict[str, Any]] = []
    for group in groups.values():
        accuracy = (group["correct"] / group["total"] * 100) if group["total"] else 0.0
        breakdown.append(
            {
                "name": group["name"],
                "total": group["total"],
                "correct": group["correct"],
                "accuracy": round(accuracy, 2),
            }
        )

    weak = [
        {"topic": entry["name"], "accuracy": entry["accuracy"]}
        for entry in sorted(breakdown, key=lambda e: e["accuracy"])
        if entry["accuracy"] < 60
    ]
    strong = [
        {"topic": entry["name"], "accuracy": entry["accuracy"]}
        for entry in sorted(breakdown, key=lambda e: -e["accuracy"])
        if entry["accuracy"] >= 80
    ]

    suggestions: list[str] = []
    for entry in weak:
        suggestions.append(
            f"Revise '{entry['topic']}' — {entry['accuracy']:.0f}% accuracy. Focus on formula application."
        )

    wrong_topics: list[str] = []
    skipped = 0
    wrong = 0
    for question in questions:
        verdict = verdicts.get(question.id)
        if verdict is None:
            skipped += 1
        elif verdict is False:
            wrong += 1
            name = topic_name(question, quiz)
            if name not in wrong_topics:
                wrong_topics.append(name)

    if wrong_topics:
        shown = ", ".join(f"'{name}'" for name in wrong_topics[:4])
        suggestions.append(f"Review the explanations for {shown} before your next attempt.")
    if skipped:
        suggestions.append(
            f"{skipped} question(s) were skipped — allocate a fixed time per question."
        )
    if not suggestions and breakdown:
        best = max(breakdown, key=lambda e: e["accuracy"])
        suggestions.append(
            f"Strongest area is '{best['name']}' at {best['accuracy']:.0f}% — try advanced sets to keep the edge."
        )
    if not suggestions:
        suggestions.append("Complete a full timed attempt to unlock personalised suggestions.")

    return {
        "weak_areas": weak,
        "strong_areas": strong,
        "topic_breakdown": breakdown,
        "suggestions": suggestions,
    }


def _build_section_analysis(
    quiz: Quiz, questions: list[Question], verdicts: dict[int, bool | None]
) -> tuple[list[dict[str, Any]], list[str]]:
    if not quiz.sections:
        return [], []

    rows: list[dict[str, Any]] = []
    index = 0
    for section in quiz.sections:
        name = str(section.get("name", "Section"))
        try:
            count = int(section.get("question_count", 0) or 0)
        except (TypeError, ValueError):
            count = 0
        chunk = questions[index : index + count] if count > 0 else []
        index += count
        attempted = sum(1 for q in chunk if verdicts.get(q.id) is not None)
        correct = sum(1 for q in chunk if verdicts.get(q.id))
        accuracy = (correct / len(chunk) * 100) if chunk else 0.0
        rows.append(
            {
                "name": name,
                "attempted": attempted,
                "correct": correct,
                "accuracy": round(accuracy, 2),
            }
        )

    suggestions: list[str] = []
    for row in sorted(rows, key=lambda r: r["accuracy"])[:3]:
        if row["accuracy"] < 70:
            suggestions.append(
                f"Section '{row['name']}' needs focus — {row['accuracy']:.0f}% accuracy. Allocate extra revision time."
            )

    wrong_topics: list[str] = []
    for question in questions:
        if verdicts.get(question.id) is False:
            name = topic_name(question, quiz)
            if name not in wrong_topics:
                wrong_topics.append(name)
    for name in wrong_topics[:3]:
        suggestions.append(f"Revisit '{name}' questions — incorrect answers in this mock test.")

    if not suggestions:
        suggestions.append("All sections are balanced — maintain speed with full-length timed mocks.")
    return rows, suggestions


def _dense_rank(db: Session, attempt: QuizAttempt) -> int:
    stmt = (
        select(QuizAttempt)
        .where(QuizAttempt.quiz_id == attempt.quiz_id)
        .order_by(QuizAttempt.score.desc(), QuizAttempt.time_taken_seconds.asc(), QuizAttempt.id.asc())
    )
    rank = 0
    previous_score: float | None = None
    for row in db.scalars(stmt).all():
        if previous_score is None or row.score != previous_score:
            rank += 1
            previous_score = row.score
        if row.id == attempt.id:
            return rank
    return 1


def attempt_payload(attempt: QuizAttempt) -> dict[str, Any]:
    return {
        "id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "mode": attempt.mode,
        "score": float(attempt.score or 0),
        "total": attempt.total,
        "correct": attempt.correct,
        "wrong": attempt.wrong,
        "skipped": attempt.skipped,
        "accuracy": round(float(attempt.accuracy or 0), 2),
        "time_taken_seconds": attempt.time_taken_seconds,
        "rank": attempt.rank,
        "xp_awarded": attempt.xp_awarded,
        "created_at": attempt.created_at,
    }


def build_report(db: Session, attempt: QuizAttempt) -> dict[str, Any]:
    quiz = db.get(Quiz, attempt.quiz_id)
    questions = load_questions(db, attempt.quiz_id)
    answers = {str(key): value for key, value in (attempt.answers or {}).items()}
    analysis = attempt.analysis or {}

    report_questions: list[dict[str, Any]] = []
    for question in questions:
        raw = answers.get(str(question.id))
        try:
            your_answer = int(raw) if raw is not None else None
        except (TypeError, ValueError):
            your_answer = None
        report_questions.append(
            {
                "id": question.id,
                "question_text": question.question_text,
                "options": list(question.options or []),
                "your_answer": your_answer,
                "correct_index": question.correct_index,
                "explanation": question.explanation or "",
                "is_correct": your_answer is not None and your_answer == question.correct_index,
            }
        )

    report: dict[str, Any] = {
        "weak_areas": analysis.get("weak_areas", []),
        "strong_areas": analysis.get("strong_areas", []),
        "topic_breakdown": analysis.get("topic_breakdown", []),
        "suggestions": analysis.get("suggestions", []),
        "questions": report_questions,
    }
    if quiz is not None and quiz.sections:
        report["section_analysis"] = analysis.get("section_analysis", [])
        report["improvement_suggestions"] = analysis.get("improvement_suggestions", [])
    return report


def submit_attempt(
    db: Session,
    user: User,
    quiz: Quiz,
    answers: dict[int, int],
    time_taken_seconds: int,
    mode: str,
) -> dict[str, Any]:
    questions = load_questions(db, quiz.id)

    verdicts: dict[int, bool | None] = {}
    correct = wrong = skipped = 0
    normalized_answers: dict[int, int] = {}
    for question in questions:
        if question.id not in answers:
            verdicts[question.id] = None
            skipped += 1
            continue
        try:
            chosen = int(answers[question.id])
        except (TypeError, ValueError):
            verdicts[question.id] = None
            skipped += 1
            continue
        normalized_answers[question.id] = chosen
        options = question.options or []
        valid = 0 <= chosen < len(options) and chosen == question.correct_index
        verdicts[question.id] = valid
        if valid:
            correct += 1
        else:
            wrong += 1

    total = len(questions)
    negative_marks = float(quiz.negative_marks or 0)
    if mode == "exam" and negative_marks > 0:
        score = correct - wrong * negative_marks
    else:
        score = float(correct)
    accuracy = round(correct / total * 100, 2) if total else 0.0

    analysis = _build_topic_analysis(quiz, questions, verdicts)
    if quiz.sections:
        section_rows, improvement = _build_section_analysis(quiz, questions, verdicts)
        analysis["section_analysis"] = section_rows
        analysis["improvement_suggestions"] = improvement

    attempt = QuizAttempt(
        user_id=user.id,
        quiz_id=quiz.id,
        mode=mode,
        answers={str(key): int(value) for key, value in normalized_answers.items()},
        score=score,
        total=total,
        correct=correct,
        wrong=wrong,
        skipped=skipped,
        accuracy=accuracy,
        time_taken_seconds=int(time_taken_seconds),
        xp_awarded=0,
        analysis=analysis,
    )
    db.add(attempt)
    db.flush()

    attempt.rank = _dense_rank(db, attempt)

    multiplier = DIFFICULTY_MULTIPLIERS.get(quiz.difficulty, 1.0)
    xp_awarded = round(correct * 10 * multiplier)
    profile = get_or_create_profile(db, user)
    award_xp(profile, xp_awarded)
    apply_daily_streak(profile)
    attempt.xp_awarded = xp_awarded
    db.add(
        XpEvent(
            user_id=user.id,
            points=xp_awarded,
            kind="mock" if quiz.quiz_type == "mock" else "quiz",
            ref_id=attempt.id,
        )
    )
    db.flush()

    total_quizzes = (
        db.scalar(
            select(func.count(QuizAttempt.id)).where(QuizAttempt.user_id == user.id)
        )
        or 0
    )
    unlocked = achievements.evaluate(
        db,
        user,
        {
            "attempt": attempt_payload(attempt),
            "quiz": quiz,
            "accuracy": accuracy,
            "profile": profile,
            "total_quizzes": total_quizzes,
        },
    )
    profile.level = (profile.xp or 0) // 500 + 1
    db.commit()
    db.refresh(attempt)

    return {
        "attempt": attempt_payload(attempt),
        "report": build_report(db, attempt),
        "achievements_unlocked": unlocked,
    }
