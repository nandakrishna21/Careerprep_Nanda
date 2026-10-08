from __future__ import annotations

import json
import re
from typing import Any

import httpx
from fastapi import HTTPException

from app.core.config import settings

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_TIMEOUT_SECONDS = 90.0
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*(.*?)\s*```$", re.DOTALL)


def _strip_fences(text: str) -> str:
    match = _FENCE_RE.match(text.strip())
    if match:
        return match.group(1).strip()
    return text.strip()


def _call(prompt: str, system: str | None, temperature: float, response_mime_type: str | None) -> str:
    if not settings.gemini_api_key:
        raise HTTPException(status_code=503, detail="AI is not configured. Set GEMINI_API_KEY.")
    generation_config: dict[str, Any] = {"temperature": temperature}
    if response_mime_type:
        generation_config["responseMimeType"] = response_mime_type
    body: dict[str, Any] = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    url = _GEMINI_URL.format(model=settings.gemini_model)
    try:
        with httpx.Client(timeout=_TIMEOUT_SECONDS) as client:
            response = client.post(url, headers={"x-goog-api-key": settings.gemini_api_key}, json=body)
        response.raise_for_status()
        payload = response.json()
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        if not isinstance(text, str):
            raise ValueError("non-text candidate")
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=502, detail="AI provider error")
    return text


def generate_text(prompt: str, system: str | None = None, temperature: float = 0.7) -> str:
    return _call(prompt, system, temperature, None)


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
