"""Evaluation tests for the semantic business metric layer."""

from semantic.context_builder import detect_finance_concepts


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
        expected = set(tc["expected"])
        detected = set(detect_finance_concepts(q))

        missing = sorted(list(expected - detected))
        status = "PASS" if not missing else "FAIL"

        print(f"\n[Test {i}/{len(TEST_CASES)}] {status}")
        print(f"  Question: {q}")
        print(f"  Expected: {sorted(list(expected))}")
        print(f"  Detected: {sorted(list(detected))}")
        if missing:
            print(f"  Missing: {missing}")

        results.append({
            "question": q,
            "expected": sorted(list(expected)),
            "detected": sorted(list(detected)),
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
