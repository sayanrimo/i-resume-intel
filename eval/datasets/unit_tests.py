# eval/unit_tests.py
import pytest
from pathlib import Path
from core.ingestion import load_resume
from core.nlp_extract import extract_entities

# Note: These tests require sample files in a 'tests/data' directory.
# For simplicity, we are checking for basic functionality.

def test_extract_entities_basic():
    """Tests basic entity extraction."""
    text = "John Doe is a Python developer. His email is test@example.com."
    entities = extract_entities(text)
    assert entities["name"] == "John Doe"
    assert entities["email"] == "test@example.com"
    assert "Python" in [skill['name'] for skill in entities["skills"]]

def test_empty_text_ingestion():
    """Tests that ingestion handles empty or invalid files gracefully."""
    # Create a dummy empty file for testing
    Path("data/uploads/empty.pdf").touch()
    result = load_resume("data/uploads/empty.pdf")
    # A more robust check would mock pypdf, but this checks the handler
    assert result == {} or result.get("text") == ""

def test_unsupported_file_ingestion():
    """Tests ingestion of an unsupported file type."""
    Path("data/uploads/test.txt").touch()
    result = load_resume("data/uploads/test.txt")
    assert result == {}