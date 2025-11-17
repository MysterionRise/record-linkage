#!/usr/bin/env python3
"""
Quick validation script to test entity matching without pytest.

This script demonstrates the difference between placeholder and BERT matching
on a few key test cases.
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.models.schemas import RecordBase, RecordPair
from app.ml.model import EntityMatchingModel
from app.ml.preprocessing import serialize_record_pair


def create_test_cases():
    """Create a few representative test cases."""
    return [
        {
            "name": "Exact Match",
            "record_a": {"name": "John Smith", "age": "45", "city": "New York"},
            "record_b": {"name": "John Smith", "age": "45", "city": "New York"},
            "expected_match": True,
        },
        {
            "name": "Name Abbreviation",
            "record_a": {"name": "John F. Kennedy", "birth_year": "1917"},
            "record_b": {"name": "John Fitzgerald Kennedy", "birth_year": "1917"},
            "expected_match": True,
        },
        {
            "name": "Nickname (Robert -> Bob)",
            "record_a": {"name": "Robert Smith", "address": "123 Main St"},
            "record_b": {"name": "Bob Smith", "address": "123 Main Street"},
            "expected_match": True,
        },
        {
            "name": "Address Format Difference",
            "record_a": {"address": "123 Main Street", "city": "New York", "state": "NY"},
            "record_b": {"address": "123 Main St.", "city": "New York", "state": "New York"},
            "expected_match": True,
        },
        {
            "name": "Typo (Christopher -> Chistopher)",
            "record_a": {"name": "Christopher Anderson", "address": "456 Oak Avenue"},
            "record_b": {"name": "Chistopher Anderson", "address": "456 0ak Avenue"},
            "expected_match": True,
        },
        {
            "name": "Different People (Non-match)",
            "record_a": {"name": "John Smith", "age": "45"},
            "record_b": {"name": "Jane Doe", "age": "32"},
            "expected_match": False,
        },
        {
            "name": "Same Name, Different Location (Non-match)",
            "record_a": {"name": "Michael Brown", "city": "Boston"},
            "record_b": {"name": "Michael Brown", "city": "Seattle"},
            "expected_match": False,
        },
    ]


def placeholder_similarity(record_pair: RecordPair) -> float:
    """Compute placeholder similarity (simple string matching)."""
    fields_a = record_pair.record_a.fields
    fields_b = record_pair.record_b.fields

    common_fields = set(fields_a.keys()) & set(fields_b.keys())

    if not common_fields:
        return 0.0

    matches = 0
    total = len(common_fields)

    for field in common_fields:
        value_a = str(fields_a[field]).lower()
        value_b = str(fields_b[field]).lower()

        if value_a == value_b:
            matches += 1
        elif value_a in value_b or value_b in value_a:
            matches += 0.5

    return matches / total if total > 0 else 0.0


def main():
    """Run validation tests."""
    print("=" * 80)
    print("Entity Matching Validation")
    print("=" * 80)
    print("\nThis script demonstrates the improvement from using BERT vs placeholder.\n")

    # Load BERT model
    print("Loading BERT model...")
    try:
        model = EntityMatchingModel()
        model.load_model()
        print("✓ BERT model loaded successfully!\n")
    except Exception as e:
        print(f"✗ Error loading BERT model: {e}")
        print("Please install dependencies: pip install -r backend/requirements.txt")
        return 1

    # Run test cases
    test_cases = create_test_cases()

    print("=" * 80)
    print("Test Results")
    print("=" * 80)

    threshold = 0.75

    correct_placeholder = 0
    correct_bert = 0

    for i, test_case in enumerate(test_cases, 1):
        record_a = RecordBase(id="a", fields=test_case["record_a"])
        record_b = RecordBase(id="b", fields=test_case["record_b"])
        record_pair = RecordPair(record_a=record_a, record_b=record_b)

        # Compute similarities
        placeholder_sim = placeholder_similarity(record_pair)

        text_a, text_b = serialize_record_pair(record_pair, add_sep=False)
        bert_sim, _, _ = model.compute_similarity(text_a, text_b)

        # Predictions
        placeholder_pred = placeholder_sim >= threshold
        bert_pred = bert_sim >= threshold
        expected = test_case["expected_match"]

        # Track accuracy
        if placeholder_pred == expected:
            correct_placeholder += 1
        if bert_pred == expected:
            correct_bert += 1

        # Display results
        print(f"\n{i}. {test_case['name']}")
        print(f"   Record A: {test_case['record_a']}")
        print(f"   Record B: {test_case['record_b']}")
        print(f"   Expected Match: {expected}")
        print(f"   Placeholder: {placeholder_sim:.3f} → {'MATCH' if placeholder_pred else 'NO MATCH'} {'✓' if placeholder_pred == expected else '✗'}")
        print(f"   BERT:        {bert_sim:.3f} → {'MATCH' if bert_pred else 'NO MATCH'} {'✓' if bert_pred == expected else '✗'}")

    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Placeholder Accuracy: {correct_placeholder}/{len(test_cases)} ({100 * correct_placeholder / len(test_cases):.1f}%)")
    print(f"BERT Accuracy:        {correct_bert}/{len(test_cases)} ({100 * correct_bert / len(test_cases):.1f}%)")
    print(f"\nImprovement: {correct_bert - correct_placeholder} more correct predictions with BERT")

    if correct_bert > correct_placeholder:
        print("✓ BERT matching performs better than placeholder!")
    elif correct_bert == correct_placeholder:
        print("⚠ BERT and placeholder have same accuracy (unusual)")
    else:
        print("✗ Warning: BERT performing worse than placeholder")

    print("\n" + "=" * 80)
    print("Next Steps:")
    print("=" * 80)
    print("1. Install test dependencies: pip install -r backend/requirements.txt")
    print("2. Run full test suite: pytest backend/tests/test_entity_matching_accuracy.py -v -s")
    print("3. See MATCHING_ANALYSIS.md for detailed analysis")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
