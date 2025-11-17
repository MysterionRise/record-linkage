"""
Comprehensive test cases for entity matching using real-world examples.

These test cases represent actual challenges in record linkage:
- Name variations (abbreviations, nicknames, different formats)
- Typos and OCR errors
- Missing or incomplete data
- Transliterations
- Product variations
- Address variations
"""

# Test cases are organized by difficulty level and matching type

PERSON_NAME_MATCHES = [
    # Easy cases - should definitely match
    {
        "record_a": {"name": "John Smith", "age": "45", "city": "New York"},
        "record_b": {"name": "John Smith", "age": "45", "city": "New York"},
        "expected_match": True,
        "difficulty": "easy",
        "description": "Exact match",
    },
    {
        "record_a": {"name": "John F. Kennedy", "birth_year": "1917"},
        "record_b": {"name": "John Fitzgerald Kennedy", "birth_year": "1917"},
        "expected_match": True,
        "difficulty": "easy",
        "description": "Full name vs abbreviated middle name",
    },
    # Medium cases - common variations
    {
        "record_a": {"name": "Robert Smith", "address": "123 Main St"},
        "record_b": {"name": "Bob Smith", "address": "123 Main Street"},
        "expected_match": True,
        "difficulty": "medium",
        "description": "Nickname variation (Robert->Bob) + address abbreviation",
    },
    {
        "record_a": {"name": "William Johnson Jr.", "phone": "555-1234"},
        "record_b": {"name": "Bill Johnson", "phone": "5551234"},
        "expected_match": True,
        "difficulty": "medium",
        "description": "Nickname + suffix difference + phone format",
    },
    {
        "record_a": {"name": "Mary Anne Thompson", "email": "mthompson@email.com"},
        "record_b": {"name": "Mary-Anne Thompson", "email": "mary.thompson@email.com"},
        "expected_match": True,
        "difficulty": "medium",
        "description": "Hyphenation difference + email variation",
    },
    {
        "record_a": {"first_name": "James", "last_name": "O'Brien", "ssn": "123-45-6789"},
        "record_b": {"first_name": "James", "last_name": "OBrien", "ssn": "123456789"},
        "expected_match": True,
        "difficulty": "medium",
        "description": "Apostrophe handling + SSN format",
    },
    # Hard cases - subtle variations
    {
        "record_a": {"name": "José García", "city": "Madrid"},
        "record_b": {"name": "Jose Garcia", "city": "Madrid"},
        "expected_match": True,
        "difficulty": "hard",
        "description": "Diacritics (accents) removed",
    },
    {
        "record_a": {"name": "Catherine Miller", "dob": "1985-03-15"},
        "record_b": {"name": "Katharine Miller", "dob": "03/15/1985"},
        "expected_match": True,
        "difficulty": "hard",
        "description": "Spelling variation (Catherine/Katharine) + date format",
    },
    {
        "record_a": {"name": "Dr. Sarah Johnson", "title": "Professor"},
        "record_b": {"name": "Sarah Johnson PhD", "title": "Prof."},
        "expected_match": True,
        "difficulty": "hard",
        "description": "Title variations (Dr. vs PhD, Professor vs Prof.)",
    },
    {
        "record_a": {"name": "李明", "name_en": "Li Ming"},
        "record_b": {"name": "Ming Li", "origin": "China"},
        "expected_match": True,
        "difficulty": "hard",
        "description": "Chinese name - different ordering (family first vs last)",
    },
    # Very hard cases - typos and OCR errors
    {
        "record_a": {"name": "Christopher Anderson", "address": "456 Oak Avenue"},
        "record_b": {"name": "Chistopher Anderson", "address": "456 0ak Avenue"},
        "expected_match": True,
        "difficulty": "very_hard",
        "description": "Typo (missing 'r') + OCR error (O->0)",
    },
    {
        "record_a": {"name": "Elizabeth Williams", "phone": "555-7890"},
        "record_b": {"name": "Elizabth Williams", "phone": "555-7890"},
        "expected_match": True,
        "difficulty": "very_hard",
        "description": "Single character missing",
    },
]

PERSON_NAME_NON_MATCHES = [
    # Clear non-matches
    {
        "record_a": {"name": "John Smith", "age": "45"},
        "record_b": {"name": "Jane Doe", "age": "32"},
        "expected_match": False,
        "difficulty": "easy",
        "description": "Different people entirely",
    },
    {
        "record_a": {"name": "Michael Brown", "city": "Boston"},
        "record_b": {"name": "Michael Brown", "city": "Seattle"},
        "expected_match": False,
        "difficulty": "medium",
        "description": "Same name, different city (common name collision)",
    },
    {
        "record_a": {"name": "John Smith", "birth_year": "1980"},
        "record_b": {"name": "John Smith", "birth_year": "1990"},
        "expected_match": False,
        "difficulty": "medium",
        "description": "Same name, different birth year",
    },
    {
        "record_a": {"name": "David Lee", "email": "david.lee1@email.com"},
        "record_b": {"name": "David Lee", "email": "david.lee2@email.com"},
        "expected_match": False,
        "difficulty": "hard",
        "description": "Same name, similar but different emails",
    },
]

