from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class SaveJobRequest(BaseModel):
    status: Literal["saved", "applied", "interviewing", "offer", "rejected"] = "saved"


class SaveJobResponse(BaseModel):
    job_id: int
    status: str
    is_saved: bool


class NotificationOut(BaseModel):
    id: int
    title: str
    body: str = ""
    type: str = "info"
    is_read: bool = False
    created_at: datetime


class NotificationReadRequest(BaseModel):
    ids: list[int] | None = None


class StudySessionCreate(BaseModel):
    minutes: int = Field(ge=1, le=1440)
    activity_type: str = Field(default="study", max_length=50)
    topic_id: int | None = None


class StudySessionOut(BaseModel):
    id: int
    minutes: int
    activity_type: str
    topic_id: int | None = None
    created_at: datetime


class StudySessionResponse(BaseModel):
    study_session: StudySessionOut
    streak_days: int


class ResumeCreate(BaseModel):
    title: str = Field(default="My Resume", max_length=255)
    template: Literal["modern", "classic", "minimal"] = "modern"
    data: dict = Field(default_factory=dict)


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    template: Literal["modern", "classic", "minimal"] | None = None
    data: dict | None = None


class ResumeOut(BaseModel):
    id: int
    user_id: int
    title: str
    template: str
    data: dict = Field(default_factory=dict)
    ats_score: int | None = None
    analysis: dict | None = None
    created_at: datetime
    updated_at: datetime


class LeaderboardItem(BaseModel):
    rank: int
    id: int
    full_name: str
    avatar_color: str
    xp: int
    streak_days: int
    level: int


class AchievementOut(BaseModel):
    id: int
    code: str
    title: str
    description: str = ""
    icon: str = "trophy"
    xp_reward: int
    unlocked: bool = False
    unlocked_at: datetime | None = None


class SearchItem(BaseModel):
    type: str
    title: str
    subtitle: str = ""
    url: str


class SearchResponse(BaseModel):
    courses: list[SearchItem] = Field(default_factory=list)
    topics: list[SearchItem] = Field(default_factory=list)
    lessons: list[SearchItem] = Field(default_factory=list)
    quizzes: list[SearchItem] = Field(default_factory=list)
    mock_tests: list[SearchItem] = Field(default_factory=list)
    jobs: list[SearchItem] = Field(default_factory=list)
    current_affairs: list[SearchItem] = Field(default_factory=list)


class DailyActivity(BaseModel):
    date: date
    hours: float = 0
    quizzes: int = 0


class ProgressDashboard(BaseModel):
    total_study_hours: float = 0
    total_quizzes: int = 0
    average_score: float = 0
    strong_topics: list[dict] = Field(default_factory=list)
    weak_topics: list[dict] = Field(default_factory=list)
    streak_days: int = 0
    xp: int = 0
    level: int = 1
    weekly_xp: int = 0
    mock_tests_taken: int = 0
    badges_unlocked: int = 0
    daily_activity: list[DailyActivity] = Field(default_factory=list)
    performance_trend: list[dict] = Field(default_factory=list)
    mock_performance: list[dict] = Field(default_factory=list)
