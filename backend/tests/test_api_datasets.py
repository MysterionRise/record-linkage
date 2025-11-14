"""Tests for dataset endpoints."""

import pytest


def test_list_datasets(client):
    """Test listing datasets."""
    response = client.get("/api/v1/datasets/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Check structure of dataset info
    if len(data) > 0:
        dataset = data[0]
        assert "name" in dataset
        assert "description" in dataset
        assert "num_records" in dataset
        assert "fields" in dataset


def test_get_dataset_info_not_found(client):
    """Test getting info for non-existent dataset."""
    response = client.get("/api/v1/datasets/nonexistent_dataset")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