PUBLICATION_MATCHES = [
    # Academic publication matching
    {
        "record_a": {
            "title": "Deep Learning for Entity Matching: A Design Space Exploration",
            "authors": "Sidharth Mudgal, Han Li, Theodoros Rekatsinas",
            "venue": "SIGMOD",
            "year": "2018",
        },
        "record_b": {
            "title": "Deep Learning for Entity Matching",
            "authors": "S. Mudgal, H. Li, T. Rekatsinas",
            "venue": "SIGMOD Conference",
            "year": "2018",
        },
        "expected_match": True,
        "difficulty": "medium",
        "description": "Shortened title + abbreviated authors + venue variation",
    },
    {
        "record_a": {
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
            "venue": "NAACL",
            "year": "2019",
        },
        "record_b": {
            "title": "BERT Pre-training of Deep Bidirectional Transformers",
            "authors": "J. Devlin, M.-W. Chang, K. Lee, K. Toutanova",
            "venue": "NAACL-HLT",
            "year": "2019",
        },
        "expected_match": True,
        "difficulty": "medium",
        "description": "Truncated title + author abbreviations + venue variation",
    },
    {
        "record_a": {
            "title": "Attention Is All You Need",
            "authors": "Vaswani et al.",
            "venue": "NeurIPS",
            "year": "2017",
        },
        "record_b": {
            "title": "Attention is All You Need",
            "authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar",
            "venue": "NIPS",
            "year": "2017",
        },
        "expected_match": True,
        "difficulty": "hard",
        "description": "Capitalization + et al. vs full authors + venue name change (NIPS->NeurIPS)",
    },
]

PRODUCT_MATCHES = [
    # E-commerce product matching
    {
        "record_a": {
            "title": "Apple iPhone 13 Pro Max 256GB Sierra Blue",
            "brand": "Apple",
            "price": "1099.00",
            "category": "Electronics > Cell Phones",
        },
        "record_b": {
            "title": "iPhone 13 Pro Max - 256GB - Blue",
            "brand": "Apple",
            "price": "1099",
            "category": "Cell Phones & Smartphones",
        },
        "expected_match": True,
        "difficulty": "medium",
        "description": "Different title format + color variation + price format + category format",
    },
    {
        "record_a": {
            "title": "Sony WH-1000XM4 Wireless Noise-Canceling Over-Ear Headphones - Black",
            "brand": "Sony",
            "model": "WH1000XM4",
            "price": "349.99",
        },
        "record_b": {
            "title": "Sony WH1000XM4 Noise Cancelling Headphones",
            "brand": "Sony",
            "model": "WH-1000XM4",
            "price": "$348.00",
        },
        "expected_match": True,
        "difficulty": "medium",
        "description": "Hyphen variation in model + price difference + currency symbol",
    },
    {
        "record_a": {
            "title": 'Samsung 65" Class QLED Q80A Series 4K UHD Smart TV',
            "brand": "Samsung",
            "screen_size": "65 inch",
            "model": "QN65Q80AAFXZA",
        },
        "record_b": {
            "title": "Samsung Q80A 65 inch QLED 4K Smart TV",
            "brand": "Samsung",
            "screen_size": '65"',
            "model": "Q80A",
        },
        "expected_match": True,
        "difficulty": "hard",
        "description": "Different title order + screen size format + model number variation",
    },
]

ADDRESS_MATCHES = [
    # Address matching
    {
        "record_a": {
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
        },
        "record_b": {
            "address": "123 Main St.",
            "city": "New York",
            "state": "New York",
            "zip": "10001-1234",
        },
        "expected_match": True,
        "difficulty": "easy",
        "description": "Street abbreviation + state format + ZIP+4",
    },
    {
        "record_a": {
            "address": "456 North Oak Avenue, Apartment 2B",
            "city": "Chicago",
            "state": "IL",
        },
        "record_b": {
            "address": "456 N Oak Ave Apt 2B",
            "city": "Chicago",
            "state": "Illinois",
        },
        "expected_match": True,
        "difficulty": "medium",
        "description": "Direction abbreviation + street type + apartment format",
    },
]

# Challenging edge cases
EDGE_CASES = [
    # Empty or minimal fields
    {
        "record_a": {"name": "John Smith"},
        "record_b": {"name": "John Smith", "age": "", "address": ""},
        "expected_match": True,
        "difficulty": "medium",
        "description": "Missing/empty fields on one side",
    },
    # Field order shouldn't matter
    {
        "record_a": {"first_name": "Alice", "last_name": "Johnson", "age": "30"},
        "record_b": {"age": "30", "last_name": "Johnson", "first_name": "Alice"},
        "expected_match": True,
        "difficulty": "easy",
        "description": "Same data, different field order",
    },
    # Multiple small differences
    {
        "record_a": {
            "name": "Dr. Robert J. Williams III",
            "address": "789 South Elm Street",
            "phone": "(555) 123-4567",
        },
        "record_b": {
            "name": "Robert Williams",
            "address": "789 S. Elm St.",
            "phone": "555-123-4567",
        },
        "expected_match": True,
        "difficulty": "very_hard",
        "description": "Multiple differences: title, middle initial, suffix, address abbreviations, phone format",
    },
]

# Combine all test cases
ALL_MATCHING_TEST_CASES = (
    PERSON_NAME_MATCHES
    + PERSON_NAME_NON_MATCHES
    + PUBLICATION_MATCHES
    + PRODUCT_MATCHES
    + ADDRESS_MATCHES
    + EDGE_CASES
)


def get_test_cases_by_difficulty(difficulty: str):
    """Get test cases filtered by difficulty level."""
    return [tc for tc in ALL_MATCHING_TEST_CASES if tc.get("difficulty") == difficulty]


def get_expected_matches():
    """Get only the cases that should match."""
    return [tc for tc in ALL_MATCHING_TEST_CASES if tc.get("expected_match") is True]


def get_expected_non_matches():
    """Get only the cases that should not match."""
    return [tc for tc in ALL_MATCHING_TEST_CASES if tc.get("expected_match") is False]
