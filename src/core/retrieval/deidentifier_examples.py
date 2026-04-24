"""
VedaAide Data Deidentification Tool - Usage Guide

This module provides comprehensive PII (Personally Identifiable Information) masking
for the VedaAide recruitment interview system.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.retrieval.deidentifier import Deidentifier, deidentify_text, verify_text


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Deidentification")
    print("=" * 60)
    
    deidentifier = Deidentifier()
    
    text = """
    John Doe has been with the company for 5 years.
    His contact information:
    - Email: john.doe@example.com
    - Phone: (555) 123-4567
    - SSN: 123-45-6789
    """
    
    print("Original text:")
    print(text)
    
    deidentified = deidentifier.deidentify(text)
    print("\nDeidentified text:")
    print(deidentified)
    
    # Verify deidentification
    is_safe = deidentifier.verify_deidentification(text, deidentified)
    print(f"\nVerification result: {'✓ SAFE' if is_safe else '✗ UNSAFE'}")


def example_batch_processing():
    """Batch processing example."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Processing")
    print("=" * 60)
    
    deidentifier = Deidentifier()
    
    # 5 candidate resumes
    resumes = [
        "Resume 1: Alice Smith, Email: alice@example.com, SSN: 111-22-3333",
        "Resume 2: Bob Johnson, Phone: (555) 222-2222, Email: bob@example.com",
        "Resume 3: Carol White, SSN: 333-44-5555, Phone: (555) 333-3333",
        "Resume 4: David Brown, Email: david@example.com, SSN: 444-55-6666",
        "Resume 5: Eve Davis, Phone: (555) 555-5555, Email: eve@example.com",
    ]
    
    print(f"Processing {len(resumes)} resumes...")
    
    deidentified_resumes = deidentifier.deidentify_batch(resumes)
    
    print("\nDeidentified resumes:")
    for i, (original, deidentified) in enumerate(zip(resumes, deidentified_resumes), 1):
        print(f"\n{i}. {deidentified[:60]}...")
    
    # Statistics
    stats = deidentifier.get_statistics()
    print(f"\nDetection statistics:")
    for info_type, count in stats.items():
        print(f"  - {info_type}: {count}")


def example_detection_details():
    """Example showing detection details."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Detection Details")
    print("=" * 60)
    
    deidentifier = Deidentifier()
    
    text = """
    Contact Information:
    - Card: 4532-1234-5678-9010
    - DOB: 01/15/1990
    - Work Phone: (555) 999-8888
    """
    
    print("Text to analyze:")
    print(text)
    
    matches = deidentifier.detect(text)
    
    print(f"\nFound {len(matches)} sensitive information(s):")
    for i, match in enumerate(matches, 1):
        print(f"  {i}. Type: {match.type.value}")
        print(f"     Text: {match.text}")
        print(f"     Position: {match.start}-{match.end}")
        print(f"     Mask: {match.mask}")


def example_custom_masks():
    """Example with custom mask templates."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Mask Templates")
    print("=" * 60)
    
    from src.core.retrieval.deidentifier import SensitiveInfoType
    
    custom_masks = {
        SensitiveInfoType.SSN: "[REDACTED_SSN]",
        SensitiveInfoType.EMAIL: "[REDACTED_EMAIL]",
        SensitiveInfoType.PHONE: "[REDACTED_PHONE]",
    }
    
    deidentifier = Deidentifier(mask_template=custom_masks)
    
    text = "Contact john@example.com or (555) 123-4567. SSN: 123-45-6789"
    result = deidentifier.deidentify(text)
    
    print("Original:")
    print(text)
    print("\nWith custom masks:")
    print(result)


def example_verification():
    """Example of verification."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Verification - Success and Failure")
    print("=" * 60)
    
    # Success case
    print("SUCCESS CASE:")
    original = "My email is alice@example.com and SSN is 123-45-6789"
    deidentified = "My email is [EMAIL] and SSN is [SSN]"
    
    result = verify_text(original, deidentified)
    print(f"Original: {original}")
    print(f"Deidentified: {deidentified}")
    print(f"Verification: {'✓ PASS' if result else '✗ FAIL'}")
    
    # Failure case
    print("\nFAILURE CASE (NOT PROPERLY MASKED):")
    original2 = "SSN: 123-45-6789"
    deidentified2 = "SSN: 123-45-6789"  # Oops, not masked!
    
    result2 = verify_text(original2, deidentified2)
    print(f"Original: {original2}")
    print(f"Deidentified: {deidentified2}")
    print(f"Verification: {'✓ PASS' if result2 else '✗ FAIL'}")


def example_convenience_functions():
    """Example using convenience functions."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Convenience Functions")
    print("=" * 60)
    
    text = "Contact John at john@example.com or (555) 123-4567"
    
    # Simple one-liner
    deidentified = deidentify_text(text)
    
    print(f"Original: {text}")
    print(f"Deidentified: {deidentified}")


def example_performance():
    """Example showing performance characteristics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Performance Test")
    print("=" * 60)
    
    import time
    
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
        sample_resume.format(
            i=i,
            ssn=f"{100+i//10:03d}-{i%100:02d}-{1000+i:04d}"
        )
        for i in range(1000)
    ]
    
    print(f"Deidentifying {len(resumes)} resumes (large batch)...")
    
    start = time.time()
    results = deidentifier.deidentify_batch(resumes)
    elapsed = time.time() - start
    
    print(f"✓ Completed in {elapsed:.2f} seconds")
    print(f"  Rate: {len(resumes)/elapsed:.0f} resumes/second")
    
    # Verify some results
    stats = deidentifier.get_statistics()
    print(f"\nStatistics:")
    for info_type, count in stats.items():
        print(f"  - {info_type}: {count}")


if __name__ == "__main__":
    example_basic_usage()
    example_batch_processing()
    example_detection_details()
    example_custom_masks()
    example_verification()
    example_convenience_functions()
    example_performance()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
