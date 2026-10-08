from datetime import date

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ProfileOut(BaseModel):
    id: int
    user_id: int
    headline: str = "Aspirant"
    bio: str = ""
    phone: str = ""
    education: str = ""
    skills: list[str] = []
    target_exams: list[str] = []
    avatar_color: str = "indigo"
    xp: int = 0
    level: int = 1
    streak_days: int = 0
    last_active_date: date | None = None


class MeResponse(BaseModel):
    user: UserOut
    profile: ProfileOut


class ProfileUpdate(BaseModel):
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = None
    phone: str | None = Field(default=None, max_length=30)
    education: str | None = Field(default=None, max_length=255)
    skills: list[str] | None = None
    target_exams: list[str] | None = None
    avatar_color: str | None = Field(default=None, max_length=20)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=10, max_length=200)
    password: str = Field(min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str
