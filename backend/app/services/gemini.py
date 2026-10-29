from __future__ import annotations

import base64
import json
import re
from typing import Any, Iterator

import httpx
from fastapi import HTTPException

from app.core.config import settings

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}"
_GEMINI_URL = _BASE_URL + ":generateContent"
_STREAM_URL = _BASE_URL + ":streamGenerateContent?alt=sse"
_TIMEOUT = httpx.Timeout(connect=8.0, read=15.0, write=10.0, pool=5.0)
_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*(.*?)\s*```$", re.DOTALL)

_IMAGE_MIMES = {"image/png", "image/jpeg", "image/webp", "image/heic", "image/heif"}
_TEXT_MIMES = {"text/plain", "text/markdown", "text/csv", "application/json"}
_MAX_INLINE_TEXT_CHARS = 100_000

# Flash-lite with thinking minimised is by far the fastest (first token ~1.5s);
# the bigger models are kept as fallbacks for when Google is overloaded.
_PREFERRED_MODEL = "gemini-3.5-flash-lite"
_FALLBACK_MODELS = (
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
)

# Tried in order for every model: budget 0 is rejected on lite models, while
# level "low" is rejected on older ones, and a few models accept neither.
_THINKING_BUDGET: dict[str, Any] = {"thinkingConfig": {"thinkingBudget": 0}}
_THINKING_LOW: dict[str, Any] = {"thinkingConfig": {"thinkingLevel": "low"}}


def _thinking_configs(model: str) -> tuple[dict[str, Any], ...]:
    if "lite" in model:
        return (_THINKING_LOW, _THINKING_BUDGET, {})
    return (_THINKING_BUDGET, _THINKING_LOW, {})

_client: httpx.Client | None = None


def _client_instance() -> httpx.Client:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.Client(timeout=_TIMEOUT, limits=httpx.Limits(max_keepalive_connections=8))
    return _client


def close_client() -> None:
    global _client
    if _client is not None and not _client.is_closed:
        _client.close()
    _client = None


def _model_candidates() -> list[str]:
    # The lite model goes first even if GEMINI_MODEL points at a slower one:
    # latency matters more here, and failures still escalate through the chain.
    ordered = [_PREFERRED_MODEL, getattr(settings, "gemini_model", "") or "", *_FALLBACK_MODELS]
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


def _request_body(
    prompt: str,
    system: str | None,
    temperature: float,
    response_mime_type: str | None,
    attachments: list[tuple[str, str, bytes]] | None,
    thinking: dict[str, Any],
) -> dict[str, Any]:
    generation_config: dict[str, Any] = {"temperature": temperature, **thinking}
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
    return body


def _api_key() -> str:
    api_key = (settings.gemini_api_key or "").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="AI is not configured. Set GEMINI_API_KEY.")
    return api_key


def _raise_for_status(response: httpx.Response) -> None:
    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=502,
            detail="Gemini rejected the API key. Check GEMINI_API_KEY in the server environment.",
        )
    raise HTTPException(status_code=502, detail=f"AI provider error: {_error_message(response)}")


def _call(
    prompt: str,
    system: str | None,
    temperature: float,
    response_mime_type: str | None,
    attachments: list[tuple[str, str, bytes]] | None = None,
) -> str:
    api_key = _api_key()
    client = _client_instance()
    headers = {"x-goog-api-key": api_key}
    last_error = "no model available"
    unreachable = False
    rate_limited = False
    for model in _model_candidates():
        url = _GEMINI_URL.format(model=model)
        for thinking in _thinking_configs(model):
            body = _request_body(
                prompt, system, temperature, response_mime_type, attachments, thinking
            )
            try:
                response = client.post(url, headers=headers, json=body)
            except httpx.HTTPError:
                unreachable = True
                last_error = "AI provider unreachable"
                break
            if response.status_code in (400, 404):
                # Retired model, or this model rejects the thinking config.
                last_error = _error_message(response)
                continue
            if response.status_code == 429 or response.status_code >= 500:
                # Rate limit / overloaded model: move on instead of waiting.
                last_error = _error_message(response)
                rate_limited = response.status_code == 429
                break
            if response.status_code >= 400:
                _raise_for_status(response)
            try:
                return _extract_text(response.json())
            except (KeyError, ValueError, IndexError, TypeError, json.JSONDecodeError) as exc:
                last_error = f"unexpected response ({type(exc).__name__})"
                break
    if rate_limited:
        raise HTTPException(status_code=429, detail="Gemini rate limit reached. Please retry in a minute.")
    if unreachable:
        raise HTTPException(
            status_code=502,
            detail="AI provider unreachable. Please retry in a moment.",
        )
    raise HTTPException(status_code=502, detail=f"AI provider error: {last_error}")


def stream_text(
    prompt: str,
    system: str | None = None,
    temperature: float = 0.7,
    attachments: list[tuple[str, str, bytes]] | None = None,
) -> Iterator[str]:
    """Yield answer deltas as Gemini produces them (first token in ~1.5s)."""
    api_key = _api_key()
    client = _client_instance()
    headers = {"x-goog-api-key": api_key}
    last_error = "no model available"
    unreachable = False
    rate_limited = False
    for model in _model_candidates():
        url = _STREAM_URL.format(model=model)
        for thinking in _thinking_configs(model):
            body = _request_body(prompt, system, temperature, None, attachments, thinking)
            yielded = False
            try:
                with client.stream("POST", url, headers=headers, json=body) as response:
                    if response.status_code in (400, 404):
                        response.read()
                        last_error = _error_message(response)
                        continue
                    if response.status_code == 429 or response.status_code >= 500:
                        response.read()
                        last_error = _error_message(response)
                        rate_limited = response.status_code == 429
                        break
                    if response.status_code >= 400:
                        response.read()
                        _raise_for_status(response)
                    for line in response.iter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            return
                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        for part in (
                            (chunk.get("candidates") or [{}])[0].get("content") or {}
                        ).get("parts", []):
                            text = part.get("text")
                            if isinstance(text, str) and text:
                                yielded = True
                                yield text
                    return
            except httpx.HTTPError:
                if yielded:
                    raise HTTPException(
                        status_code=502,
                        detail="AI response was cut off. Please retry.",
                    )
                unreachable = True
                last_error = "AI provider unreachable"
                break
    if rate_limited:
        raise HTTPException(status_code=429, detail="Gemini rate limit reached. Please retry in a minute.")
    if unreachable:
        raise HTTPException(
            status_code=502,
            detail="AI provider unreachable. Please retry in a moment.",
        )
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
