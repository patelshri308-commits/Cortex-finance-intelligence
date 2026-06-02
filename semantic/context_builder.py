"""Semantic context builder using `semantic.finance_metrics`.

Provides utilities to detect finance concepts mentioned in a user query
and build a concise semantic context block suitable for LLM prompts.
"""
from __future__ import annotations

import re
from typing import Dict, List

from semantic.finance_metrics import (
    CONCEPT_EXPANSIONS,
    FINANCE_METRICS,
    get_all_metric_aliases,
    get_metric_definition,
)


def normalize_query(text: str) -> str:
    """Normalize query text for deterministic semantic matching."""
    if not text:
        return ""

    normalized = text.lower()
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    deduped = []

    for item in items:
        if item not in seen:
            deduped.append(item)
            seen.add(item)

    return deduped


def _contains_alias(query: str, alias: str) -> bool:
    normalized_alias = normalize_query(alias)

    if not normalized_alias:
        return False

    return re.search(rf"\b{re.escape(normalized_alias)}\b", query) is not None


def _is_parent_concept(key: str) -> bool:
    return key in CONCEPT_EXPANSIONS


def detect_semantic_terms(question: str) -> Dict[str, List[str]]:
    """Detect direct finance metrics and parent concepts in a user question."""
    query = normalize_query(question)

    if not query:
        return {
            "detected_concepts": [],
            "detected_metrics": [],
        }

    detected_concepts = []
    detected_metrics = []
    alias_map = get_all_metric_aliases()

    for alias, key in alias_map.items():
        if _contains_alias(query, alias):
            if _is_parent_concept(key):
                detected_concepts.append(key)
            else:
                detected_metrics.append(key)

    for key, info in FINANCE_METRICS.items():
        name = info.get("name", "")
        if name and _contains_alias(query, name):
            if _is_parent_concept(key):
                detected_concepts.append(key)
            else:
                detected_metrics.append(key)

    return {
        "detected_concepts": _dedupe_preserve_order(detected_concepts),
        "detected_metrics": _dedupe_preserve_order(detected_metrics),
    }


def expand_concepts(detected_concepts: List[str]) -> List[str]:
    """Expand parent semantic concepts into required child metrics."""
    expanded = []

    for concept in detected_concepts:
        expanded.extend(CONCEPT_EXPANSIONS.get(concept, []))

    return _dedupe_preserve_order(expanded)


def resolve_semantic_context(question: str) -> Dict[str, List[str]]:
    """Resolve detected concepts, direct metrics, expanded metrics, and all relevant terms."""
    detected = detect_semantic_terms(question)
    detected_concepts = detected["detected_concepts"]
    detected_metrics = detected["detected_metrics"]

    if not detected_concepts and not detected_metrics:
        detected_concepts = ["revenue_health"]

    expanded_metrics = expand_concepts(detected_concepts)

    all_relevant_terms = _dedupe_preserve_order(
        detected_concepts
        + detected_metrics
        + expanded_metrics
    )

    return {
        "detected_concepts": detected_concepts,
        "detected_metrics": detected_metrics,
        "expanded_metrics": expanded_metrics,
        "all_relevant_terms": all_relevant_terms,
    }


def detect_finance_concepts(user_query: str) -> List[str]:
    """Return all relevant semantic terms for backward-compatible callers."""
    if not user_query:
        return []

    return resolve_semantic_context(user_query)["all_relevant_terms"]


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
    resolved = resolve_semantic_context(user_query)
    detected = resolved["all_relevant_terms"]

    lines = ["Semantic Business Context:"]

    if "churn_analysis" in resolved["detected_concepts"]:
        lines.append(
            "- Churn analysis data boundary: The current dataset supports churned ARR trend "
            "and financial-impact analysis, but not definitive customer-level root-cause "
            "analysis. Do not infer unsupported causes such as pricing, product quality, "
            "customer satisfaction, market competition, geography, industry, product usage, "
            "or cancellation reasons unless those attributes are present in the KPI context."
        )

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
