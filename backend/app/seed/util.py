"""Shared helpers for deterministic seed content generation."""
from __future__ import annotations

import random
import re
import zlib
from typing import Any

QuestionDict = dict[str, Any]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


def mcq(
    text: str,
    correct: Any,
    distractors: list[Any],
    explanation: str,
    difficulty: str = "beginner",
) -> QuestionDict:
    """Build a 4-option MCQ; guarantees unique options and a valid correct_index."""
    options: list[str] = [str(correct)]
    for candidate in distractors:
        rendered = str(candidate)
        if rendered not in options:
            options.append(rendered)
        if len(options) == 4:
            break
    counter = 1
    fallbacks = ["None of these", "All of these", "Cannot be determined", "Only two of these"]
    while len(options) < 4:
        if isinstance(correct, (int, float)):
            filler = correct + counter * 3
            if int(filler) == correct:
                filler = correct - counter * 3
            rendered = str(int(filler))
        else:
            rendered = fallbacks[len(options) - 1] if len(options) - 1 < len(fallbacks) else f"Option {len(options) + 1}"
        if rendered not in options:
            options.append(rendered)
        counter += 1
        if counter > 50:
            raise RuntimeError(f"Unable to build 4 unique options for: {text}")
    rng = random.Random(zlib.crc32(f"{text}|{correct}".encode("utf-8")))
    rng.shuffle(options)
    return {
        "question_text": text,
        "options": options,
        "correct_index": options.index(str(correct)),
        "explanation": explanation,
        "difficulty": difficulty,
    }


def num_mcq(prompt: str, answer: int, explanation: str, difficulty: str = "beginner") -> QuestionDict:
    """MCQ with auto-generated unique numeric distractors near the answer."""
    deltas = [1, 2, 5, 10, -1, -2, -5, 3, 7, 4, 6, 8, 12, 15, 20]
    distractors: list[int] = []
    for delta in deltas:
        candidate = answer + delta
        if candidate >= 0 and candidate != answer and candidate not in distractors:
            distractors.append(candidate)
        if len(distractors) == 3:
            break
    return mcq(prompt, answer, distractors, explanation, difficulty)


def pick(rng: random.Random, items: list[Any]) -> Any:
    return items[rng.randrange(len(items))]


def shuffled(seed: str) -> random.Random:
    return random.Random(seed)
