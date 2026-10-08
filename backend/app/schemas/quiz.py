from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class QuestionPublic(BaseModel):
    id: int
    question_text: str
    options: list[str]
    order: int


class AttemptRequest(BaseModel):
    answers: dict[str, int] = Field(default_factory=dict)
    time_taken_seconds: int = Field(default=0, ge=0)
    mode: Literal["practice", "exam"] = "practice"


class TopicRef(BaseModel):
    id: int
    title: str


class QuizMeta(BaseModel):
    id: int
    title: str
    slug: str = ""
    quiz_type: str
    difficulty: str
    duration_minutes: int
    total_questions: int
    negative_marks: float
    sections: list | None = None
    meta: dict = Field(default_factory=dict)
    is_published: bool = True


class QuizDetail(BaseModel):
    id: int
    title: str
    slug: str
    quiz_type: str
    difficulty: str
    duration_minutes: int
    total_questions: int
    negative_marks: float
    sections: list | None = None
    topic: TopicRef | None = None
    exam: dict | None = None
    meta: dict = Field(default_factory=dict)
    mode_options: dict = Field(default_factory=lambda: {"practice": True, "exam": True})


class ReportQuestion(BaseModel):
    id: int
    question_text: str
    options: list[str]
    your_answer: int | None = None
    correct_index: int
    explanation: str = ""
    is_correct: bool


class TopicBreakdownItem(BaseModel):
    name: str
    total: int
    correct: int
    accuracy: float


class AreaItem(BaseModel):
    topic: str
    accuracy: float


class AttemptReport(BaseModel):
    weak_areas: list[AreaItem] = Field(default_factory=list)
    strong_areas: list[AreaItem] = Field(default_factory=list)
    topic_breakdown: list[TopicBreakdownItem] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    questions: list[ReportQuestion] = Field(default_factory=list)
    section_analysis: list[dict] | None = None
    improvement_suggestions: list[str] | None = None


class AttemptOut(BaseModel):
    id: int
    quiz_id: int
    mode: str
    score: float
    total: int
    correct: int
    wrong: int
    skipped: int
    accuracy: float
    time_taken_seconds: int
    rank: int | None = None
    xp_awarded: int
    created_at: datetime


class AchievementUnlocked(BaseModel):
    code: str
    title: str
    icon: str
    xp_reward: int


class AttemptResponse(BaseModel):
    attempt: AttemptOut
    report: AttemptReport
    achievements_unlocked: list[AchievementUnlocked] = Field(default_factory=list)
