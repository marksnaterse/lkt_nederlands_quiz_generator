"""Quiz loader utilities."""

import json
from pathlib import Path
from typing import Any, Dict, List, TextIO, Union


Quiz = List[Dict[str, Any]]


def _normalize_question(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Zet een ruwe vraag om naar een standaard quiz-vraag.

    Ondersteunt twee (veelvoorkomende) formats:
    - {question, choices: [...], answer: index}
    - {question, options: {a:.., b:..}, correct_answer: "a"}
    """

    question_text = raw.get("question") or raw.get("text") or "(geen vraag)"

    # Bestaand format
    choices = raw.get("choices")
    answer = raw.get("answer")

    # Oud format met opties als dict
    if choices is None and isinstance(raw.get("options"), dict):
        options = raw["options"]
        # We keep insertion order from JSON
        keys = list(options.keys())
        choices = [options[k] for k in keys]

        correct_value = raw.get("correct_answer")
        if correct_value in keys:
            answer = keys.index(correct_value)
        else:
            # Als de JSON een index of een letter bevat die niet in keys staat
            try:
                answer = int(correct_value)
            except Exception:
                answer = None

    # Zorg dat we een list hebben
    if not isinstance(choices, list):
        choices = []

    # Zorg dat answer een index is
    if isinstance(answer, int):
        answer_index = answer
    else:
        answer_index = None

    return {
        "question": question_text,
        "choices": choices,
        "answer": answer_index,
        "domain": raw.get("domain"),
        "id": raw.get("id"),
    }


def load_quiz(source: Union[str, Path, TextIO]) -> Quiz:
    """Load a quiz from a JSON file path or file-like object."""

    if hasattr(source, "read"):
        data = json.load(source)
    else:
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Quiz JSON moet een lijst met vragen bevatten")

    return [_normalize_question(q) for q in data]
