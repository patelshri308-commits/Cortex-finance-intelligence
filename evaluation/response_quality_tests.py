"""Response quality evaluation for agent outputs."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from evaluation.test_cases import RESPONSE_QUALITY_TESTS


def score_response(response_text, test_case):
    """
    Score a response against quality criteria.

    Args:
        response_text (str): The agent's response to evaluate
        test_case (dict): Test case with must_contain and must_not_contain

    Returns:
        dict: Scoring result with:
            - passed (bool): True if all criteria met
            - missing_terms (list): Terms expected but not found
            - forbidden_terms_found (list): Forbidden terms that appeared
            - score (str): "PASS" or "FAIL"
    """
    response_lower = response_text.lower()

    # Check for required terms
    missing_terms = []
    must_contain = test_case.get("must_contain", [])

    for term in must_contain:
        if term.lower() not in response_lower:
            missing_terms.append(term)

    # Check for forbidden terms
    forbidden_terms_found = []
    must_not_contain = test_case.get("must_not_contain", [])

    for term in must_not_contain:
        if term.lower() in response_lower:
            forbidden_terms_found.append(term)

    # Determine pass/fail
    passed = len(missing_terms) == 0 and len(forbidden_terms_found) == 0

    return {
        "passed": passed,
        "score": "PASS" if passed else "FAIL",
        "missing_terms": missing_terms,
        "forbidden_terms_found": forbidden_terms_found,
    }


def evaluate_response_quality(response_text, test_index):
    """
    Evaluate a response against a specific test case.

    Args:
        response_text (str): The agent's response
        test_index (int): Index of the test case in RESPONSE_QUALITY_TESTS

    Returns:
        dict: Evaluation result
    """
    if test_index < 0 or test_index >= len(RESPONSE_QUALITY_TESTS):
        return {"error": f"Invalid test index: {test_index}"}

    test_case = RESPONSE_QUALITY_TESTS[test_index]
    result = score_response(response_text, test_case)

    return {
        "question": test_case["question"],
        "agent": test_case["agent"],
        "result": result,
    }
