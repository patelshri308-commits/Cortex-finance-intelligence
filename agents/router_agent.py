def route_query(user_query: str) -> str:
    query = user_query.lower()

    forecast_keywords = [
        "forecast",
        "scenario",
        "sensitivity",
        "what if",
        "projection",
        "projected",
        "simulate",
        "assumption",
        "assumptions",
        "increase",
        "decrease",
        "increases",
        "decreases",
        "if churn",
        "churn increases",
        "churn decreases",
    ]

    executive_keywords = [
        "briefing",
        "executive",
        "leadership",
        "cfo",
        "board",
        "qbr",
    ]

    variance_keywords = [
        "variance",
        "decline",
        "declined",
        "changed",
        "change",
        "why",
        "driver",
        "drivers",
        "explain",
    ]

    revenue_keywords = [
        "summary",
        "performance",
        "revenue",
        "arr",
        "bookings",
        "trend",
    ]

    if any(keyword in query for keyword in forecast_keywords):
        return "forecast_sensitivity"

    if any(keyword in query for keyword in executive_keywords):
        return "executive_briefing"

    if any(keyword in query for keyword in variance_keywords):
        return "variance_analysis"

    if any(keyword in query for keyword in revenue_keywords):
        return "revenue_summary"

    return "revenue_summary"


if __name__ == "__main__":
    test_queries = [
        "Analyze current revenue performance",
        "Why did ARR decline?",
        "Create an executive briefing",
        "What happens if churn increases by 10%?",
        "Run a forecast scenario",
    ]

    for query in test_queries:
        print(f"{query} → {route_query(query)}")