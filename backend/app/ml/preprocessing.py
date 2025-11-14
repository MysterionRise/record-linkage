"""Data preprocessing utilities for entity matching."""

from typing import Dict, List, Tuple
import re

from app.models.schemas import RecordBase, RecordPair


def serialize_record(record: RecordBase, fields_order: List[str] = None) -> str:
    """
    Serialize a record into a text string for BERT encoding.

    Args:
        record: Record to serialize
        fields_order: Optional order of fields (for consistency)

    Returns:
        str: Serialized record text
    """
    fields = record.fields

    if fields_order:
        # Use specified order
        ordered_fields = fields_order
    else:
        # Sort alphabetically for consistency
        ordered_fields = sorted(fields.keys())

    # Create field: value pairs
    parts = []
    for field in ordered_fields:
        if field in fields and fields[field]:
            value = str(fields[field]).strip()
            if value and value.lower() not in ["nan", "none", "null", ""]:
                parts.append(f"{field}: {value}")

    return " | ".join(parts)


def serialize_record_pair(record_pair: RecordPair, add_sep: bool = True) -> str:
    """
    Serialize a record pair for BERT encoding.

    Args:
        record_pair: Pair of records
        add_sep: Whether to add [SEP] token between records

    Returns:
        str: Serialized record pair
    """
    # Get consistent field order from both records
    all_fields = set(record_pair.record_a.fields.keys()) | set(record_pair.record_b.fields.keys())
    fields_order = sorted(all_fields)

    text_a = serialize_record(record_pair.record_a, fields_order)
    text_b = serialize_record(record_pair.record_b, fields_order)

    if add_sep:
        return f"{text_a} [SEP] {text_b}"
    else:
        return (text_a, text_b)


def normalize_text(text: str) -> str:
    """
    Normalize text for better matching.

    Args:
        text: Input text

    Returns:
        str: Normalized text
    """
    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove special characters (optional)
    # text = re.sub(r'[^\w\s]', '', text)

    return text


def extract_field_pairs(
    record_pair: RecordPair,
) -> List[Tuple[str, str, str]]:
    """
    Extract field-by-field pairs for comparison.

    Args:
        record_pair: Pair of records

    Returns:
        List of (field_name, value_a, value_b) tuples
    """
    fields_a = record_pair.record_a.fields
    fields_b = record_pair.record_b.fields

    all_fields = set(fields_a.keys()) | set(fields_b.keys())

    field_pairs = []
    for field in sorted(all_fields):
        value_a = fields_a.get(field, "")
        value_b = fields_b.get(field, "")
        field_pairs.append((field, str(value_a), str(value_b)))

    return field_pairs


def preprocess_dataset(records: List[RecordBase], normalize: bool = True) -> List[RecordBase]:
    """
    Preprocess a dataset of records.

    Args:
        records: List of records to preprocess
        normalize: Whether to normalize text

    Returns:
        List[RecordBase]: Preprocessed records
    """
    preprocessed = []

    for record in records:
        fields = record.fields.copy()

        if normalize:
            # Normalize all field values
            fields = {k: normalize_text(str(v)) for k, v in fields.items()}

        preprocessed.append(
            RecordBase(
                id=record.id,
                fields=fields,
            )
        )

    return preprocessed


def create_field_embeddings_text(record_pair: RecordPair) -> Dict[str, str]:
    """
    Create field-specific texts for embeddings.

    Args:
        record_pair: Pair of records

    Returns:
        Dict mapping field names to combined texts
    """
    field_texts = {}

    field_pairs = extract_field_pairs(record_pair)

    for field_name, value_a, value_b in field_pairs:
        if value_a or value_b:
            field_texts[field_name] = f"{value_a} [SEP] {value_b}"

    return field_texts
