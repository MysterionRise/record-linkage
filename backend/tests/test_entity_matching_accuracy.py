"""
Comprehensive tests for entity matching accuracy using real-world test cases.

This test suite evaluates the entity matching system against realistic
record linkage challenges including:
- Name variations (abbreviations, nicknames, formats)
- Typos and OCR errors
- Missing data
- Different formats (dates, phones, addresses)
- Product and publication matching

Tests are organized by difficulty level to identify where the system
performs well and where improvements are needed.
"""

import pytest
from typing import List, Dict, Tuple

from app.models.schemas import RecordPair, RecordBase
from app.ml.inference import predict_match, _compute_placeholder_similarity
from app.ml.model import EntityMatchingModel
from app.ml.preprocessing import serialize_record_pair

# Import test cases
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "test_data"))
from entity_matching_test_cases import (
    ALL_MATCHING_TEST_CASES,
    PERSON_NAME_MATCHES,
    PERSON_NAME_NON_MATCHES,
    PUBLICATION_MATCHES,
    PRODUCT_MATCHES,
    ADDRESS_MATCHES,
    EDGE_CASES,
    get_test_cases_by_difficulty,
    get_expected_matches,
    get_expected_non_matches,
)


def create_record_pair_from_test_case(test_case: Dict) -> RecordPair:
    """Convert a test case dict into a RecordPair object."""
    record_a = RecordBase(id="a", fields=test_case["record_a"])
    record_b = RecordBase(id="b", fields=test_case["record_b"])
    return RecordPair(record_a=record_a, record_b=record_b)


class TestPlaceholderMatching:
    """Test the current placeholder string matching implementation."""

    @pytest.mark.parametrize("test_case", PERSON_NAME_MATCHES)
    def test_person_name_matches_placeholder(self, test_case):
        """Test person name matching with placeholder implementation."""
        record_pair = create_record_pair_from_test_case(test_case)
        similarity = _compute_placeholder_similarity(record_pair)

        expected_match = test_case["expected_match"]
        difficulty = test_case["difficulty"]
        description = test_case["description"]

        # Log results
        print(f"\n{difficulty.upper()}: {description}")
        print(f"Expected match: {expected_match}, Similarity: {similarity:.3f}")
        print(f"Record A: {test_case['record_a']}")
        print(f"Record B: {test_case['record_b']}")

        # For now, just collect data - don't assert
        # We expect the placeholder to fail on many cases

    @pytest.mark.parametrize("test_case", PERSON_NAME_NON_MATCHES)
    def test_person_name_non_matches_placeholder(self, test_case):
        """Test that non-matching records are correctly identified."""
        record_pair = create_record_pair_from_test_case(test_case)
        similarity = _compute_placeholder_similarity(record_pair)

        description = test_case["description"]
        print(f"\nNON-MATCH: {description}")
        print(f"Similarity: {similarity:.3f}")

    @pytest.mark.parametrize("test_case", PUBLICATION_MATCHES)
    def test_publication_matches_placeholder(self, test_case):
        """Test publication matching."""
        record_pair = create_record_pair_from_test_case(test_case)
        similarity = _compute_placeholder_similarity(record_pair)

        difficulty = test_case["difficulty"]
        description = test_case["description"]

        print(f"\nPUBLICATION {difficulty.upper()}: {description}")
        print(f"Similarity: {similarity:.3f}")

    @pytest.mark.parametrize("test_case", PRODUCT_MATCHES)
    def test_product_matches_placeholder(self, test_case):
        """Test product matching."""
        record_pair = create_record_pair_from_test_case(test_case)
        similarity = _compute_placeholder_similarity(record_pair)

        difficulty = test_case["difficulty"]
        description = test_case["description"]

        print(f"\nPRODUCT {difficulty.upper()}: {description}")
        print(f"Similarity: {similarity:.3f}")


