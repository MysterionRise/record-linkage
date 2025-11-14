"""Tests for ML preprocessing utilities."""

import pytest
from app.ml.preprocessing import (
    serialize_record,
    serialize_record_pair,
    normalize_text,
    extract_field_pairs,
    preprocess_dataset,
)
from app.models.schemas import RecordBase, RecordPair


def test_serialize_record():
    """Test record serialization."""
    record = RecordBase(
        id="1",
        fields={
            "name": "John Smith",
            "address": "123 Main St",
            "city": "New York",
        },
    )

    serialized = serialize_record(record)
    assert isinstance(serialized, str)
    assert "John Smith" in serialized
    assert "123 Main St" in serialized
    assert "New York" in serialized
    assert " | " in serialized  # Check separator


def test_serialize_record_with_field_order():
    """Test record serialization with specific field order."""
    record = RecordBase(
        fields={"name": "Alice", "email": "alice@example.com"}
    )

    serialized = serialize_record(record, fields_order=["email", "name"])
    # Email should come before name
    email_pos = serialized.find("email")
    name_pos = serialized.find("name")
    assert email_pos < name_pos


def test_normalize_text():
    """Test text normalization."""
    text = "  Hello   World  "
    normalized = normalize_text(text)
    assert normalized == "hello world"

    text_with_special = "Test\n\tMultiple   Spaces"
    normalized = normalize_text(text_with_special)
    assert normalized == "test multiple spaces"


def test_extract_field_pairs():
    """Test field pair extraction."""
    record_pair = RecordPair(
        record_a=RecordBase(fields={"name": "John", "age": "30"}),
        record_b=RecordBase(fields={"name": "Jon", "city": "NYC"}),
    )

    field_pairs = extract_field_pairs(record_pair)

    assert len(field_pairs) == 3  # age, city, name (sorted)
    assert all(len(pair) == 3 for pair in field_pairs)  # (field, val_a, val_b)

    # Check that all fields are present
    fields = [pair[0] for pair in field_pairs]
    assert "name" in fields
    assert "age" in fields
    assert "city" in fields


def test_preprocess_dataset():
    """Test dataset preprocessing."""
    records = [
        RecordBase(fields={"name": "  John  ", "city": "NYC"}),
        RecordBase(fields={"name": "Alice", "city": "  Boston  "}),
    ]

    preprocessed = preprocess_dataset(records, normalize=True)

    assert len(preprocessed) == 2
    assert preprocessed[0].fields["name"] == "john"
    assert preprocessed[0].fields["city"] == "nyc"
    assert preprocessed[1].fields["name"] == "alice"
    assert preprocessed[1].fields["city"] == "boston"


def test_serialize_record_pair():
    """Test record pair serialization."""
    record_pair = RecordPair(
        record_a=RecordBase(fields={"name": "John Smith"}),
        record_b=RecordBase(fields={"name": "J. Smith"}),
    )

    serialized = serialize_record_pair(record_pair, add_sep=True)
    assert isinstance(serialized, str)
    assert "[SEP]" in serialized
    assert "John Smith" in serialized
    assert "J. Smith" in serialized
