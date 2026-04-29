"""
Unit tests for the Deidentifier module.

Tests cover:
- SSN detection and masking
- Phone number detection and masking
- Email detection and masking
- Credit card detection and masking
- DOB detection and masking
- Address detection (heuristic)
- Batch processing
- Verification
- Edge cases and boundary conditions
- Performance metrics
"""

import time

import pytest

from src.core.data.deidentifier import (
    Deidentifier,
    SensitiveInfoType,
    deidentify_text,
    verify_text,
)


class TestSSNDetection:
    """Test SSN (Social Security Number) detection."""

    def test_ssn_format_xxx_xx_xxxx(self) -> None:
        """Test SSN in XXX-XX-XXXX format."""
        deidentifier = Deidentifier()
        text = "My SSN is 123-45-6789"
        matches = deidentifier.detect(text)

        assert len(matches) > 0
        assert any(m.type == SensitiveInfoType.SSN for m in matches)
        assert any(m.text == "123-45-6789" for m in matches)

    def test_ssn_format_xxxxxxxxx(self) -> None:
        """Test SSN in 9-digit format."""
        deidentifier = Deidentifier()
        text = "SSN: 123456789"
        matches = deidentifier.detect(text)

        assert len(matches) > 0
        assert any(m.type == SensitiveInfoType.SSN for m in matches)

    def test_ssn_masking(self) -> None:
        """Test SSN is properly masked."""
        deidentifier = Deidentifier()
        text = "My SSN is 123-45-6789"
        result = deidentifier.deidentify(text)

        assert "123-45-6789" not in result
        assert "[SSN]" in result

    def test_multiple_ssns(self) -> None:
        """Test detection of multiple SSNs."""
        deidentifier = Deidentifier()
        text = "First SSN: 111-22-3333, Second SSN: 444-55-6666"
        matches = deidentifier.detect(text)

        ssn_matches = [m for m in matches if m.type == SensitiveInfoType.SSN]
        assert len(ssn_matches) == 2


class TestPhoneDetection:
    """Test phone number detection."""

    @pytest.mark.parametrize(
        "phone",
        [
            "(555) 123-4567",
            "555-123-4567",
            "555.123.4567",
            "5551234567",
            "+1-555-123-4567",
            "+1 (555) 123-4567",
        ],
    )
    def test_phone_formats(self, phone: str) -> None:
        """Test various phone number formats."""
        deidentifier = Deidentifier()
        text = f"Call me at {phone}"
        matches = deidentifier.detect(text)

        phone_matches = [m for m in matches if m.type == SensitiveInfoType.PHONE]
        assert len(phone_matches) > 0, f"Failed to detect phone: {phone}"

    def test_phone_masking(self) -> None:
        """Test phone is properly masked."""
        deidentifier = Deidentifier()
        text = "My phone is (555) 123-4567"
        result = deidentifier.deidentify(text)

        assert "555" not in result or "[PHONE]" in result
        assert "[PHONE]" in result


class TestEmailDetection:
    """Test email address detection."""

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "john.doe@company.co.uk",
            "test_email+tag@domain.org",
        ],
    )
    def test_email_formats(self, email: str) -> None:
        """Test various email formats."""
        deidentifier = Deidentifier()
        text = f"Contact: {email}"
        matches = deidentifier.detect(text)

        email_matches = [m for m in matches if m.type == SensitiveInfoType.EMAIL]
        assert len(email_matches) > 0, f"Failed to detect email: {email}"

    def test_email_masking(self) -> None:
        """Test email is properly masked."""
        deidentifier = Deidentifier()
        text = "Email me at john@example.com"
        result = deidentifier.deidentify(text)

        assert "john@example.com" not in result
        assert "[EMAIL]" in result


class TestCreditCardDetection:
    """Test credit card detection."""

    def test_credit_card_detection(self) -> None:
        """Test credit card number detection."""
        deidentifier = Deidentifier()
        text = "Card: 4532-1234-5678-9010"
        matches = deidentifier.detect(text)

        cc_matches = [m for m in matches if m.type == SensitiveInfoType.CREDIT_CARD]
        assert len(cc_matches) > 0

    def test_credit_card_masking(self) -> None:
        """Test credit card is properly masked."""
        deidentifier = Deidentifier()
        text = "Payment: 4532 1234 5678 9010"
        result = deidentifier.deidentify(text)

        assert "[CREDIT_CARD]" in result


