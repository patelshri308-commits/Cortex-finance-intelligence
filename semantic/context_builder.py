"""Semantic context builder using `semantic.finance_metrics`.

Provides utilities to detect finance concepts mentioned in a user query
and build a concise semantic context block suitable for LLM prompts.
"""
from __future__ import annotations

from typing import List

from semantic.finance_metrics import FINANCE_METRICS, get_all_metric_aliases, get_metric_definition


def detect_finance_concepts(user_query: str) -> List[str]:
    """Detect finance concept keys mentioned in the user query.

    Matching is performed against metric aliases and metric names (case-insensitive).
    Returns a list of canonical metric keys (e.g., 'arr', 'expansion_revenue').
    """
    if not user_query:
        return []

    q = user_query.lower()
    alias_map = get_all_metric_aliases()

    found = []
    seen = set()

    # Match aliases first
    for alias, key in alias_map.items():
        if alias in q and key not in seen:
            found.append(key)
            seen.add(key)

    # Match canonical names
    for key, info in FINANCE_METRICS.items():
        name = info.get("name", "").lower()
        if name and name in q and key not in seen:
            found.append(key)
            seen.add(key)

    return found


def _first_sentence(text: str, max_len: int = 200) -> str:
    if not text:
        return ""
    sentence = text.split(".")
    first = sentence[0].strip()
    if len(first) > max_len:
        return first[: max_len - 3].rstrip() + "..."
    return first


def build_semantic_context(user_query: str) -> str:
    """Build a concise semantic business context block for detected concepts.

    If no concepts are detected, returns a default Revenue Health context.
    The returned string is compact to fit inside LLM prompts.
    """
    detected = detect_finance_concepts(user_query)

    if not detected:
        detected = ["revenue_health"]

    lines = ["Semantic Business Context:"]

    for key in detected:
        info = get_metric_definition(key)
        if not info:
            continue

        name = info.get("name", key)
        definition = _first_sentence(info.get("definition", ""))

        related = info.get("related_metrics", [])
        # Map related metric keys to their human names where possible
        related_names = []
        for r in related:
            r_info = get_metric_definition(r)
            related_names.append(r_info.get("name", r))

        guidance = _first_sentence(info.get("analysis_guidance", ""), max_len=220)

        line = f"- {name}: {definition}"
        if related_names:
            line += f" Related: {', '.join(related_names)}."
        if guidance:
            line += f" Guidance: {guidance}."

        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    tests = [
        "How healthy is revenue growth?",
        "Is expansion offsetting churn?",
        "What happened to ARR?",
    ]

    for q in tests:
        print("\n---")
        print(f"Query: {q}")
        ctx = build_semantic_context(q)
        print(ctx)
