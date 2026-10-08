from datetime import date, datetime

from pydantic import BaseModel, Field


class CourseListItem(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    description: str = ""
    icon: str = "book"
    level: str = "Beginner"
    career_path: bool = False
    topic_count: int = 0


class TopicListItem(BaseModel):
    id: int
    title: str
    slug: str
    description: str = ""
    order: int = 0
    lesson_count: int = 0
    quiz_count: int = 0


class CourseDetail(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    description: str = ""
    icon: str = "book"
    level: str = "Beginner"
    career_path: bool = False
    topics: list[TopicListItem] = Field(default_factory=list)


class LessonItem(BaseModel):
    id: int
    title: str
    order: int = 0


class TopicDetail(BaseModel):
    id: int
    title: str
    slug: str
    description: str = ""
    order: int = 0
    course: dict = Field(default_factory=dict)
    lessons: list[LessonItem] = Field(default_factory=list)
    quizzes: list[dict] = Field(default_factory=list)


class ExamOut(BaseModel):
    id: int
    name: str
    slug: str
    category: str = "government"
    description: str = ""
    pattern: dict = Field(default_factory=dict)


class MockTestOut(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    description: str = ""
    duration_minutes: int = 60
    total_questions: int = 100
    negative_marks: float = 0.25
    sections: list = Field(default_factory=list)
    exam_pattern: dict = Field(default_factory=dict)
    quiz_id: int | None = None
    attempts_count: int = 0


class CurrentAffairItem(BaseModel):
    id: int
    title: str
    slug: str
    period: str
    date: date
    summary: str = ""


class CurrentAffairDetail(CurrentAffairItem):
    content: str = ""
    ai_content: dict = Field(default_factory=dict)
    quiz_id: int | None = None
    quiz: dict | None = None
    created_at: datetime | None = None


class JobOut(BaseModel):
    id: int
    title: str
    company: str = ""
    type: str
    category: str
    description: str = ""
    location: str = ""
    salary: str = ""
    apply_link: str = "#"
    deadline: date | None = None
    source: str = ""
    created_at: datetime | None = None
    is_saved: bool = False
    save_status: str | None = None


class PagedJobs(BaseModel):
    items: list[JobOut]
    total: int
    page: int
    page_size: int
