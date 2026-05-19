def route_query(user_query: str) -> str:
    query = user_query.lower()

    if any(word in query for word in ["variance", "decline", "changed", "change", "why", "driver", "drivers"]):
        return "variance_analysis"

    if any(word in query for word in ["summary", "performance", "revenue", "arr", "bookings", "trend"]):
        return "revenue_summary"

    if any(word in query for word in ["briefing", "executive", "leadership", "cfo"]):
        return "executive_briefing"

    return "revenue_summary"


if __name__ == "__main__":
    test_queries = [
        "Analyze current revenue performance",
        "Why did ARR decline?",
        "Create an executive briefing",
    ]

    for query in test_queries:
        print(f"{query} → {route_query(query)}")