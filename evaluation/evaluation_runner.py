"""Evaluation runner for router tests and end-to-end agent tests."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from evaluation.router_tests import run_router_tests
from evaluation.end_to_end_tests import run_all_end_to_end_tests, print_detailed_report
from evaluation.secret_loader import load_streamlit_secrets_into_env
from evaluation.semantic_tests import run_semantic_tests


def main():
    """Run evaluation suite."""
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluation tests")
    parser.add_argument(
        "--mode",
        choices=["router", "semantic", "end-to-end", "all"],
        default="router",
        help="Which tests to run (default: router)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed failure reports",
    )

    args = parser.parse_args()

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
