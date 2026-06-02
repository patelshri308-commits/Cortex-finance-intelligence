"""Router test execution and evaluation."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from agents.router_agent import route_query
from evaluation.test_cases import ROUTER_TESTS


def run_router_tests():
    """
    Run all router tests and return evaluation summary.

    Returns:
        dict: Summary with passed, total, accuracy_pct, and failed_cases
    """
    passed = 0
    total = len(ROUTER_TESTS)
    failed_cases = []

    print("\n" + "=" * 70)
    print("ROUTER EVALUATION")
    print("=" * 70)

    for i, test_case in enumerate(ROUTER_TESTS, 1):
        query = test_case["query"]
        expected_route = test_case["expected_route"]

        actual_route = route_query(query)

        is_pass = actual_route == expected_route
        status = "PASS" if is_pass else "FAIL"

        print(f"\n[Test {i}/{total}] {status}")
        print(f"  Query:    {query}")
        print(f"  Expected: {expected_route}")
        print(f"  Actual:   {actual_route}")

        if is_pass:
            passed += 1
        else:
            failed_cases.append(
                {
                    "query": query,
                    "expected": expected_route,
                    "actual": actual_route,
                }
            )

    accuracy_pct = (passed / total * 100) if total > 0 else 0

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} passed ({accuracy_pct:.1f}%)")
    print("=" * 70 + "\n")

    return {
        "passed": passed,
        "total": total,
        "accuracy_pct": accuracy_pct,
        "failed_cases": failed_cases,
    }
