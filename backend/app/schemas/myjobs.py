from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

MyJobStatus = Literal[
    "wishlist", "applied", "preparing", "exam", "interview", "selected", "rejected"
]


class MyJobCreate(BaseModel):
    job_id: int | None = None
    template_key: str | None = Field(default=None, max_length=60)
    title: str = Field(min_length=1, max_length=300)
    organization: str = Field(default="", max_length=255)
    role_name: str = Field(default="", max_length=255)
    status: MyJobStatus = "applied"
    applied_date: date | None = None
    exam_date: date | None = None
    deadline: date | None = None
    notification_link: str = Field(default="", max_length=1000)
    apply_link: str = Field(default="", max_length=1000)
    syllabus: list = Field(default_factory=list)
    exam_pattern: list = Field(default_factory=list)
    strategy: str = ""
    preparation_plan: list = Field(default_factory=list)
    notes: str = ""


class MyJobUpdate(BaseModel):
    job_id: int | None = None
    template_key: str | None = Field(default=None, max_length=60)
    title: str | None = Field(default=None, min_length=1, max_length=300)
    organization: str | None = Field(default=None, max_length=255)
    role_name: str | None = Field(default=None, max_length=255)
    status: MyJobStatus | None = None
    applied_date: date | None = None
    exam_date: date | None = None
    deadline: date | None = None
    notification_link: str | None = Field(default=None, max_length=1000)
    apply_link: str | None = Field(default=None, max_length=1000)
    syllabus: list | None = None
    exam_pattern: list | None = None
    strategy: str | None = None
    preparation_plan: list | None = None
    notes: str | None = None
