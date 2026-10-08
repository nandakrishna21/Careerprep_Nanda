from __future__ import annotations

from collections import Counter
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from app.core.security import CurrentUser, DbSession
from app.models import InterviewSession, InterviewTurn, Question, Quiz, StudyPlan
from app.schemas.ai import (
    InterviewAnswerRequest,
    InterviewStartRequest,
    QuizGenerateRequest,
    StudyPlanRequest,
)
from app.services import achievements, gemini
from app.services.common import unique_slug

router = APIRouter(tags=["ai"])

_QUESTION_SYSTEM = (
    "You are an expert exam question writer for Indian government exams and IT placements. "
    "You always answer with strict, valid JSON only."
)
_INTERVIEW_SYSTEM = (
    "You are a senior interviewer conducting a mock interview. "
    "You respond with strict, valid JSON only."
)
_PLANNER_SYSTEM = (
    "You are an experienced study coach. You always answer with strict, valid JSON only."
)


def _top_three(groups: list[list[str]]) -> list[str]:
    counts: Counter[str] = Counter()
    display: dict[str, str] = {}
    for group in groups:
        for raw in group or []:
            label = str(raw).strip()
            if not label:
                continue
            key = label.lower()
            counts[key] += 1
            display.setdefault(key, label)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [display[key] for key, _ in ordered[:3]]


def _clamp_score(value: Any) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        score = 5
    return max(1, min(10, score))


def _clean_questions(raw: Any, count: int, difficulty: str) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        raw = raw.get("questions") or raw.get("items") or []
    if not isinstance(raw, list):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    cleaned: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        text = str(item.get("question_text") or item.get("question") or "").strip()
        options = item.get("options")
        if not text or not isinstance(options, list) or len(options) < 4:
            continue
        try:
            correct_index = int(item.get("correct_index", 0))
        except (TypeError, ValueError):
            continue
        correct_index = max(0, min(3, correct_index))
        cleaned.append(
            {
                "question_text": text,
                "options": [str(option) for option in options[:4]],
                "correct_index": correct_index,
                "explanation": str(item.get("explanation") or ""),
                "difficulty": str(item.get("difficulty") or difficulty),
            }
        )
        if len(cleaned) >= count:
            break
    if not cleaned:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    return cleaned


@router.post("/quiz-generate")
def generate_quiz(payload: QuizGenerateRequest, user: CurrentUser, db: DbSession) -> dict:
    count = max(1, min(50, payload.count))
    difficulty = payload.difficulty if payload.difficulty in {"beginner", "intermediate", "advanced"} else "beginner"
    prompt = (
        f"Generate exactly {count} multiple choice questions about \"{payload.topic}\" "
        f"at {difficulty} difficulty for exam preparation.\n"
        "Respond with a strict JSON array (no prose, no markdown) where each element is an object with keys: "
        '"question_text" (string), "options" (array of exactly 4 strings), '
        '"correct_index" (integer 0-3), "explanation" (string), "difficulty" (string).'
    )
    raw = gemini.generate_json(prompt, system=_QUESTION_SYSTEM, temperature=0.8)
    questions = _clean_questions(raw, count, difficulty)

    quiz_id: int | None = None
    if payload.save:
        title = (payload.title or f"AI Quiz — {payload.topic}").strip()
        slug = unique_slug(db, Quiz, title)
        quiz = Quiz(
            title=title,
            slug=slug,
            quiz_type="ai",
            difficulty=difficulty,
            duration_minutes=max(5, len(questions) * 2),
            negative_marks=0,
            total_questions=len(questions),
            is_published=True,
            created_by=user.id,
            meta={"topic": payload.topic, "generated_by": "ai"},
        )
        db.add(quiz)
        db.flush()
        for index, item in enumerate(questions):
            db.add(
                Question(
                    quiz_id=quiz.id,
                    question_text=item["question_text"],
                    options=item["options"],
                    correct_index=item["correct_index"],
                    explanation=item["explanation"],
                    difficulty=item["difficulty"],
                    order=index,
                    tags=[payload.topic],
                )
            )
        db.commit()
        quiz_id = quiz.id

    return {"questions": questions, "quiz_id": quiz_id}