@pytest.mark.slow
class TestBERTMatching:
    """Test BERT-based entity matching."""

    @pytest.fixture(scope="class")
    def bert_model(self):
        """Load BERT model once for all tests in this class."""
        model = EntityMatchingModel()
        model.load_model()
        return model

    def compute_bert_similarity(
        self, bert_model: EntityMatchingModel, test_case: Dict
    ) -> float:
        """Compute BERT similarity for a test case."""
        record_pair = create_record_pair_from_test_case(test_case)

        # Serialize the record pair for BERT
        text_a = serialize_record_pair(record_pair, add_sep=False)[0]
        text_b = serialize_record_pair(record_pair, add_sep=False)[1]

        # Compute BERT similarity
        similarity, _, _ = bert_model.compute_similarity(text_a, text_b)
        return similarity

    @pytest.mark.parametrize("test_case", PERSON_NAME_MATCHES)
    def test_person_name_matches_bert(self, bert_model, test_case):
        """Test person name matching with BERT."""
        similarity = self.compute_bert_similarity(bert_model, test_case)

        expected_match = test_case["expected_match"]
        difficulty = test_case["difficulty"]
        description = test_case["description"]

        print(f"\nBERT {difficulty.upper()}: {description}")
        print(f"Expected match: {expected_match}, Similarity: {similarity:.3f}")
        print(f"Record A: {test_case['record_a']}")
        print(f"Record B: {test_case['record_b']}")

        # Collect results for analysis
        # Don't assert yet - we're evaluating performance

    @pytest.mark.parametrize("test_case", PERSON_NAME_NON_MATCHES)
    def test_person_name_non_matches_bert(self, bert_model, test_case):
        """Test that BERT correctly identifies non-matches."""
        similarity = self.compute_bert_similarity(bert_model, test_case)

        description = test_case["description"]
        print(f"\nBERT NON-MATCH: {description}")
        print(f"Similarity: {similarity:.3f}")

        # Non-matches should have lower similarity
        # But don't assert yet - just collect data

    @pytest.mark.parametrize("test_case", PUBLICATION_MATCHES)
    def test_publication_matches_bert(self, bert_model, test_case):
        """Test publication matching with BERT."""
        similarity = self.compute_bert_similarity(bert_model, test_case)

        difficulty = test_case["difficulty"]
        description = test_case["description"]

        print(f"\nBERT PUBLICATION {difficulty.upper()}: {description}")
        print(f"Similarity: {similarity:.3f}")

    @pytest.mark.parametrize("test_case", PRODUCT_MATCHES)
    def test_product_matches_bert(self, bert_model, test_case):
        """Test product matching with BERT."""
        similarity = self.compute_bert_similarity(bert_model, test_case)

        difficulty = test_case["difficulty"]
        description = test_case["description"]

        print(f"\nBERT PRODUCT {difficulty.upper()}: {description}")
        print(f"Similarity: {similarity:.3f}")

    @pytest.mark.parametrize("test_case", EDGE_CASES)
    def test_edge_cases_bert(self, bert_model, test_case):
        """Test challenging edge cases with BERT."""
        similarity = self.compute_bert_similarity(bert_model, test_case)

        difficulty = test_case["difficulty"]
        description = test_case["description"]
        expected_match = test_case["expected_match"]

        print(f"\nBERT EDGE CASE {difficulty.upper()}: {description}")
        print(f"Expected: {expected_match}, Similarity: {similarity:.3f}")


