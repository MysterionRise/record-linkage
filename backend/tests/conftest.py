"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_record_pair():
    """Sample record pair for testing."""
    return {
        "record_a": {
            "fields": {
                "name": "John Smith",
                "address": "123 Main St",
                "city": "New York",
                "phone": "555-1234",
            }
        },
        "record_b": {
            "fields": {
                "name": "J. Smith",
                "address": "123 Main Street",
                "city": "New York",
                "phone": "5551234",
            }
        },
    }


@pytest.fixture
def sample_records():
    """Sample records for testing."""
    return [
        {
            "id": "1",
            "fields": {
                "name": "Alice Johnson",
                "email": "alice@example.com",
            },
        },
        {
            "id": "2",
            "fields": {
                "name": "Bob Wilson",
                "email": "bob@example.com",
            },
        },
    ]
