#!/usr/bin/env python3
"""
Run entity matching accuracy tests and generate a comprehensive report.

This script runs the test suite and provides detailed analysis of:
- Placeholder vs BERT performance comparison
- Accuracy metrics by difficulty level
- Similarity score distributions
- Specific failure cases
"""

import sys
import subprocess
from pathlib import Path

# Get project root
script_dir = Path(__file__).parent.absolute()
project_root = script_dir.parent
backend_dir = project_root / "backend"


def run_tests(test_class: str = None, verbose: bool = True):
    """Run pytest with specified test class."""
    cmd = ["pytest", "tests/test_entity_matching_accuracy.py"]

    if test_class:
        cmd[1] = f"tests/test_entity_matching_accuracy.py::{test_class}"

    if verbose:
        cmd.extend(["-v", "-s"])

    print(f"Running: {' '.join(cmd)}")
    print("=" * 80)

    result = subprocess.run(cmd, cwd=backend_dir)
    return result.returncode


def main():
    """Run comprehensive matching tests."""
    print("Entity Matching Test Suite")
    print("=" * 80)
    print()

    # Change to backend directory
    import os

    os.chdir(backend_dir)

    # Run tests in order
    tests = [
        ("Placeholder Matching (Current Implementation)", "TestPlaceholderMatching"),
        ("BERT Matching (Fixed Implementation)", "TestBERTMatching"),
        ("Accuracy Metrics", "TestAccuracyMetrics"),
    ]

    for description, test_class in tests:
        print(f"\n{'=' * 80}")
        print(f"Running: {description}")
        print(f"{'=' * 80}\n")

        returncode = run_tests(test_class)

        if returncode != 0 and test_class != "TestPlaceholderMatching":
            # Placeholder is expected to fail, but others shouldn't
            print(f"\n⚠️  Warning: {test_class} had failures")

        input("\nPress Enter to continue to next test suite...")

    print("\n" + "=" * 80)
    print("Test Suite Complete!")
    print("=" * 80)
    print("\nSee MATCHING_ANALYSIS.md for detailed analysis and recommendations.")


if __name__ == "__main__":
    main()
