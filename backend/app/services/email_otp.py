"""Email verification via magic link.

Flow: register creates an unverified user and emails a verification link,
``verify-email`` consumes the link token and activates the account,
``resend-otp`` emails a fresh link. Tokens are 256-bit random values stored
as SHA-256 hashes, expire after 24 hours, and resends are throttled to one
per minute (each resend invalidates older links).

(The ``email_otps`` table predates this flow when short codes were used; the
``purpose`` column distinguishes link tokens. No migration was needed.)

Delivery mirrors the forgot-password pattern: real SMTP when configured,
otherwise (local development) the link is printed to the server log and
returned in the ``dev_token`` response field.
"""
from __future__ import annotations

import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import EmailOTP, User
from app.services.common import naive_utc_now

VERIFY_LINK_TTL_HOURS = 24
OTP_RESEND_COOLDOWN_SECONDS = 60


class OtpError(ValueError):
    """User-facing verification failure with a stable, matchable message."""


def hash_token(token: str) -> str:
    return hashlib.sha256(token.strip().encode("utf-8")).hexdigest()


def verification_link(token: str) -> str:
    base = (settings.frontend_url or "http://localhost:5173").rstrip("/")
    return f"{base}/verify-email?token={token}"


def _as_naive(value: datetime) -> datetime:
    # SQLite returns naive datetimes, Postgres aware ones; stored instants are UTC.
    if value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


def ensure_user_columns(engine: Engine) -> int:
    """Add ``users.is_verified`` to databases created before this feature.

    Existing accounts predate verification, so they are grandfathered as
    verified instead of being locked out. Returns rows backfilled.
    """
    from sqlalchemy import inspect, text

    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    backfilled = 0
    with engine.begin() as connection:
        if "is_verified" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
            # The column is brand new, so every row predates verification.
            backfilled = connection.execute(text("UPDATE users SET is_verified = TRUE")).rowcount or 0
        else:
            backfilled = connection.execute(
                text("UPDATE users SET is_verified = TRUE WHERE is_verified IS NULL")
            ).rowcount or 0
    return backfilled


def _latest_otp(db: Session, user_id: int) -> EmailOTP | None:
    return db.scalar(
        select(EmailOTP)
        .where(EmailOTP.user_id == user_id, EmailOTP.purpose == "verify_link")
        .order_by(EmailOTP.id.desc())
        .limit(1)
    )


def issue_verify_link(db: Session, user: User) -> tuple[str, EmailOTP]:
    """Create a fresh verification link token, invalidating older ones."""
    now = naive_utc_now()
    latest = _latest_otp(db, user.id)
    if latest is not None:
        elapsed = (now - _as_naive(latest.created_at)).total_seconds()
        if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed) + 1
            raise OtpError(f"A verification email was just sent - please wait {wait}s before requesting a new one.")
    db.query(EmailOTP).filter(
        EmailOTP.user_id == user.id,
        EmailOTP.purpose == "verify_link",
        EmailOTP.consumed.is_(False),
    ).update({"consumed": True})
    plain = secrets.token_urlsafe(32)
    row = EmailOTP(
        user_id=user.id,
        otp_hash=hash_token(plain),
        purpose="verify_link",
        expires_at=now + timedelta(hours=VERIFY_LINK_TTL_HOURS),
        attempts=0,
        consumed=False,
    )
    db.add(row)
    db.commit()
    return plain, row


def consume_verify_token(db: Session, token: str) -> User:
    """Consume a verification link token; on success the account is verified."""
    row = db.scalar(
        select(EmailOTP).where(
            EmailOTP.otp_hash == hash_token(token or ""),
            EmailOTP.purpose == "verify_link",
        )
    )
    if row is None:
        raise OtpError("This verification link is invalid - request a new one.")
    user = db.get(User, row.user_id)
    if user is None:
        raise OtpError("This verification link is invalid - request a new one.")
    if user.is_verified:
        raise OtpError("This email is already verified - please log in.")
    if row.consumed:
        raise OtpError("This link was already used - request a new one.")
    if _as_naive(row.expires_at) <= naive_utc_now():
        raise OtpError("This link has expired - request a new one.")
    row.consumed = True
    user.is_verified = True
    db.commit()
    return user


def _send_email(to: str, subject: str, body: str) -> None:
    from fastapi import HTTPException, status

    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
            server.starttls()
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)
    except (smtplib.SMTPException, OSError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email",
        )


def send_verification_email(user: User, link: str) -> bool:
    """Deliver the verification link. Returns True when a real email went out."""
    if not settings.smtp_host and settings.environment == "development":
        print(f"[verify] link for {user.email}: {link}", flush=True)
        return False
    _send_email(
        user.email,
        "CareerPrep Hub - verify your email",
        f"Hi {user.full_name},\n\nWelcome to CareerPrep Hub! Open the link below to verify "
        f"your email and activate your account:\n\n{link}\n\n"
        f"The link expires in {VERIFY_LINK_TTL_HOURS} hours. If you did not sign up, ignore this email.",
    )
    return True
