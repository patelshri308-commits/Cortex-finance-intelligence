"""Router test cases for evaluation framework."""

ROUTER_TESTS = [
    # Revenue Summary Tests (original)
    {
        "query": "Give me a revenue summary",
        "expected_route": "revenue_summary",
    },
    {
        "query": "Summarize ARR performance",
        "expected_route": "revenue_summary",
    },
    # Variance Analysis Tests (original)
    {
        "query": "Why did ARR decline?",
        "expected_route": "variance_analysis",
    },
    {
        "query": "What drove ARR growth?",
        "expected_route": "variance_analysis",
    },
    # Executive Briefing Tests (original)
    {
        "query": "Create a CFO briefing",
        "expected_route": "executive_briefing",
    },
    {
        "query": "Board level revenue update",
        "expected_route": "executive_briefing",
    },
    # Forecast Sensitivity Tests (original)
    {
        "query": "What happens if churn increases by 10%?",
        "expected_route": "forecast_sensitivity",
    },
    {
        "query": "Run a forecast scenario",
        "expected_route": "forecast_sensitivity",
    },
    # Revenue Summary Tests (edge cases)
    {
        "query": "Give me the latest revenue performance",
        "expected_route": "revenue_summary",
    },
    {
        "query": "Summarize bookings and ARR",
        "expected_route": "revenue_summary",
    },
    {
        "query": "Provide a monthly performance overview",
        "expected_route": "revenue_summary",
    },
    # Variance Analysis Tests (edge cases)
    {
        "query": "What caused ARR to decline?",
        "expected_route": "variance_analysis",
    },
    {
        "query": "Explain the main drivers of revenue movement",
        "expected_route": "variance_analysis",
    },
    {
        "query": "What are the positive and negative drivers?",
        "expected_route": "variance_analysis",
    },
    # Executive Briefing Tests (edge cases)
    {
        "query": "Prepare a board-ready revenue update",
        "expected_route": "executive_briefing",
    },
    {
        "query": "Create a leadership summary for the latest month",
        "expected_route": "executive_briefing",
    },
    {
        "query": "Write a CFO-level performance briefing",
        "expected_route": "executive_briefing",
    },
    # Forecast Sensitivity Tests (edge cases)
    {
        "query": "What if bookings decrease by 15%?",
        "expected_route": "forecast_sensitivity",
    },
    {
        "query": "Assume churn rises by 20%",
        "expected_route": "forecast_sensitivity",
    },
    {
        "query": "If expansion revenue falls by 10%, what happens?",
        "expected_route": "forecast_sensitivity",
    },
]


RESPONSE_QUALITY_TESTS = [
    {
        "question": "Why did ARR decline last month?",
        "agent": "variance_analysis",
        "must_contain": ["ARR", "decline", "expansion", "contraction", "churn"],
        "must_not_contain": ["customer satisfaction", "pricing strategy", "market competition"],
    },
    {
        "question": "Create a CFO-ready briefing on latest revenue performance",
        "agent": "executive_briefing",
        "must_contain": ["ARR", "bookings", "risk", "takeaway"],
        "must_not_contain": ["sales team performance", "product quality", "market competition"],
    },
    {
        "question": "What happens if churned revenue increases by 10%?",
        "agent": "forecast_sensitivity",
        "must_contain": ["churn", "10%", "ARR"],
        "must_not_contain": ["pricing strategy", "customer satisfaction", "market competition"],
    },
]
