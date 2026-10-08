from __future__ import annotations

import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import CurrentUser, DbSession, create_access_token, hash_password, verify_password
from app.models import PasswordResetToken, Profile, User
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    MeResponse,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.services.common import profile_brief, user_brief
from app.services.profiles import get_or_create_profile

router = APIRouter(tags=["auth"])

_RESET_TOKEN_TTL_MINUTES = 30


def _issue_token(user: User) -> dict:
    return {
        "access_token": create_access_token(user.id, user.role),
        "token_type": "bearer",
        "user": user_brief(user),
    }


def _find_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(func.lower(User.email) == email.strip().lower()))


def _is_expired(expires_at: datetime) -> bool:
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        return expires_at <= now.replace(tzinfo=None)
    return expires_at <= now


def _send_reset_email(user: User, token: str) -> None:
    reset_url = f"/reset-password?token={token}"
    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = user.email
    message["Subject"] = "CareerPrep Hub — password reset"
    message.set_content(
        f"Hi {user.full_name},\n\nUse the token below to reset your password "
        f"(valid for {_RESET_TOKEN_TTL_MINUTES} minutes):\n\n{token}\n\n"
        f"Or open: {reset_url}\n\nIf you did not request this, ignore this email."
    )
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
            server.starttls()
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)
    except (smtplib.SMTPException, OSError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send reset email",
        )


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: DbSession) -> dict:
    if _find_user_by_email(db, str(payload.email)) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(
        email=str(payload.email).strip().lower(),
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name.strip(),
        role="student",
        is_active=True,
    )
    db.add(user)
    db.flush()
    db.add(Profile(user_id=user.id, headline=f"{payload.full_name.strip()} — Aspirant"))
    db.commit()
    db.refresh(user)
    return _issue_token(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbSession) -> dict:
    user = _find_user_by_email(db, str(payload.email))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account is inactive")
    return _issue_token(user)


@router.get("/me", response_model=MeResponse)
def me(user: CurrentUser, db: DbSession) -> dict:
    profile = get_or_create_profile(db, user)
    db.commit()
    db.refresh(user)
    db.refresh(profile)
    return {"user": user_brief(user), "profile": profile_brief(profile)}


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(payload: ForgotPasswordRequest, db: DbSession) -> dict:
    generic = "If that email is registered, a password reset request has been received."
    user = _find_user_by_email(db, str(payload.email))
    if user is None:
        return {"message": generic}
    token = secrets.token_urlsafe(32)
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=_RESET_TOKEN_TTL_MINUTES),
            used=False,
        )
    )
    db.commit()
    if not settings.smtp_host and settings.environment == "development":
        return {"message": generic, "reset_token": token}
    _send_reset_email(user, token)
    return {"message": generic}


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: DbSession) -> dict:
    row = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token == payload.token))
    if row is None or row.used or _is_expired(row.expires_at):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
    user = db.get(User, row.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")
    user.hashed_password = hash_password(payload.password)
    row.used = True
    db.commit()
    return {"message": "Password has been reset"}


@router.post("/logout", response_model=MessageResponse)
def logout() -> dict:
    return {"message": "Logged out"}