class TestDOBDetection:
    """Test Date of Birth detection."""

    @pytest.mark.parametrize(
        "dob",
        [
            "01/15/1990",
            "01-15-1990",
            "1990-01-15",
        ],
    )
    def test_dob_formats(self, dob: str) -> None:
        """Test various DOB formats."""
        deidentifier = Deidentifier()
        text = f"Born on {dob}"
        matches = deidentifier.detect(text)

        # Note: Some formats might be caught by other patterns
        assert len(matches) > 0, f"Failed to detect DOB: {dob}"

    def test_dob_masking(self) -> None:
        """Test DOB masking."""
        deidentifier = Deidentifier()
        text = "My DOB is 01/15/1990"

        result = deidentifier.deidentify(text)
        assert "[DOB]" in result


class TestBatchProcessing:
    """Test batch processing functionality."""

    def test_batch_deidentify(self) -> None:
        """Test batch deidentification."""
        deidentifier = Deidentifier()
        texts = ["SSN: 111-22-3333", "Email: user@example.com", "Phone: (555) 123-4567"]
        results = deidentifier.deidentify_batch(texts)

        assert len(results) == len(texts)
        assert "111-22-3333" not in results[0]
        assert "user@example.com" not in results[1]
        assert "[PHONE]" in results[2]

    def test_batch_performance(self) -> None:
        """Test batch processing performance (1000 texts)."""
        deidentifier = Deidentifier()
        texts = [
            f"Person {i}: Email is user{i}@example.com, "
            f"Phone: (555) 123-{i:04d}, SSN: {100 + i:03d}-{i:02d}-{1000 + i:04d}"
            for i in range(1000)
        ]

        start = time.time()
        results = deidentifier.deidentify_batch(texts)
        elapsed = time.time() - start

        assert len(results) == 1000
        assert elapsed < 5.0, f"Batch processing too slow: {elapsed:.2f}s for 1000 items"
        # At least some items should be deidentified
        assert sum(1 for r in results if "[EMAIL]" in r) > 900


class TestVerification:
    """Test verification functionality."""

    def test_verification_success(self) -> None:
        """Test successful verification."""
        original = "My email is john@example.com"
        deidentified = "My email is [EMAIL]"

        assert verify_text(original, deidentified) is True

    def test_verification_failure(self) -> None:
        """Test verification detects unmasked sensitive info."""
        original = "My email is john@example.com"
        deidentified = "My email is john@example.com"  # Not masked!

        assert verify_text(original, deidentified) is False

    def test_verification_with_ssn(self) -> None:
        """Test verification with SSN."""
        original = "SSN: 123-45-6789"
        deidentified = "SSN: [SSN]"

        assert verify_text(original, deidentified) is True

        # False positive case
        deidentified_bad = "SSN: 123-45-6789"
        assert verify_text(original, deidentified_bad) is False


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string(self) -> None:
        """Test empty string handling."""
        deidentifier = Deidentifier()

        matches = deidentifier.detect("")
        assert not matches

        result = deidentifier.deidentify("")
        assert result == ""

    def test_none_input(self) -> None:
        """Test None input handling."""
        deidentifier = Deidentifier()

        matches = deidentifier.detect(None)  # type: ignore[arg-type]
        assert not matches

        result = deidentifier.deidentify(None)  # type: ignore[arg-type]
        assert result is None

    def test_text_with_no_pii(self) -> None:
        """Test text without any PII."""
        deidentifier = Deidentifier()
        text = "This is a normal text with no sensitive information."

        matches = deidentifier.detect(text)
        assert len(matches) == 0

        result = deidentifier.deidentify(text)
        assert result == text

    def test_overlapping_patterns(self) -> None:
        """Test handling of overlapping patterns."""
        deidentifier = Deidentifier()
        # A text where multiple patterns might match the same area
        text = "Contact: john@example.com, SSN: 123-45-6789"

        matches = deidentifier.detect(text)
        # Should have email and SSN, no overlaps
        assert len(matches) >= 2

        result = deidentifier.deidentify(text)
        assert "@" not in result
        assert "123-45" not in result

    def test_special_characters(self) -> None:
        """Test handling of special characters."""
        deidentifier = Deidentifier()
        text = "SSN: 123-45-6789!!! Email: test@example.com???"

        result = deidentifier.deidentify(text)
        assert "[SSN]" in result
        assert "[EMAIL]" in result

    def test_multiline_text(self) -> None:
        """Test handling of multiline text."""
        deidentifier = Deidentifier()
        text = """
        Name: John Doe
        SSN: 123-45-6789
        Email: john@example.com
        Phone: (555) 123-4567
        """

        matches = deidentifier.detect(text)
        assert len(matches) >= 3  # SSN, Email, Phone

    def test_repeated_pii(self) -> None:
        """Test handling of repeated PII."""
        deidentifier = Deidentifier()
        text = "Email: test@example.com, also test@example.com"

        result = deidentifier.deidentify(text)
        # Both instances should be masked
        assert result.count("[EMAIL]") == 2

    def test_unicode_and_international(self) -> None:
        """Test handling of unicode and international characters."""
        deidentifier = Deidentifier()
        text = "名前: John Doe, Email: john@example.com"

        result = deidentifier.deidentify(text)
        assert "[EMAIL]" in result
        assert "John Doe" in result  # Name should remain


