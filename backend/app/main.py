from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select

from app.api import (
    admin,
    admin_ops,
    admin_quizzes,
    ai,
    ai_tools,
    auth,
    catalog,
    government,
    jobs,
    leaderboard,
    progress,
    profile,
    quizzes,
    resumes,
    search,
)
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import Profile, User
from app.services import achievements
from app.services.job_taxonomy import backfill_jobs


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    # The jobs table gained filter columns after the first release; add them to an
    # existing database and derive role/city for anything already in it.
    backfill_jobs(engine)
    db = SessionLocal()
    try:
        admin_email = settings.admin_email.strip().lower()
        existing = db.scalar(select(User).where(func.lower(User.email) == admin_email))
        if existing is None:
            admin_user = User(
                email=admin_email,
                hashed_password=hash_password(settings.admin_password),
                full_name="Administrator",
                role="admin",
                is_active=True,
            )
            db.add(admin_user)
            db.flush()
            db.add(Profile(user_id=admin_user.id, headline="Platform Administrator"))
        db.commit()
        achievements.ensure_defaults(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="CareerPrep Hub API",
    version="1.0.0",
    description="Backend API for CareerPrep Hub — courses, quizzes, mock tests, AI tools, jobs and progress tracking.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth")
app.include_router(profile.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
app.include_router(quizzes.router, prefix="/api")
app.include_router(government.router, prefix="/api")
app.include_router(ai.router, prefix="/api/ai")
app.include_router(ai_tools.router, prefix="/api/ai")
app.include_router(resumes.router, prefix="/api/resumes")
app.include_router(jobs.router, prefix="/api/jobs")
app.include_router(progress.router, prefix="/api/progress")
app.include_router(leaderboard.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")
app.include_router(admin_quizzes.router, prefix="/api/admin")
app.include_router(admin_ops.router, prefix="/api/admin")
