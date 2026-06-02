"""End-to-end agent evaluation with routing and response quality scoring."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from agents.router_agent import route_query
from agents.revenue_summary_agent import generate_revenue_summary
from agents.variance_analysis_agent import generate_variance_analysis
from agents.executive_briefing_agent import generate_executive_briefing
from agents.forecast_sensitivity_agent import generate_forecast_sensitivity_from_question

from evaluation.test_cases import RESPONSE_QUALITY_TESTS
from evaluation.response_quality_tests import score_response


def execute_agent_by_route(route: str, question: str = None):
    """
    Execute the appropriate agent based on route.

    Args:
        route (str): One of: revenue_summary, variance_analysis, executive_briefing, forecast_sensitivity
        question (str): User question (used for forecast_sensitivity)

    Returns:
        str: Agent response or error message
    """
    try:
        if route == "revenue_summary":
            return generate_revenue_summary()
        elif route == "variance_analysis":
            return generate_variance_analysis()
        elif route == "executive_briefing":
            return generate_executive_briefing()
        elif route == "forecast_sensitivity":
            if question:
                return generate_forecast_sensitivity_from_question(question)
            else:
                return generate_forecast_sensitivity_from_question("Run a forecast scenario")
        else:
            return f"Error: Unknown route '{route}'"
    except Exception as e:
        error_msg = str(e)
        if "Snowflake" in error_msg or "configuration" in error_msg.lower():
            return f"[SKIPPED] Snowflake not configured: {error_msg}"
        return f"[ERROR] Agent execution failed: {error_msg}"


def run_end_to_end_test(test_case):
    """
    Run a single end-to-end test: route -> execute -> evaluate.

    Args:
        test_case (dict): Test case from RESPONSE_QUALITY_TESTS

    Returns:
        dict: Test result with routing, execution, and quality score
    """
    question = test_case["question"]
    expected_agent = test_case["agent"]

    # Step 1: Route the question
    selected_agent = route_query(question)

    # Step 2: Execute the agent
    response = execute_agent_by_route(selected_agent, question)

    # Step 3: Check if skipped
    is_skipped = "[SKIPPED]" in response

    # Step 4: Score the response
    quality_score = score_response(response, test_case) if not is_skipped else {}

    # Step 5: Build result
    routing_correct = selected_agent == expected_agent
    quality_pass = quality_score.get("passed", False) if not is_skipped else None
    overall_pass = (routing_correct and quality_pass) if not is_skipped else None

    return {
        "question": question,
        "expected_agent": expected_agent,
        "selected_agent": selected_agent,
        "routing_correct": routing_correct,
        "response_preview": response[:200] + "..." if len(response) > 200 else response,
        "quality_score": quality_score,
        "overall_pass": overall_pass,
        "is_skipped": is_skipped,
    }


def run_all_end_to_end_tests():
    """
    Run all end-to-end tests and generate report.

    Returns:
        dict: Summary report with results
    """
    results = []
    passed_count = 0
    failed_count = 0
    skipped_count = 0

    print("\n" + "=" * 80)
    print("END-TO-END AGENT EVALUATION")
    print("=" * 80)

    for i, test_case in enumerate(RESPONSE_QUALITY_TESTS, 1):
        print(f"\n[Test {i}/{len(RESPONSE_QUALITY_TESTS)}] Running...", end="", flush=True)

        try:
            result = run_end_to_end_test(test_case)
            results.append(result)

            # Check if test was skipped (no Snowflake config)
            if result.get("is_skipped", False):
                print(f" ⊘ SKIPPED (Snowflake not configured)")
                skipped_count += 1
                # Print concise skipped card
                print("\nQuestion:")
                print(f"  {result['question']}")
                print("Expected Agent:")
                print(f"  {result['expected_agent']}")
                print("Selected Agent:")
                print(f"  {result['selected_agent']}")
                print("Routing Status: SKIPPED")
            else:
                status = "PASS" if result["overall_pass"] else "FAIL"
                print(f" {status}")

                # Scorecard per requirements
                print("\nQuestion:")
                print(f"  {result['question']}")
                print("Expected Agent:")
                print(f"  {result['expected_agent']}")
                print("Selected Agent:")
                print(f"  {result['selected_agent']}")
                print("Routing Status:")
                print(f"  {'PASS' if result['routing_correct'] else 'FAIL'}")

                # Must contain section
                must_contain = test_case.get('must_contain', [])
                present = []
                missing = []
                resp_lower = result['quality_score'].get('response_text', '').lower() if result['quality_score'] else ''
                # score_response already returns missing terms; reuse
                missing = result['quality_score'].get('missing_terms', [])
                for term in must_contain:
                    if term not in missing:
                        present.append(term)

                print("\nMust Contain:")
                print(f"  Present terms: {present if present else 'None'}")
                print(f"  Missing terms: {missing if missing else 'None'}")

                # Forbidden terms
                forbidden_found = result['quality_score'].get('forbidden_terms_found', [])
                print("\nForbidden Terms:")
                print(f"  Found: {forbidden_found if forbidden_found else 'None'}")
                print(f"  Clean: { 'YES' if not forbidden_found else 'NO'}")

                print("\nOverall Result:")
                print(f"  {status}")

                # Failure visibility
                if status != 'PASS':
                    print("\nFAILED TEST")
                    print("Question:")
                    print(f"  {result['question']}")
                    print("Selected Agent:")
                    print(f"  {result['selected_agent']}")
                    if missing:
                        print("Missing Terms:")
                        print(f"  {missing}")
                    if forbidden_found:
                        print("Forbidden Terms Found:")
                        print(f"  {forbidden_found}")

                if status == 'PASS':
                    passed_count += 1
                else:
                    failed_count += 1

        except Exception as e:
            print(f" ✗ ERROR")
            print(f"  Question: {test_case['question']}")
            print(f"  Error: {str(e)}")
            failed_count += 1
            results.append({
                "question": test_case["question"],
                "error": str(e),
                "overall_pass": False,
                "is_skipped": False,
            })

    # Generate summary report
    total_tests = len(RESPONSE_QUALITY_TESTS)
    evaluated_tests = passed_count + failed_count
    pass_rate = (passed_count / evaluated_tests * 100) if evaluated_tests > 0 else 0

    print("\n" + "=" * 50)
    print("END-TO-END EVALUATION SUMMARY")
    print("=" * 50 + "\n")
    print(f"Total Tests:    {total_tests}")
    if skipped_count > 0:
        print(f"Skipped:        {skipped_count} (Snowflake configuration required)")
    print(f"Evaluated:      {evaluated_tests}")
    print(f"Passed:         {passed_count}")
    print(f"Failed:         {failed_count}")
    if evaluated_tests > 0:
        print(f"Pass Rate:      {pass_rate:.1f}%")
    print("\n" + "=" * 50 + "\n")

    return {
        "total_tests": total_tests,
        "skipped": skipped_count,
        "evaluated": evaluated_tests,
        "passed": passed_count,
        "failed": failed_count,
        "pass_rate": pass_rate,
        "results": results,
    }


def print_detailed_report(summary):
    """
    Print a detailed report of all test results.

    Args:
        summary (dict): Summary report from run_all_end_to_end_tests
    """
    if summary["failed"] == 0 and summary["skipped"] == 0:
        print("✓ All tests passed!")
        return

    if summary["failed"] == 0:
        print(f"✓ All {summary['passed']} evaluated tests passed!")
        if summary["skipped"] > 0:
            print(f"ℹ {summary['skipped']} test(s) skipped (Snowflake configuration required)")
        return

    print("\nDETAILED FAILURE REPORT")
    print("=" * 80)

    for i, result in enumerate(summary["results"], 1):
        if result.get("is_skipped"):
            continue  # Skip detailed report for skipped tests
        if not result.get("overall_pass", False):
            print(f"\n[Test {i}] {result.get('question', 'Unknown')}")

            if "error" in result:
                print(f"  Error: {result['error']}")
            else:
                if not result.get("routing_correct", True):
                    print(f"  Routing: Expected {result['expected_agent']}, got {result['selected_agent']}")

                quality = result.get("quality_score", {})
                if quality.get("missing_terms"):
                    print(f"  Missing terms: {quality['missing_terms']}")
                if quality.get("forbidden_terms_found"):
                    print(f"  Forbidden terms: {quality['forbidden_terms_found']}")

    print("\n" + "=" * 80)