class TestAccuracyMetrics:
    """Comprehensive accuracy evaluation across all test cases."""

    @pytest.fixture(scope="class")
    def bert_model(self):
        """Load BERT model once."""
        model = EntityMatchingModel()
        model.load_model()
        return model

    def evaluate_model(
        self,
        model: EntityMatchingModel,
        test_cases: List[Dict],
        threshold: float = 0.75,
    ) -> Dict:
        """
        Evaluate model performance on test cases.

        Returns:
            Dict with metrics: accuracy, precision, recall, f1, etc.
        """
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0

        results = []

        for test_case in test_cases:
            record_pair = create_record_pair_from_test_case(test_case)
            text_a = serialize_record_pair(record_pair, add_sep=False)[0]
            text_b = serialize_record_pair(record_pair, add_sep=False)[1]

            similarity, _, _ = model.compute_similarity(text_a, text_b)
            predicted_match = similarity >= threshold
            expected_match = test_case["expected_match"]

            results.append(
                {
                    "description": test_case["description"],
                    "difficulty": test_case["difficulty"],
                    "similarity": similarity,
                    "predicted": predicted_match,
                    "expected": expected_match,
                    "correct": predicted_match == expected_match,
                }
            )

            if expected_match and predicted_match:
                true_positives += 1
            elif expected_match and not predicted_match:
                false_negatives += 1
            elif not expected_match and predicted_match:
                false_positives += 1
            elif not expected_match and not predicted_match:
                true_negatives += 1

        # Calculate metrics
        total = len(test_cases)
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0
        )

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0
        )

        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "true_negatives": true_negatives,
            "false_negatives": false_negatives,
            "total": total,
            "results": results,
        }

    @pytest.mark.slow
    def test_overall_accuracy(self, bert_model):
        """Test overall accuracy across all test cases."""
        metrics = self.evaluate_model(bert_model, ALL_MATCHING_TEST_CASES)

        print("\n" + "=" * 80)
        print("OVERALL ACCURACY METRICS")
        print("=" * 80)
        print(f"Accuracy:  {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall:    {metrics['recall']:.3f}")
        print(f"F1 Score:  {metrics['f1']:.3f}")
        print(f"\nTrue Positives:  {metrics['true_positives']}")
        print(f"False Positives: {metrics['false_positives']}")
        print(f"True Negatives:  {metrics['true_negatives']}")
        print(f"False Negatives: {metrics['false_negatives']}")
        print(f"Total Cases:     {metrics['total']}")

        # Print failures
        print("\n" + "=" * 80)
        print("INCORRECT PREDICTIONS")
        print("=" * 80)
        for result in metrics["results"]:
            if not result["correct"]:
                print(f"\n{result['difficulty'].upper()}: {result['description']}")
                print(
                    f"  Expected: {result['expected']}, Predicted: {result['predicted']}"
                )
                print(f"  Similarity: {result['similarity']:.3f}")

    @pytest.mark.slow
    def test_accuracy_by_difficulty(self, bert_model):
        """Test accuracy broken down by difficulty level."""
        difficulties = ["easy", "medium", "hard", "very_hard"]

        print("\n" + "=" * 80)
        print("ACCURACY BY DIFFICULTY LEVEL")
        print("=" * 80)

        for difficulty in difficulties:
            test_cases = get_test_cases_by_difficulty(difficulty)
            if not test_cases:
                continue

            metrics = self.evaluate_model(bert_model, test_cases)

            print(f"\n{difficulty.upper()}:")
            print(f"  Accuracy:  {metrics['accuracy']:.3f}")
            print(f"  Precision: {metrics['precision']:.3f}")
            print(f"  Recall:    {metrics['recall']:.3f}")
            print(f"  F1 Score:  {metrics['f1']:.3f}")
            print(f"  Cases:     {metrics['total']}")

    @pytest.mark.slow
    def test_similarity_distribution(self, bert_model):
        """Analyze the distribution of similarity scores."""
        matches = get_expected_matches()
        non_matches = get_expected_non_matches()

        match_similarities = []
        for test_case in matches:
            record_pair = create_record_pair_from_test_case(test_case)
            text_a = serialize_record_pair(record_pair, add_sep=False)[0]
            text_b = serialize_record_pair(record_pair, add_sep=False)[1]
            similarity, _, _ = bert_model.compute_similarity(text_a, text_b)
            match_similarities.append(similarity)

        non_match_similarities = []
        for test_case in non_matches:
            record_pair = create_record_pair_from_test_case(test_case)
            text_a = serialize_record_pair(record_pair, add_sep=False)[0]
            text_b = serialize_record_pair(record_pair, add_sep=False)[1]
            similarity, _, _ = bert_model.compute_similarity(text_a, text_b)
            non_match_similarities.append(similarity)

        print("\n" + "=" * 80)
        print("SIMILARITY SCORE DISTRIBUTION")
        print("=" * 80)

        if match_similarities:
            print(f"\nMatching Pairs (n={len(match_similarities)}):")
            print(f"  Min:    {min(match_similarities):.3f}")
            print(f"  Max:    {max(match_similarities):.3f}")
            print(
                f"  Mean:   {sum(match_similarities) / len(match_similarities):.3f}"
            )
            print(f"  Median: {sorted(match_similarities)[len(match_similarities) // 2]:.3f}")

        if non_match_similarities:
            print(f"\nNon-Matching Pairs (n={len(non_match_similarities)}):")
            print(f"  Min:    {min(non_match_similarities):.3f}")
            print(f"  Max:    {max(non_match_similarities):.3f}")
            print(
                f"  Mean:   {sum(non_match_similarities) / len(non_match_similarities):.3f}"
            )
            print(
                f"  Median: {sorted(non_match_similarities)[len(non_match_similarities) // 2]:.3f}"
            )

        # Calculate optimal threshold (simple version)
        all_scores = sorted(
            [(s, True) for s in match_similarities]
            + [(s, False) for s in non_match_similarities]
        )

        best_threshold = 0.75
        best_f1 = 0.0

        for threshold in [i / 100 for i in range(50, 100)]:
            tp = sum(1 for s, is_match in all_scores if is_match and s >= threshold)
            fp = sum(1 for s, is_match in all_scores if not is_match and s >= threshold)
            fn = sum(1 for s, is_match in all_scores if is_match and s < threshold)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = (
                2 * (precision * recall) / (precision + recall)
                if (precision + recall) > 0
                else 0
            )

            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold

        print(f"\nOptimal Threshold: {best_threshold:.3f} (F1: {best_f1:.3f})")
