from __future__ import annotations

import base64
import json
import re
from typing import Any

import httpx
from fastapi import HTTPException

from app.core.config import settings

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_TIMEOUT_SECONDS = 90.0
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*(.*?)\s*```$", re.DOTALL)

_IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp", "image/heic", "image/heif"}
_TEXT_MIMES = {"text/plain", "text/markdown", "text/csv", "application/json"}
_MAX_INLINE_TEXT_CHARS = 100_000

# Google retires model names for new API keys (e.g. gemini-2.0-flash and
# gemini-2.5-flash now return 404 "no longer available to new users"). Try the
# configured model first, then these known-good ones before giving up, so a
# stale GEMINI_MODEL env var can never break the chat.
_FALLBACK_MODELS = (
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-3.8-flash",
    "gemini-2.5-pro",
)


def _model_candidates() -> list[str]:
    ordered = [getattr(settings, "gemini_model", "") or "", *_FALLBACK_MODELS]
    seen: set[str] = set()
    result: list[str] = []
    for model in ordered:
        model = model.strip()
        if model and model not in seen:
            seen.add(model)
            result.append(model)
    return result


def _error_message(response: httpx.Response) -> str:
    try:
        payload = response.json()
        message = (payload.get("error") or {}).get("message")
        if message:
            return str(message)[:300]
    except Exception:
        pass
    return f"HTTP {response.status_code}"


def _extract_text(payload: dict[str, Any]) -> str:
    candidates = payload.get("candidates") or []
    if not candidates:
        blocked = (payload.get("promptFeedback") or {}).get("blockReason")
        if blocked:
            raise HTTPException(status_code=502, detail=f"Gemini blocked this request ({blocked}).")
        raise KeyError("candidates")
    parts = (candidates[0].get("content") or {}).get("parts") or []
    texts = [part["text"] for part in parts if isinstance(part.get("text"), str)]
    if not texts:
        raise ValueError("empty candidate")
    return "".join(texts)


def _strip_fences(text: str) -> str:
    match = _FENCE_RE.match(text.strip())
    if match:
        return match.group(1).strip()
    return text.strip()


def _attachment_part(mime: str, data: bytes, name: str) -> dict[str, Any]:
    """Images/PDFs go to Gemini as inline data; plain text is inlined as text."""
    if mime in _TEXT_MIMES:
        decoded = data.decode("utf-8", errors="replace")[:_MAX_INLINE_TEXT_CHARS]
        return {"text": f"--- Attached file: {name} ---\n{decoded}"}
    return {
        "inlineData": {
            "mimeType": mime,
            "data": base64.b64encode(data).decode("ascii"),
        }
    }


def _call(
    prompt: str,
    system: str | None,
    temperature: float,
    response_mime_type: str | None,
    attachments: list[tuple[str, str, bytes]] | None = None,
) -> str:
    api_key = (settings.gemini_api_key or "").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="AI is not configured. Set GEMINI_API_KEY.")
    generation_config: dict[str, Any] = {"temperature": temperature}
    if response_mime_type:
        generation_config["responseMimeType"] = response_mime_type
    parts = [_attachment_part(mime, data, name) for name, mime, data in (attachments or [])]
    parts.append({"text": prompt})
    body: dict[str, Any] = {
        "contents": [{"parts": parts}],
        "generationConfig": generation_config,
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}

    last_error = "no model available"
    for model in _model_candidates():
        url = _GEMINI_URL.format(model=model)
        try:
            with httpx.Client(timeout=_TIMEOUT_SECONDS) as client:
                response = client.post(url, headers={"x-goog-api-key": api_key}, json=body)
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"AI provider unreachable ({type(exc).__name__}). Please retry in a moment.",
            )
        if response.status_code in (400, 404):
            # Unknown/retired model for this key — try the next candidate.
            last_error = _error_message(response)
            continue
        if response.status_code == 429:
            raise HTTPException(status_code=429, detail="Gemini rate limit reached. Please retry in a minute.")
        if response.status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="Gemini rejected the API key. Check GEMINI_API_KEY in the server environment.",
            )
        if response.status_code >= 400:
            raise HTTPException(
                status_code=502, detail=f"AI provider error: {_error_message(response)}"
            )
        try:
            return _extract_text(response.json())
        except (KeyError, ValueError, IndexError, TypeError, json.JSONDecodeError) as exc:
            last_error = f"unexpected response ({type(exc).__name__})"
            continue
    raise HTTPException(status_code=502, detail=f"AI provider error: {last_error}")


def generate_text(prompt: str, system: str | None = None, temperature: float = 0.7) -> str:
    return _call(prompt, system, temperature, None)


def generate_with_attachments(
    prompt: str,
    attachments: list[tuple[str, str, bytes]],
    system: str | None = None,
    temperature: float = 0.7,
) -> str:
    """`attachments` entries are (filename, mime_type, raw_bytes)."""
    return _call(prompt, system, temperature, None, attachments)


def generate_json(prompt: str, system: str | None = None, temperature: float = 0.7) -> Any:
    raw = _call(prompt, system, temperature, "application/json")
    cleaned = _strip_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        alt = cleaned.find("[")
        alt_end = cleaned.rfind("]")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                pass
        if alt != -1 and alt_end != -1 and alt_end > alt:
            try:
                return json.loads(cleaned[alt : alt_end + 1])
            except json.JSONDecodeError:
                pass
        raise HTTPException(status_code=502, detail="AI provider error")
