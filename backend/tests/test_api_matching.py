"""Tests for matching endpoints."""

import pytest


@pytest.mark.asyncio
async def test_predict_match(client, sample_record_pair):
    """Test record matching prediction."""
    response = client.post(
        "/api/v1/match/predict",
        json=sample_record_pair,
        params={"include_explanation": True, "explanation_method": "shap"},
    )

    assert response.status_code == 200
    data = response.json()

    # Check prediction structure
    assert "prediction" in data
    prediction = data["prediction"]
    assert "is_match" in prediction
    assert "match_probability" in prediction
    assert "confidence" in prediction
    assert "similarity_score" in prediction

    # Check value ranges
    assert 0.0 <= prediction["match_probability"] <= 1.0
    assert 0.0 <= prediction["similarity_score"] <= 1.0
    assert prediction["confidence"] in ["High", "Medium", "Low"]

    # Check explanation structure
    if data.get("explanation"):
        explanation = data["explanation"]
        assert "method" in explanation
        assert "feature_contributions" in explanation
        assert "top_positive_features" in explanation
        assert "top_negative_features" in explanation


@pytest.mark.asyncio
async def test_predict_match_without_explanation(client, sample_record_pair):
    """Test matching without explanation."""
    response = client.post(
        "/api/v1/match/predict",
        json=sample_record_pair,
        params={"include_explanation": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data


@pytest.mark.asyncio
async def test_batch_match(client, sample_records):
    """Test batch matching."""
    request = {
        "dataset_a": sample_records,
        "dataset_b": sample_records,
        "threshold": 0.75,
        "include_explanations": False,
    }

    response = client.post("/api/v1/match/batch", json=request)
    assert response.status_code == 200

    data = response.json()
    assert "total_comparisons" in data
    assert "matches_found" in data
    assert "match_results" in data
    assert "processing_time" in data

    assert isinstance(data["match_results"], list)
    assert data["total_comparisons"] >= 0
    assert data["matches_found"] >= 0


def test_optimize_threshold_not_implemented(client):
    """Test threshold optimization endpoint (not yet implemented)."""
    response = client.get(
        "/api/v1/match/threshold/optimize",
        params={"dataset_name": "test"},
    )
    assert response.status_code == 501  # Not implemented
