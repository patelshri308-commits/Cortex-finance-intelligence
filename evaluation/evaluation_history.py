"""Local persistence helpers for evaluation run history."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORY_PATH = PROJECT_ROOT / "outputs" / "evaluation_history.json"


def _resolve_history_path(path: str | None = None) -> Path:
    """Return the configured evaluation history path."""
    if path is None:
        return DEFAULT_HISTORY_PATH
    return Path(path)


def load_evaluation_history(path: str | None = None) -> list[dict]:
    """Load local evaluation history.

    Missing files are treated as an empty history.
    """
    history_path = _resolve_history_path(path)

    if not history_path.exists():
        return []

    with history_path.open("r", encoding="utf-8") as file:
        data: Any = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Evaluation history must be a JSON list: {history_path}")

    return data


def save_evaluation_history(history: list[dict], path: str | None = None) -> None:
    """Save local evaluation history as pretty-printed JSON."""
    history_path = _resolve_history_path(path)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    with history_path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)
        file.write("\n")


def append_evaluation_result(result: dict, path: str | None = None) -> None:
    """Append one evaluation run summary to local history."""
    history = load_evaluation_history(path)
    history.append(result)
    save_evaluation_history(history, path)


def get_latest_evaluation(path: str | None = None) -> dict | None:
    """Return the latest evaluation run summary, if one exists."""
    history = load_evaluation_history(path)
    if not history:
        return None
    return history[-1]