@router.post("/interview/start")
def interview_start(payload: InterviewStartRequest, user: CurrentUser, db: DbSession) -> dict:
    prompt = (
        f"You are interviewing a candidate for the role of \"{payload.role}\".\n"
        "Ask your first interview question.\n"
        'Respond with strict JSON: {"question": "<the interview question>"}'
    )
    data = gemini.generate_json(prompt, system=_INTERVIEW_SYSTEM, temperature=0.7)
    question = str((data or {}).get("question") or "").strip() if isinstance(data, dict) else ""
    if not question:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")

    session = InterviewSession(user_id=user.id, role=payload.role, status="active", summary={})
    db.add(session)
    db.flush()
    db.add(
        InterviewTurn(
            session_id=session.id,
            question=question,
            user_answer="",
            score=None,
            strengths=[],
            weaknesses=[],
            improved_answer="",
        )
    )
    db.commit()
    return {"session_id": session.id, "question": question, "question_number": 1}


@router.post("/interview/answer")
def interview_answer(
    payload: InterviewAnswerRequest, user: CurrentUser, db: DbSession
) -> dict:
    session = db.get(InterviewSession, payload.session_id)
    if session is None or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    if session.status != "active":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Interview already completed")

    turns = db.scalars(
        select(InterviewTurn)
        .where(InterviewTurn.session_id == session.id)
        .order_by(InterviewTurn.id)
    ).all()
    current = next((turn for turn in reversed(turns) if not (turn.user_answer or "").strip()), None)
    if current is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Interview already completed")

    transcript = [
        f"Q: {turn.question}\nA: {turn.user_answer}"
        for turn in turns
        if (turn.user_answer or "").strip()
    ]
    prompt = (
        f"Role: {session.role}\n"
        f"Question asked: {current.question}\n"
        f"Candidate answer: {payload.answer}\n"
        + (f"Earlier conversation:\n" + "\n".join(transcript[-6:]) + "\n" if transcript else "")
        + "Evaluate this answer.\n"
        "Respond with strict JSON: {\"score\": <integer 1-10>, \"strengths\": [<strings>], "
        "\"weaknesses\": [<strings>], \"improved_answer\": <string>, "
        "\"next_question\": <string or null>, \"finish\": <boolean>}. "
        "Set next_question to null and finish to true when the interview should end."
    )
    data = gemini.generate_json(prompt, system=_INTERVIEW_SYSTEM, temperature=0.6)
    if not isinstance(data, dict):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")

    score = _clamp_score(data.get("score"))
    strengths = [str(item) for item in (data.get("strengths") or []) if str(item).strip()]
    weaknesses = [str(item) for item in (data.get("weaknesses") or []) if str(item).strip()]
    improved = str(data.get("improved_answer") or "")
    raw_next = data.get("next_question")
    next_question = str(raw_next).strip() if raw_next else ""
    wants_finish = bool(data.get("finish"))

    current.user_answer = payload.answer
    current.score = score
    current.strengths = strengths
    current.weaknesses = weaknesses
    current.improved_answer = improved
    db.flush()

    turns = db.scalars(
        select(InterviewTurn)
        .where(InterviewTurn.session_id == session.id)
        .order_by(InterviewTurn.id)
    ).all()
    answered = [turn for turn in turns if turn.score is not None]
    overall = round(sum(turn.score for turn in answered) / len(answered), 2)
    session.overall_score = overall

    finish = (not next_question) or wants_finish or len(answered) >= 10
    if finish:
        session.status = "completed"
        session.summary = {
            "strengths": _top_three([turn.strengths or [] for turn in answered]),
            "weaknesses": _top_three([turn.weaknesses or [] for turn in answered]),
        }
        next_question = None
        achievements.unlock(db, user, "interview_first")
    else:
        db.add(
            InterviewTurn(
                session_id=session.id,
                question=next_question,
                user_answer="",
                score=None,
                strengths=[],
                weaknesses=[],
                improved_answer="",
            )
        )
    db.commit()

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improved_answer": improved,
        "next_question": next_question,
        "progress": {"answered": len(answered), "overall_score": overall},
    }


