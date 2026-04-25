#!/usr/bin/env python3
"""Demo script for quick testing of the data generation system.

This script demonstrates:
- Generating 1000 sample resumes
- Generating 500 sample job postings
- Displaying generated data format and statistics
"""

import logging
from pathlib import Path

from scripts.data.generator import DataExporter, JobPostingGenerator, ResumeGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def print_section(title: str) -> None:
    """Print a formatted section title.

    Args:
        title: Section title text.
    """
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def demo_basic_generation() -> Path:
    """Demonstrate basic data generation.

    Generates 100 resumes and 50 job postings, displaying samples
    and statistics.

    Returns:
        Path to output directory.
    """
    print_section("Demo 1: Basic Data Generation")

    logger.info("Generating 100 resumes...")
    resume_gen = ResumeGenerator(seed=42)
    resumes = [resume_gen.generate() for _ in range(100)]

    if resumes:
        sample = resumes[0]
        print("\n✓ Sample resume:")
        print(f"  ID: {sample.id}")
        print(f"  Name: {sample.name}")
        print(f"  Level: {sample.level}")
        print(f"  Experience: {sample.years_experience} years")
        print(f"  Tech: {', '.join(sample.tech_stack[:3])}...")
        print(f"  Soft skills: {', '.join(sample.soft_skills)}")

    logger.info("Generating 50 job postings...")
    job_gen = JobPostingGenerator(seed=42)
    jobs = [job_gen.generate() for _ in range(50)]

    if jobs:
        sample = jobs[0]
        print("\n✓ Sample job posting:")
        print(f"  ID: {sample.id}")
        print(f"  Title: {sample.title}")
        print(f"  Company: {sample.company}")
        print(f"  Level: {sample.level}")
        print(f"  Salary: ${sample.salary_min:,} - ${sample.salary_max:,}")
        print(f"  Tech: {', '.join(sample.tech_stack[:3])}...")

    # Export
    output_dir = Path("data/generated_demo")
    output_dir.mkdir(parents=True, exist_ok=True)

    DataExporter.to_jsonl(resumes, str(output_dir / "resumes_basic.jsonl"))
    DataExporter.to_jsonl(jobs, str(output_dir / "jobs_basic.jsonl"))

    logger.info(f"Exported to {output_dir}/")
    return output_dir


def print_statistics(output_dir: Path) -> None:
    """Print file statistics from output directory.

    Args:
        output_dir: Directory containing generated files.
    """
    print_section("Generation Statistics")

    total_size = 0
    total_files = 0

    for file_path in output_dir.glob("*.jsonl"):
        try:
            size = file_path.stat().st_size
            lines = sum(1 for _ in open(file_path))
            total_size += size
            total_files += 1

            print(f"✓ {file_path.name}")
            print(f"  Lines: {lines:,}")
            print(f"  Size: {size/1024/1024:.2f} MB")
        except (IOError, OSError) as e:
            logger.error(f"Failed to read {file_path}: {e}")

    print("\nTotal:")
    print(f"  Files: {total_files}")
    print(f"  Size: {total_size/1024/1024:.2f} MB")


def main() -> None:
    """Main demo entry point."""
    print("\n" + "=" * 70)
    print("  VedaAide Data Generation System Demo")
    print("=" * 70)

    try:
        output_dir = demo_basic_generation()
        print_statistics(output_dir)

        print("\n" + "=" * 70)
        print("  ✅ Demo Complete!")
        print("=" * 70)

        logger.info("To generate larger datasets:")
        logger.info("  python -m scripts.data.generator --resumes 100000 --jobs 50000")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
