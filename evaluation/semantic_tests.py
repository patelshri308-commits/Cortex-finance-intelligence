"""Evaluation tests for the semantic business metric layer."""

from semantic.context_builder import resolve_semantic_context


TEST_CASES = [
    {
        "question": "How healthy is revenue growth?",
        "expected": [
            "revenue_health",
            "arr",
            "bookings",
            "expansion_revenue",
            "churned_revenue",
            "contraction_revenue",
            "net_revenue_impact",
        ],
    },
    {
        "question": "Is expansion offsetting churn?",
        "expected": ["expansion_revenue", "churned_revenue"],
    },
    {
        "question": "What happened to ARR?",
        "expected": ["arr"],
    },
    {
        "question": "Are we seeing revenue quality issues?",
        "expected": [
            "revenue_quality",
            "churned_revenue",
            "contraction_revenue",
            "expansion_revenue",
        ],
    },
]


def run_semantic_tests():
    results = []
    passed = 0
    failed = 0

    print("\n" + "=" * 60)
    print("RUNNING SEMANTIC METRIC DETECTION TESTS")
    print("=" * 60)

    for i, tc in enumerate(TEST_CASES, 1):
        q = tc["question"]
        expected_terms = tc["expected"]
        expected = set(expected_terms)
        resolved = resolve_semantic_context(q)
        all_relevant_terms = resolved["all_relevant_terms"]
        detected = set(all_relevant_terms)

        missing = sorted(list(expected - detected))
        status = "PASS" if not missing else "FAIL"

        print(f"\n[Test {i}/{len(TEST_CASES)}] {status}")
        print(f"  Question: {q}")
        print(f"  Expected Terms: {expected_terms}")
        print(f"  Detected Concepts: {resolved['detected_concepts']}")
        print(f"  Detected Metrics: {resolved['detected_metrics']}")
        print(f"  Expanded Metrics: {resolved['expanded_metrics']}")
        print(f"  All Relevant Terms: {all_relevant_terms}")
        print(f"  Missing Terms: {missing}")
        if missing:
            print(f"  Missing: {missing}")

        results.append({
            "question": q,
            "expected": expected_terms,
            "detected_concepts": resolved["detected_concepts"],
            "detected_metrics": resolved["detected_metrics"],
            "expanded_metrics": resolved["expanded_metrics"],
            "all_relevant_terms": all_relevant_terms,
            "missing": missing,
            "status": status,
        })

        if status == "PASS":
            passed += 1
        else:
            failed += 1

    total = len(TEST_CASES)

    print("\n" + "=" * 60)
    print("SEMANTIC TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    pass_rate = (passed / total * 100) if total > 0 else 0
    print(f"Pass Rate:   {pass_rate:.1f}%")

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "results": results,
    }


if __name__ == "__main__":
    run_semantic_tests()
