"""Pure-Python semantic definitions for finance metrics.

Provides a `FINANCE_METRICS` dictionary with canonical metric entries,
aliases, definitions, related metrics, and guidance for analysis. This
module intentionally contains no external dependencies, no I/O, and no
Snowflake or Streamlit references so it can be imported anywhere.
"""
from __future__ import annotations

from typing import Dict, List


FINANCE_METRICS: Dict[str, Dict] = {
    "arr": {
        "name": "Annual Recurring Revenue",
        "aliases": ["arr", "annual recurring revenue", "recurring revenue"],
        "definition": (
            "The annualized value of recurring revenue from subscribed customers, "
            "typically calculated as MRR * 12 or by summing recurring contract values."
        ),
        "related_metrics": [
            "bookings",
            "expansion_revenue",
            "churned_revenue",
            "renewal_revenue",
        ],
        "analysis_guidance": (
            "When analyzing ARR, decompose changes into: new business (bookings), "
            "expansions, contractions, churn, and renewals. Quantify each contributor "
            "in dollars and percent to reconcile period-over-period ARR movement."
        ),
    },

    "bookings": {
        "name": "Bookings",
        "aliases": ["bookings", "new bookings", "new business bookings"],
        "definition": (
            "The total contract value or contracted ARR/MRR signed in a period, "
            "often used as a leading indicator of revenue growth."
        ),
        "related_metrics": ["arr", "new_business_revenue", "renewal_revenue"],
        "analysis_guidance": (
            "Segment bookings by new vs. renewal, and by ACV/MRR size. Use bookings "
            "to forecast future ARR but reconcile timing differences between booking "
            "and revenue recognition.")
    },

    "expansion_revenue": {
        "name": "Expansion Revenue",
        "aliases": ["expansion", "expansion revenue", "upsell revenue"],
        "definition": (
            "Additional recurring revenue from existing customers due to upsells, "
            "cross-sells, or usage growth."
        ),
        "related_metrics": ["arr", "bookings", "net_revenue_impact"],
        "analysis_guidance": (
            "Attribute expansion to identifiable cohorts or product lines when possible. "
            "Compare expansion vs. contraction to understand net customer-led growth."
        ),
    },

    "churned_revenue": {
        "name": "Churned Revenue",
        "aliases": ["churn", "churned revenue", "lost recurring revenue"],
        "definition": (
            "Recurring revenue lost from customers that fully cancel their subscriptions "
            "in the period."
        ),
        "related_metrics": ["arr", "net_revenue_impact", "contraction_revenue"],
        "analysis_guidance": (
            "Distinguish voluntary vs. involuntary churn if available. Quantify the dollars "
            "lost and express as a percent of ARR to prioritize retention efforts."
        ),
    },

    "contraction_revenue": {
        "name": "Contraction Revenue",
        "aliases": ["contraction", "contraction revenue", "downsells"],
        "definition": (
            "Recurring revenue lost from existing customers reducing their subscription "
            "value (e.g., downgrades), excluding full cancellations."
        ),
        "related_metrics": ["arr", "churned_revenue", "net_revenue_impact"],
        "analysis_guidance": (
            "Measure contraction separately from churn. Quantify the revenue impact and "
            "identify customer segments or product areas where downsells are concentrated."
        ),
    },

    "renewal_revenue": {
        "name": "Renewal Revenue",
        "aliases": ["renewal", "renewal revenue", "retained revenue"],
        "definition": (
            "Recurring revenue preserved through contract renewals from existing customers."
        ),
        "related_metrics": ["arr", "bookings", "churned_revenue"],
        "analysis_guidance": (
            "Track renewal rates by cohort and contract type. Quantify the dollar value "
            "of renewals and compare against expected renewal baselines."
        ),
    },

    "net_revenue_impact": {
        "name": "Net Revenue Impact",
        "aliases": ["net revenue impact", "net revenue change", "net revenue"],
        "definition": (
            "The net change in recurring revenue over a period after accounting for new "
            "bookings, expansions, contractions, and churn."
        ),
        "related_metrics": [
            "bookings",
            "expansion_revenue",
            "contraction_revenue",
            "churned_revenue",
        ],
        "analysis_guidance": (
            "Compute net revenue impact by summing positive contributors (bookings, expansions) "
            "and subtracting negative contributors (contraction, churn). Use this as a "
            "concise reconciliation of period-over-period revenue movement."
        ),
    },

    "revenue_quality": {
        "name": "Revenue Quality",
        "aliases": ["revenue quality", "quality of revenue"],
        "definition": (
            "A qualitative assessment of how sustainable and predictable revenue streams are, "
            "often considering factors like contract length, churn risk, and concentration."
        ),
        "related_metrics": ["arr", "renewal_revenue", "churned_revenue"],
        "analysis_guidance": (
            "Assess revenue quality by examining cohort retention, contract terms, customer "
            "concentration, and renewal behavior. Highlight risks that could make revenue "
            "less predictable."
        ),
    },

    "revenue_health": {
        "name": "Revenue Health",
        "aliases": ["revenue health", "health of revenue"],
        "definition": (
            "An aggregated view of the sustainability of a company's recurring revenue, "
            "combining growth, retention, and concentration metrics."
        ),
        "related_metrics": ["arr", "net_revenue_impact", "revenue_quality"],
        "analysis_guidance": (
            "Summarize revenue health by combining trend (ARR growth), retention (renewals/churn), "
            "and concentration signals. Provide clear numeric indicators and any leading risks."
        ),
    },
}


def get_all_metric_aliases() -> Dict[str, str]:
    """Return a mapping of alias -> canonical metric key.

    Useful for resolving free-text mentions into known semantic metrics.
    """
    alias_map: Dict[str, str] = {}
    for key, info in FINANCE_METRICS.items():
        for alias in info.get("aliases", []):
            alias_map[alias.lower()] = key
    return alias_map


def get_metric_definition(metric_key: str) -> Dict:
    """Return the metric definition dict for a given canonical key or alias.

    The function accepts either the canonical metric key (e.g., "arr") or any alias,
    and returns the corresponding metric dict. If not found, returns an empty dict.
    """
    if not metric_key:
        return {}

    key = metric_key.lower()

    # Direct key
    if key in FINANCE_METRICS:
        return FINANCE_METRICS[key]

    # Alias lookup
    for k, info in FINANCE_METRICS.items():
        for alias in info.get("aliases", []):
            if alias.lower() == key:
                return FINANCE_METRICS[k]

    return {}