@router.get("/interview/sessions")
def list_interview_sessions(user: CurrentUser, db: DbSession) -> list[dict]:
    sessions = db.scalars(
        select(InterviewSession)
        .where(InterviewSession.user_id == user.id)
        .order_by(InterviewSession.created_at.desc(), InterviewSession.id.desc())
    ).all()
    counts = dict(
        db.execute(
            select(InterviewTurn.session_id, func.count(InterviewTurn.id)).group_by(
                InterviewTurn.session_id
            )
        ).all()
    )
    return [
        {
            "id": session.id,
            "role": session.role,
            "status": session.status,
            "overall_score": session.overall_score,
            "summary": session.summary or {},
            "turns_count": int(counts.get(session.id, 0)),
            "created_at": session.created_at,
        }
        for session in sessions
    ]


@router.get("/interview/sessions/{id}")
def get_interview_session(id: int, user: CurrentUser, db: DbSession) -> dict:
    session = db.get(InterviewSession, id)
    if session is None or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
    turns = db.scalars(
        select(InterviewTurn)
        .where(InterviewTurn.session_id == session.id)
        .order_by(InterviewTurn.id)
    ).all()
    return {
        "id": session.id,
        "role": session.role,
        "status": session.status,
        "overall_score": session.overall_score,
        "summary": session.summary or {},
        "created_at": session.created_at,
        "turns": [
            {
                "id": turn.id,
                "question": turn.question,
                "user_answer": turn.user_answer or "",
                "score": turn.score,
                "strengths": turn.strengths or [],
                "weaknesses": turn.weaknesses or [],
                "improved_answer": turn.improved_answer or "",
                "created_at": turn.created_at,
            }
            for turn in turns
        ],
    }


@router.post("/study-plan")
def create_study_plan(payload: StudyPlanRequest, user: CurrentUser, db: DbSession) -> dict:
    performance = payload.performance or "No performance data available yet."
    prompt = (
        f"Create a study plan.\nGoal: {payload.goal}\nExam: {payload.exam or 'General preparation'}\n"
        f"Hours per day: {payload.hours_per_day}\nDuration (days): {payload.duration_days}\n"
        f"Learner performance: {performance}\n"
        "Respond with strict JSON: {\"daily\": [{\"day\": <int>, \"items\": "
        "[{\"time\": <string>, \"task\": <string>, \"hours\": <number>}]}], "
        "\"weekly\": [{\"week\": <int>, \"focus\": <string>, \"tasks\": [<strings>]}], "
        "\"monthly\": [{\"month\": <int>, \"milestones\": [<strings>]}]}. "
        f"Cover exactly {payload.duration_days} days."
    )
    plan = gemini.generate_json(prompt, system=_PLANNER_SYSTEM, temperature=0.7)
    if not isinstance(plan, dict):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    record = StudyPlan(
        user_id=user.id,
        goal=payload.goal,
        exam=payload.exam,
        hours_per_day=payload.hours_per_day,
        duration_days=payload.duration_days,
        plan={
            "daily": plan.get("daily") or [],
            "weekly": plan.get("weekly") or [],
            "monthly": plan.get("monthly") or [],
        },
        is_active=True,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "plan": record.plan}


@router.get("/study-plans")
def list_study_plans(user: CurrentUser, db: DbSession) -> list[dict]:
    plans = db.scalars(
        select(StudyPlan)
        .where(StudyPlan.user_id == user.id)
        .order_by(StudyPlan.created_at.desc(), StudyPlan.id.desc())
    ).all()
    return [
        {
            "id": plan.id,
            "goal": plan.goal,
            "exam": plan.exam,
            "hours_per_day": plan.hours_per_day,
            "duration_days": plan.duration_days,
            "is_active": plan.is_active,
            "created_at": plan.created_at,
        }
        for plan in plans
    ]


@router.get("/study-plans/{id}")
def get_study_plan(id: int, user: CurrentUser, db: DbSession) -> dict:
    plan = db.get(StudyPlan, id)
    if plan is None or plan.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found")
    return {
        "id": plan.id,
        "goal": plan.goal,
        "exam": plan.exam,
        "hours_per_day": plan.hours_per_day,
        "duration_days": plan.duration_days,
        "is_active": plan.is_active,
        "plan": plan.plan,
        "created_at": plan.created_at,
    }


@router.delete("/study-plans/{id}")
def delete_study_plan(id: int, user: CurrentUser, db: DbSession) -> dict:
    plan = db.get(StudyPlan, id)
    if plan is None or plan.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found")
    db.delete(plan)
    db.commit()
    return {"message": "Study plan deleted"}
