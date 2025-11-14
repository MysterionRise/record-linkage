"""Tests for ML model."""

import pytest
import torch
from app.ml.model import EntityMatchingModel, get_model


@pytest.mark.slow
def test_model_initialization():
    """Test model initialization."""
    model = EntityMatchingModel()
    assert model.model_name is not None
    assert model.device in ["cpu", "cuda"]
    assert model.is_loaded is False


@pytest.mark.slow
def test_model_loading():
    """Test model loading."""
    model = EntityMatchingModel()
    model.load_model()

    assert model.is_loaded is True
    assert model.model is not None


@pytest.mark.slow
def test_model_encoding():
    """Test text encoding."""
    model = EntityMatchingModel()
    model.load_model()

    texts = ["Hello world", "Test sentence"]
    embeddings = model.encode(texts)

    assert isinstance(embeddings, torch.Tensor)
    assert embeddings.shape[0] == 2  # Two texts
    assert embeddings.shape[1] > 0  # Embedding dimension


@pytest.mark.slow
def test_compute_similarity():
    """Test similarity computation."""
    model = EntityMatchingModel()
    model.load_model()

    text_a = "John Smith"
    text_b = "J. Smith"

    similarity, emb_a, emb_b = model.compute_similarity(text_a, text_b)

    assert isinstance(similarity, float)
    assert 0.0 <= similarity <= 1.0
    assert isinstance(emb_a, torch.Tensor)
    assert isinstance(emb_b, torch.Tensor)


@pytest.mark.slow
def test_predict_batch():
    """Test batch prediction."""
    model = EntityMatchingModel()
    model.load_model()

    text_pairs = [
        ("John Smith", "J. Smith"),
        ("Alice Johnson", "Bob Wilson"),
    ]

    similarities = model.predict_batch(text_pairs)

    assert len(similarities) == 2
    assert all(0.0 <= sim <= 1.0 for sim in similarities)


def test_get_model_singleton():
    """Test global model instance."""
    model1 = get_model()
    model2 = get_model()

    assert model1 is model2  # Same instance
