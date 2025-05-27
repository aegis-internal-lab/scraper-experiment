import pytest
from unittest.mock import Mock, patch

from scraper.libs.utils import validate_url, truncate_string


class TestUtils:
    """Test cases for utility functions"""

    def test_validate_url_valid_http(self):
        """Test validating a valid HTTP URL"""
        assert validate_url("http://example.com") is True

    def test_validate_url_valid_https(self):
        """Test validating a valid HTTPS URL"""
        assert validate_url("https://example.com") is True

    def test_validate_url_invalid_no_protocol(self):
        """Test validating an invalid URL without protocol"""
        assert validate_url("example.com") is False

    def test_validate_url_empty(self):
        """Test validating an empty URL"""
        assert validate_url("") is False

    def test_validate_url_none(self):
        """Test validating a None URL"""
        assert validate_url(None) is False

    def test_truncate_string_short(self):
        """Test truncating a string shorter than max length"""
        result = truncate_string("short", 10)
        assert result == "short"

    def test_truncate_string_long(self):
        """Test truncating a string longer than max length"""
        result = truncate_string("this is a very long string", 10)
        assert result == "this is a ..."

    def test_truncate_string_exact_length(self):
        """Test truncating a string of exact max length"""
        result = truncate_string("exactly10c", 10)
        assert result == "exactly10c"
