"""
VedaAide Data Deidentification Tool - Usage Guide

This module provides comprehensive PII (Personally Identifiable Information) masking
for the VedaAide recruitment interview system.
"""

import logging
import sys
import time
from pathlib import Path

from src.core.retrieval.deidentifier import (
    Deidentifier,
    SensitiveInfoType,
    deidentify_text,
    verify_text,
)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger(__name__)


def example_basic_usage() -> None:
    """Basic usage example."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 1: Basic Deidentification")
    logger.info("=" * 60)

    deidentifier = Deidentifier()

    text = """
    John Doe has been with the company for 5 years.
    His contact information:
    - Email: john.doe@example.com
    - Phone: (555) 123-4567
    - SSN: 123-45-6789
    """

    logger.info("Original text:")
    logger.info(text)

    deidentified = deidentifier.deidentify(text)
    logger.info("Deidentified text:")
    logger.info(deidentified)

    # Verify deidentification
    is_safe = deidentifier.verify_deidentification(text, deidentified)
    result_str = "✓ SAFE" if is_safe else "✗ UNSAFE"
    logger.info("Verification result: %s", result_str)


def example_batch_processing() -> None:
    """Batch processing example."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 2: Batch Processing")
    logger.info("=" * 60)

    deidentifier = Deidentifier()

    # 5 candidate resumes
    resumes = [
        "Resume 1: Alice Smith, Email: alice@example.com, SSN: 111-22-3333",
        "Resume 2: Bob Johnson, Phone: (555) 222-2222, Email: bob@example.com",
        "Resume 3: Carol White, SSN: 333-44-5555, Phone: (555) 333-3333",
        "Resume 4: David Brown, Email: david@example.com, SSN: 444-55-6666",
        "Resume 5: Eve Davis, Phone: (555) 555-5555, Email: eve@example.com",
    ]

    logger.info("Processing %d resumes...", len(resumes))

    deidentified_resumes = deidentifier.deidentify_batch(resumes)

    logger.info("Deidentified resumes:")
    for i, deidentified in enumerate(deidentified_resumes, 1):
        logger.info("%d. %s...", i, deidentified[:60])

    # Statistics
    stats = deidentifier.get_statistics()
    logger.info("Detection statistics:")
    for info_type, count in stats.items():
        logger.info("  - %s: %d", info_type, count)


def example_detection_details() -> None:
    """Example showing detection details."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 3: Detection Details")
    logger.info("=" * 60)

    deidentifier = Deidentifier()

    text = """
    Contact Information:
    - Card: 4532-1234-5678-9010
    - DOB: 01/15/1990
    - Work Phone: (555) 999-8888
    """

    logger.info("Text to analyze:")
    logger.info(text)

    matches = deidentifier.detect(text)

    logger.info("Found %d sensitive information(s):", len(matches))
    for i, match in enumerate(matches, 1):
        logger.info("  %d. Type: %s", i, match.type.value)
        logger.info("     Text: %s", match.text)
        logger.info("     Position: %d-%d", match.start, match.end)
        logger.info("     Mask: %s", match.mask)


def example_custom_masks() -> None:
    """Example with custom mask templates."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 4: Custom Mask Templates")
    logger.info("=" * 60)

    custom_masks = {
        SensitiveInfoType.SSN: "[REDACTED_SSN]",
        SensitiveInfoType.EMAIL: "[REDACTED_EMAIL]",
        SensitiveInfoType.PHONE: "[REDACTED_PHONE]",
    }

    deidentifier = Deidentifier(mask_template=custom_masks)

    text = "Contact john@example.com or (555) 123-4567. SSN: 123-45-6789"
    result = deidentifier.deidentify(text)

    logger.info("Original: %s", text)
    logger.info("With custom masks: %s", result)


def example_verification() -> None:
    """Example of verification."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 5: Verification - Success and Failure")
    logger.info("=" * 60)

    # Success case
    logger.info("SUCCESS CASE:")
    original = "My email is alice@example.com and SSN is 123-45-6789"
    deidentified = "My email is [EMAIL] and SSN is [SSN]"

    result = verify_text(original, deidentified)
    logger.info("Original: %s", original)
    logger.info("Deidentified: %s", deidentified)
    result_str = "✓ PASS" if result else "✗ FAIL"
    logger.info("Verification: %s", result_str)

    # Failure case
    logger.info("FAILURE CASE (NOT PROPERLY MASKED):")
    original2 = "SSN: 123-45-6789"
    deidentified2 = "SSN: 123-45-6789"

    result2 = verify_text(original2, deidentified2)
    logger.info("Original: %s", original2)
    logger.info("Deidentified: %s", deidentified2)
    result2_str = "✓ PASS" if result2 else "✗ FAIL"
    logger.info("Verification: %s", result2_str)


def example_convenience_functions() -> None:
    """Example using convenience functions."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 6: Convenience Functions")
    logger.info("=" * 60)

    text = "Contact John at john@example.com or (555) 123-4567"

    # Simple one-liner
    deidentified = deidentify_text(text)

    logger.info("Original: %s", text)
    logger.info("Deidentified: %s", deidentified)


def example_performance() -> None:
    """Example showing performance characteristics."""
    logger.info("=" * 60)
    logger.info("EXAMPLE 7: Performance Test")
    logger.info("=" * 60)

    deidentifier = Deidentifier()

    # Create 1000 sample resumes
    sample_resume = """
    Name: Candidate {i}
    Email: candidate{i}@example.com
    Phone: (555) 000-{i:04d}
    SSN: {ssn}
    Experience: 5 years in software engineering
    """

    resumes = [
        sample_resume.format(i=i, ssn=f"{100+i//10:03d}-{i%100:02d}-{1000+i:04d}")
        for i in range(1000)
    ]

    logger.info("Deidentifying %d resumes (large batch)...", len(resumes))

    start = time.time()
    deidentifier.deidentify_batch(resumes)
    elapsed = time.time() - start

    logger.info("✓ Completed in %.2f seconds", elapsed)
    logger.info("  Rate: %.0f resumes/second", len(resumes) / elapsed)

    # Verify some results
    stats = deidentifier.get_statistics()
    logger.info("Statistics:")
    for info_type, count in stats.items():
        logger.info("  - %s: %d", info_type, count)


if __name__ == "__main__":
    example_basic_usage()
    example_batch_processing()
    example_detection_details()
    example_custom_masks()
    example_verification()
    example_convenience_functions()
    example_performance()

    logger.info("=" * 60)