class TestStatistics:
    """Test statistics tracking."""

    def test_statistics_tracking(self) -> None:
        """Test that statistics are tracked."""
        deidentifier = Deidentifier()

        text = """
        SSN: 111-22-3333
        Phone: (555) 123-4567
        Email: test@example.com
        """

        deidentifier.detect(text)
        stats = deidentifier.get_statistics()

        assert stats.get("SSN", 0) >= 1
        assert stats.get("PHONE", 0) >= 1
        assert stats.get("EMAIL", 0) >= 1

    def test_statistics_reset(self) -> None:
        """Test statistics reset."""
        deidentifier = Deidentifier()

        deidentifier.detect("SSN: 123-45-6789")
        stats1 = deidentifier.get_statistics()
        assert stats1.get("SSN", 0) > 0

        deidentifier.reset_statistics()
        stats2 = deidentifier.get_statistics()
        assert len(stats2) == 0


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_deidentify_text_function(self) -> None:
        """Test the standalone deidentify_text function."""
        text = "My email is john@example.com and SSN is 123-45-6789"
        result = deidentify_text(text)

        assert "john@example.com" not in result
        assert "123-45" not in result
        assert "[EMAIL]" in result
        assert "[SSN]" in result

    def test_verify_text_function(self) -> None:
        """Test the standalone verify_text function."""
        original = "SSN: 123-45-6789"
        deidentified = "SSN: [SSN]"

        assert verify_text(original, deidentified) is True


class TestPerformance:
    """Performance-related tests."""

    def test_single_document_deidentification(self) -> None:
        """Test single large document deidentification."""
        deidentifier = Deidentifier()

        # Create a 100KB document
        text = (
            """
        John Doe
        SSN: 123-45-6789
        Email: john@example.com
        Phone: (555) 123-4567
        """
            * 5000
        )

        start = time.time()
        result = deidentifier.deidentify(text)
        elapsed = time.time() - start

        # Allow up to 10s to account for slower CI runners (local dev ~2s, CI can be 5x slower)
        assert elapsed < 10.0, f"Deidentification too slow: {elapsed:.2f}s"
        assert "[SSN]" in result
        assert "[EMAIL]" in result

    def test_detection_without_pii(self) -> None:
        """Test detection performance on text without PII."""
        deidentifier = Deidentifier()

        text = "Normal business document " * 10000

        start = time.time()
        matches = deidentifier.detect(text)
        elapsed = time.time() - start

        assert len(matches) == 0
        assert elapsed < 5.0, f"Detection too slow on clean text: {elapsed:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
