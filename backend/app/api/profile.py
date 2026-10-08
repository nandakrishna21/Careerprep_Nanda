from __future__ import annotations

from fastapi import APIRouter

from app.core.security import CurrentUser, DbSession
from app.schemas.auth import ProfileUpdate
from app.services.common import profile_brief
from app.services.profiles import get_or_create_profile

router = APIRouter(tags=["profile"])


@router.put("/profile")
def update_profile(payload: ProfileUpdate, user: CurrentUser, db: DbSession) -> dict:
    profile = get_or_create_profile(db, user)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        if value is None:
            continue
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile_brief(profile)
