from __future__ import annotations

import io
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pypdf import PdfReader

from app.core.security import AdminUser, CurrentUser, DbSession
from app.schemas.ai import CurrentAffairsGenerateRequest, ResumePolishRequest
from app.services import gemini

router = APIRouter(tags=["ai-tools"])

_MAX_TEXT_CHARS = 15000

_ANALYSIS_SYSTEM = (
    "You are an expert ATS resume reviewer for hiring managers. "
    "You always answer with strict, valid JSON only."
)
_CA_SYSTEM = (
    "You are an editor preparing daily current affairs for competitive exam aspirants. "
    "You always answer with strict, valid JSON only."
)


def _extract_pdf_text(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        parts: list[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text:
                parts.append(text)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not read PDF file")
    return "\n".join(parts).strip()[:_MAX_TEXT_CHARS]


@router.post("/resume/analyze")
def analyze_resume(
    user: CurrentUser, db: DbSession, file: UploadFile = File(...)
) -> dict:
    filename = (file.filename or "").lower()
    if not filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported")
    data = file.file.read()
    text = _extract_pdf_text(data)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No extractable text found in the PDF"
        )
    prompt = (
        "Analyse this resume for ATS readiness.\n"
        f"Resume text:\n\"\"\"\n{text}\n\"\"\"\n"
        "Respond with strict JSON: {\"ats_score\": <integer 0-100>, "
        "\"missing_keywords\": [<strings>], \"suggestions\": [<strings>], "
        "\"job_recommendations\": [{\"title\": <string>, \"reason\": <string>}]}."
    )
    data_json = gemini.generate_json(prompt, system=_ANALYSIS_SYSTEM, temperature=0.4)
    if not isinstance(data_json, dict):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    try:
        ats_score = int(round(float(data_json.get("ats_score", 0))))
    except (TypeError, ValueError):
        ats_score = 0
    recommendations = data_json.get("job_recommendations") or []
    cleaned_recommendations = [
        {
            "title": str(item.get("title") or ""),
            "reason": str(item.get("reason") or ""),
        }
        for item in recommendations
        if isinstance(item, dict)
    ]
    return {
        "ats_score": max(0, min(100, ats_score)),
        "missing_keywords": [str(item) for item in (data_json.get("missing_keywords") or [])],
        "suggestions": [str(item) for item in (data_json.get("suggestions") or [])],
        "job_recommendations": cleaned_recommendations,
        "extracted_text": text,
    }


@router.post("/resume/polish")
def polish_resume(payload: ResumePolishRequest, user: CurrentUser, db: DbSession) -> dict:
    target = payload.target_role or "the target role"
    prompt = (
        f"Polish the \"{payload.section}\" section of a resume for a candidate targeting {target}.\n"
        f"Current text:\n\"\"\"\n{payload.content}\n\"\"\"\n"
        "Return only the improved text (no markdown, no preamble). Keep it concise and factual."
    )
    polished = gemini.generate_text(prompt, system=_ANALYSIS_SYSTEM, temperature=0.6).strip()
    if not polished:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    return {"content": polished}


@router.post("/current-affairs")
def generate_current_affairs(
    payload: CurrentAffairsGenerateRequest, admin: AdminUser, db: DbSession
) -> dict:
    day = str(payload.date) if payload.date else "today"
    articles = payload.articles or "Use your best knowledge of recent events."
    prompt = (
        f"Prepare current affairs content dated {day} for competitive exam aspirants.\n"
        f"Source notes/articles:\n\"\"\"\n{articles}\n\"\"\"\n"
        "Respond with strict JSON: {\"title\": <string>, \"summary\": <string>, \"content\": <string>, "
        "\"ai_content\": {\"mcqs\": [{\"question\": <string>, \"options\": [<4 strings>], "
        "\"correct_index\": <0-3>, \"explanation\": <string>}], \"short_questions\": [<strings>], "
        "\"revision_notes\": <string>}}. Include 5 MCQs."
    )
    generated: Any = gemini.generate_json(prompt, system=_CA_SYSTEM, temperature=0.7)
    if not isinstance(generated, dict):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI provider error")
    ai_content = generated.get("ai_content")
    if not isinstance(ai_content, dict):
        ai_content = {
            "mcqs": generated.get("mcqs") or [],
            "short_questions": generated.get("short_questions") or [],
            "revision_notes": str(generated.get("revision_notes") or ""),
        }
    return {
        "title": str(generated.get("title") or f"Current Affairs — {day}"),
        "summary": str(generated.get("summary") or ""),
        "content": str(generated.get("content") or ""),
        "ai_content": ai_content,
    }
