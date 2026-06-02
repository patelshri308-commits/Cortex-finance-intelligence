def route_query(user_query: str) -> str:
    query = user_query.lower().strip()

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
        "increases by",
        "decreases by",
    ]

    executive_keywords = [
        "briefing",
        "executive",
        "leadership",
        "cfo",
        "board",
        "qbr",
        "board-level",
        "investor",
    ]

    driver_intent_keywords = [
        "what drove",
        "what is driving",
        "what are the drivers",
        "drivers of",
        "driver of",
        "driven by",
        "growth driver",
        "growth drivers",
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
        "movement",
    ]

    if any(keyword in query for keyword in executive_keywords):
        return "executive_briefing"

    if any(keyword in query for keyword in forecast_keywords):
        return "forecast_sensitivity"

    if any(keyword in query for keyword in driver_intent_keywords):
        return "variance_analysis"

    if any(keyword in query for keyword in revenue_summary_keywords):
        if not any(
            keyword in query
            for keyword in [
                "why",
                "driver",
                "drivers",
                "what caused",
                "what drove",
                "driven by",
            ]
        ):
            return "revenue_summary"

    if any(keyword in query for keyword in variance_keywords):
        return "variance_analysis"

    return "revenue_summary"


if __name__ == "__main__":
    test_queries = [
        "Give me a revenue summary",
        "Summarize latest ARR performance",
        "Why did ARR decline?",
        "What drove ARR growth?",
        "Create an executive briefing",
        "Board level revenue summary",
        "What happens if churn increases by 10%?",
        "Run a forecast sensitivity analysis",
    ]

    for query in test_queries:
        print(f"{query} → {route_query(query)}")