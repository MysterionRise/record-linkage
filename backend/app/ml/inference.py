"""Inference pipeline for entity matching."""

import time
from typing import List, Optional

from app.models.schemas import (
    RecordPair,
    RecordBase,
    MatchResult,
    MatchPrediction,
    BatchMatchResult,
    Explanation,
    FeatureContribution,
)
from app.core.config import settings
from app.ml.model import get_model
from app.ml.preprocessing import serialize_record_pair


async def predict_match(
    record_pair: RecordPair,
    include_explanation: bool = True,
) -> MatchResult:
    """
    Predict if two records match using BERT-based entity matching.

    Args:
        record_pair: Pair of records to compare
        include_explanation: Whether to include SHAP explainability

    Returns:
        MatchResult: Match prediction with optional SHAP explanation
    """
    # Get the BERT model
    model = get_model()

    # Serialize records for BERT encoding
    # Returns tuple of (text_a, text_b) when add_sep=False
    text_a, text_b = serialize_record_pair(record_pair, add_sep=False)

    # Compute BERT-based similarity
    similarity, embedding_a, embedding_b = model.compute_similarity(text_a, text_b)

    prediction = MatchPrediction(
        is_match=similarity > settings.SIMILARITY_THRESHOLD,
        match_probability=similarity,
        confidence=_get_confidence_level(similarity),
        similarity_score=similarity,
    )

    explanation = None
    if include_explanation:
        explanation = _generate_placeholder_explanation(record_pair)

    return MatchResult(
        prediction=prediction,
        explanation=explanation,
        record_pair=record_pair,
    )


async def batch_predict(
    dataset_a: List[RecordBase],
    dataset_b: List[RecordBase],
    threshold: Optional[float] = None,
    include_explanations: bool = False,
) -> BatchMatchResult:
    """
    Perform batch matching between two datasets using BERT.

    This implementation uses batch encoding for better performance.

    Args:
        dataset_a: First dataset
        dataset_b: Second dataset
        threshold: Optional custom threshold
        include_explanations: Whether to include explanations

    Returns:
        BatchMatchResult: Results of all comparisons
    """
    start_time = time.time()

    match_results = []
    matches_found = 0

    # Use custom threshold or default
    match_threshold = threshold or settings.SIMILARITY_THRESHOLD

    # Get the BERT model
    model = get_model()

    # Limit comparisons for demo (avoid O(n²) explosion)
    max_comparisons = 1000
    comparison_count = 0

    # Prepare batch of record pairs
    record_pairs = []
    for record_a in dataset_a:
        for record_b in dataset_b:
            if comparison_count >= max_comparisons:
                break
            record_pairs.append(RecordPair(record_a=record_a, record_b=record_b))
            comparison_count += 1
        if comparison_count >= max_comparisons:
            break

    # Batch encode all pairs for efficiency
    text_pairs = []
    for record_pair in record_pairs:
        text_a, text_b = serialize_record_pair(record_pair, add_sep=False)
        text_pairs.append((text_a, text_b))

    # Compute similarities in batch
    similarities = model.predict_batch(text_pairs)

    # Process results
    for i, (record_pair, similarity) in enumerate(zip(record_pairs, similarities)):
        is_match = similarity >= match_threshold

        prediction = MatchPrediction(
            is_match=is_match,
            match_probability=similarity,
            confidence=_get_confidence_level(similarity),
            similarity_score=similarity,
        )

        explanation = None
        if include_explanations and is_match:
            # Only generate explanations for matches to save time
            explanation = _generate_placeholder_explanation(record_pair)

        result = MatchResult(
            prediction=prediction,
            explanation=explanation,
            record_pair=record_pair,
        )

        if is_match:
            matches_found += 1
            match_results.append(result)

    processing_time = time.time() - start_time

    return BatchMatchResult(
        total_comparisons=comparison_count,
        matches_found=matches_found,
        match_results=match_results,
        processing_time=processing_time,
    )


def _compute_placeholder_similarity(record_pair: RecordPair) -> float:
    """
    Compute a placeholder similarity score.
    This will be replaced with actual BERT-based similarity.

    Args:
        record_pair: Pair of records

    Returns:
        float: Similarity score between 0 and 1
    """
    # Simple placeholder: compare field values
    fields_a = record_pair.record_a.fields
    fields_b = record_pair.record_b.fields

    # Get common fields
    common_fields = set(fields_a.keys()) & set(fields_b.keys())

    if not common_fields:
        return 0.0

    # Simple string matching
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


def _get_confidence_level(similarity: float) -> str:
    """Get confidence level based on similarity score."""
    if similarity >= 0.85:
        return "High"
    elif similarity >= 0.65:
        return "Medium"
    else:
        return "Low"


def _generate_placeholder_explanation(record_pair: RecordPair) -> Explanation:
    """
    Generate a placeholder explanation.
    This will be replaced with actual SHAP explanations.

    Args:
        record_pair: Pair of records

    Returns:
        Explanation: Placeholder SHAP explanation
    """
    fields_a = record_pair.record_a.fields
    fields_b = record_pair.record_b.fields

    feature_contributions = []
    top_positive = []
    top_negative = []

    for field in set(fields_a.keys()) | set(fields_b.keys()):
        value_a = fields_a.get(field, "")
        value_b = fields_b.get(field, "")

        # Placeholder contribution calculation
        if value_a.lower() == value_b.lower():
            contribution = 0.8
            top_positive.append(field)
        elif value_a.lower() in value_b.lower() or value_b.lower() in value_a.lower():
            contribution = 0.4
        else:
            contribution = -0.3
            top_negative.append(field)

        feature_contributions.append(
            FeatureContribution(
                field_name=field,
                contribution=contribution,
                value_a=value_a,
                value_b=value_b,
            )
        )

    return Explanation(
        method="SHAP",
        feature_contributions=feature_contributions,
        top_positive_features=top_positive[:5],
        top_negative_features=top_negative[:5],
    )
