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
        "if churn",
        "churn increases",
        "churn decreases",
        "increase by",
        "decrease by",
    ]

    executive_keywords = [
        "briefing",
        "executive",
        "leadership",
        "cfo",
        "board",
        "qbr",
        "board-level",
    ]

    revenue_summary_keywords = [
        "summary",
        "summarize",
        "overview",
        "recap",
        "latest performance",
        "current performance",
        "revenue summary",
        "monthly summary",
        "performance summary",
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
        "explain why",
        "what caused",
        "what drove",
        "cause",
    ]

    # Executive always wins
    if any(keyword in query for keyword in executive_keywords):
        return "executive_briefing"

    # Forecast always wins
    if any(keyword in query for keyword in forecast_keywords):
        return "forecast_sensitivity"

    # Summary should beat variance unless user explicitly asks WHY
    if any(keyword in query for keyword in revenue_summary_keywords):
        if not any(
            keyword in query
            for keyword in [
                "why",
                "driver",
                "drivers",
                "what caused",
                "what drove",
            ]
        ):
            return "revenue_summary"

    # Variance analysis
    if any(keyword in query for keyword in variance_keywords):
        return "variance_analysis"

    return "revenue_summary"