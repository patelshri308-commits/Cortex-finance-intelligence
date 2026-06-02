"""Evaluation runner for router tests and end-to-end agent tests."""

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from evaluation.router_tests import run_router_tests
from evaluation.end_to_end_tests import run_all_end_to_end_tests, print_detailed_report
from evaluation.evaluation_history import append_evaluation_result, load_evaluation_history
from evaluation.secret_loader import load_streamlit_secrets_into_env
from evaluation.semantic_tests import run_semantic_tests


def _summarize_router_results(results):
    if results is None:
        return None

    return {
        "passed": results["passed"],
        "total": results["total"],
        "pass_rate": results["accuracy_pct"],
    }


def _summarize_semantic_results(results):
    if results is None:
        return None

    return {
        "passed": results["passed"],
        "total": results["total"],
        "pass_rate": results["pass_rate"],
    }


def _summarize_end_to_end_results(results):
    if results is None:
        return None

    return {
        "passed": results["passed"],
        "total": results["total_tests"],
        "skipped": results["skipped"],
        "pass_rate": results["pass_rate"],
    }


def _suite_passed(summary):
    if summary is None:
        return None
    if "skipped" in summary:
        evaluated = summary["total"] - summary["skipped"]
        return summary["passed"] == evaluated
    return summary["passed"] == summary["total"]


def _build_run_summary(mode, router_results, semantic_results, e2e_results):
    router_summary = _summarize_router_results(router_results)
    semantic_summary = _summarize_semantic_results(semantic_results)
    e2e_summary = _summarize_end_to_end_results(e2e_results)

    evaluated_statuses = [
        status
        for status in [
            _suite_passed(router_summary),
            _suite_passed(semantic_summary),
            _suite_passed(e2e_summary),
        ]
        if status is not None
    ]
    overall_status = "PASS" if evaluated_statuses and all(evaluated_statuses) else "FAIL"

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "router": router_summary,
        "semantic": semantic_summary,
        "end_to_end": e2e_summary,
        "overall_status": overall_status,
    }


def _format_pass_rate(summary):
    if summary is None:
        return "N/A"
    return f"{summary['pass_rate']:.1f}%"


def _print_history_run(run):
    print(f"Timestamp:      {run.get('timestamp', 'N/A')}")
    print(f"Router:         {_format_pass_rate(run.get('router'))}")
    print(f"Semantic:       {_format_pass_rate(run.get('semantic'))}")
    print(f"End-to-End:     {_format_pass_rate(run.get('end_to_end'))}")
    print(f"Overall Status: {run.get('overall_status', 'N/A')}")


def print_evaluation_history():
    history = load_evaluation_history()

    if not history:
        print("No evaluation history found.")
        return

    print("\nLATEST EVALUATION RUN")
    print("=" * 80)
    _print_history_run(history[-1])

    print("\nLAST 5 EVALUATION RUNS")
    print("=" * 80)
    for run in history[-5:]:
        _print_history_run(run)
        print("-" * 80)


def main():
    """Run evaluation suite."""
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluation tests")
    parser.add_argument(
        "--mode",
        choices=["router", "semantic", "end-to-end", "all", "history"],
        default="router",
        help="Which tests to run (default: router)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed failure reports",
    )

    args = parser.parse_args()

    if args.mode == "history":
        print_evaluation_history()
        return None

    router_results = None
    semantic_results = None
    e2e_results = None

    if args.mode in ["router", "all"]:
        print("\n" + "=" * 80)
        print("RUNNING ROUTER TESTS")
        print("=" * 80)
        router_results = run_router_tests()

        if router_results["failed_cases"]:
            print("\nFAILED CASES:")
            print("-" * 80)
            for case in router_results["failed_cases"]:
                print(f"\nQuery: {case['query']}")
                print(f"  Expected: {case['expected']}")
                print(f"  Got:      {case['actual']}")
            print()

    if args.mode in ["end-to-end", "all"]:
        print("\n" + "=" * 80)
        print("RUNNING END-TO-END AGENT TESTS")
        print("=" * 80)
        print("\nNote: End-to-end tests require Snowflake configuration.")
        print("Set SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_WAREHOUSE\n")

        # Attempt to load Streamlit secrets into environment so local runs work
        project_root = Path(__file__).resolve().parents[1]
        loaded = load_streamlit_secrets_into_env(project_root)
        if loaded:
            print("Loaded Snowflake secrets from .streamlit/secrets.toml for evaluation:")
            for k, v in loaded.items():
                print(f"  {k} set from secrets.toml")

        e2e_results = run_all_end_to_end_tests()

        if args.verbose:
            print_detailed_report(e2e_results)

    if args.mode in ["semantic", "all"]:
        print("\n" + "=" * 80)
        print("RUNNING SEMANTIC METRIC TESTS")
        print("=" * 80)
        semantic_results = run_semantic_tests()

    run_summary = _build_run_summary(args.mode, router_results, semantic_results, e2e_results)
    append_evaluation_result(run_summary)
    print("Saved evaluation history to outputs/evaluation_history.json")

    # Final return behavior: return a dict for the mode most recently run, or router results for router
    if args.mode == "router":
        return router_results
    if args.mode == "semantic":
        return semantic_results
    if args.mode in ["end-to-end", "all"]:
        return e2e_results

    return None


if __name__ == "__main__":
    main()
