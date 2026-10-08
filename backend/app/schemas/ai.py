from __future__ import annotations

from datetime import date as date_type

from pydantic import BaseModel, Field


class QuizGenerateRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    difficulty: str = "beginner"
    count: int = Field(default=10, ge=1, le=50)
    save: bool = False
    title: str | None = Field(default=None, max_length=255)


class GeneratedQuestion(BaseModel):
    question_text: str
    options: list[str]
    correct_index: int
    explanation: str = ""
    difficulty: str = "beginner"


class QuizGenerateResponse(BaseModel):
    questions: list[GeneratedQuestion]
    quiz_id: int | None = None


class InterviewStartRequest(BaseModel):
    role: str = Field(min_length=1, max_length=100)


class InterviewStartResponse(BaseModel):
    session_id: int
    question: str
    question_number: int = 1


class InterviewAnswerRequest(BaseModel):
    session_id: int
    answer: str = Field(min_length=1, max_length=4000)


class InterviewAnswerResponse(BaseModel):
    score: int
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improved_answer: str = ""
    next_question: str | None = None
    progress: dict = Field(default_factory=dict)


class StudyPlanRequest(BaseModel):
    goal: str = Field(min_length=2, max_length=500)
    exam: str = Field(default="", max_length=255)
    hours_per_day: int = Field(default=2, ge=1, le=24)
    duration_days: int = Field(default=30, ge=1, le=365)
    performance: str | None = Field(default=None, max_length=4000)


class ResumeAnalyzeResponse(BaseModel):
    ats_score: int
    missing_keywords: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    job_recommendations: list[dict] = Field(default_factory=list)
    extracted_text: str = ""


class ResumePolishRequest(BaseModel):
    section: str = Field(min_length=1, max_length=60)
    content: str = Field(default="", max_length=8000)
    target_role: str = Field(default="", max_length=120)


class CurrentAffairsGenerateRequest(BaseModel):
    date: date_type | None = None
    articles: str | None = Field(default=None, max_length=12000)
