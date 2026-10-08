from __future__ import annotations

from datetime import date as date_type
from typing import Literal

from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    category: Literal["government", "it"] = "government"
    description: str = ""
    icon: str = "book"
    level: str = "Beginner"
    order: int = 0
    is_published: bool = True
    career_path: bool = False


class CourseUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    category: Literal["government", "it"] | None = None
    description: str | None = None
    icon: str | None = None
    level: str | None = None
    order: int | None = None
    is_published: bool | None = None
    career_path: bool | None = None


class TopicCreate(BaseModel):
    course_id: int
    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    description: str = ""
    order: int = 0


class TopicUpdate(BaseModel):
    course_id: int | None = None
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    order: int | None = None


class LessonCreate(BaseModel):
    topic_id: int
    title: str = Field(min_length=1, max_length=255)
    order: int = 0
    content: dict = Field(default_factory=dict)


class LessonUpdate(BaseModel):
    topic_id: int | None = None
    title: str | None = None
    order: int | None = None
    content: dict | None = None


class QuizCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    quiz_type: Literal["topic", "pyq", "mock", "current_affair", "ai"] = "topic"
    topic_id: int | None = None
    exam_id: int | None = None
    current_affair_id: int | None = None
    difficulty: Literal["beginner", "intermediate", "advanced"] = "beginner"
    duration_minutes: int = Field(default=20, ge=1)
    negative_marks: float = Field(default=0, ge=0)
    sections: list | None = None
    total_questions: int = Field(default=0, ge=0)
    is_published: bool = True
    meta: dict = Field(default_factory=dict)


class QuizUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    quiz_type: Literal["topic", "pyq", "mock", "current_affair", "ai"] | None = None
    topic_id: int | None = None
    exam_id: int | None = None
    current_affair_id: int | None = None
    difficulty: Literal["beginner", "intermediate", "advanced"] | None = None
    duration_minutes: int | None = Field(default=None, ge=1)
    negative_marks: float | None = Field(default=None, ge=0)
    sections: list | None = None
    total_questions: int | None = Field(default=None, ge=0)
    is_published: bool | None = None
    meta: dict | None = None


class QuestionCreate(BaseModel):
    quiz_id: int
    question_text: str = Field(min_length=1)
    options: list[str] = Field(min_length=2, max_length=8)
    correct_index: int = Field(ge=0, le=7)
    explanation: str = ""
    difficulty: str = "beginner"
    order: int = 0
    tags: list[str] = Field(default_factory=list)


class QuestionUpdate(BaseModel):
    quiz_id: int | None = None
    question_text: str | None = None
    options: list[str] | None = None
    correct_index: int | None = Field(default=None, ge=0, le=7)
    explanation: str | None = None
    difficulty: str | None = None
    order: int | None = None
    tags: list[str] | None = None


class CurrentAffairCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    slug: str | None = Field(default=None, max_length=255)
    period: Literal["daily", "weekly", "monthly"] = "daily"
    date: date_type
    summary: str = ""
    content: str = ""
    ai_content: dict = Field(default_factory=dict)
    is_published: bool = True


class CurrentAffairUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    period: Literal["daily", "weekly", "monthly"] | None = None
    date: date_type | None = None
    summary: str | None = None
    content: str | None = None
    ai_content: dict | None = None
    is_published: bool | None = None


class JobAdminCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    company: str = Field(default="", max_length=255)
    type: Literal["government", "it"] = "government"
    category: str = Field(min_length=1, max_length=50)
    description: str = ""
    location: str = Field(default="", max_length=255)
    salary: str = Field(default="", max_length=255)
    apply_link: str = "#"
    deadline: date_type | None = None
    source: str = Field(default="", max_length=255)
    is_published: bool = True


class JobAdminUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    type: Literal["government", "it"] | None = None
    category: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    apply_link: str | None = None
    deadline: date_type | None = None
    source: str | None = None
    is_published: bool | None = None


class AdminUserUpdate(BaseModel):
    role: Literal["student", "admin"] | None = None
    is_active: bool | None = None
