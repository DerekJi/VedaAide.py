#!/usr/bin/env python3
"""
Data generation system - backward compatibility wrapper.

This module re-exports all generators and models for backward compatibility.
New code should import directly from scripts.data.generator submodules.

Deprecated: Use 'from scripts.data.generator import <Class>' instead.
"""

import argparse
import logging
from pathlib import Path

# Import all components from new modular structure
from scripts.data.generator import (
    DataExporter,
    DataRepository,
    JobPostingGenerator,
    JobPostingRecord,
    ResumeGenerator,
    ResumeRecord,
)

logger = logging.getLogger(__name__)

# Re-export for backward compatibility
__all__ = [
    "DataRepository",
    "ResumeRecord",
    "JobPostingRecord",
    "ResumeGenerator",
    "JobPostingGenerator",
    "DataExporter",
]


def main() -> None:
    """Generate synthetic resume and job posting data (CLI entry point).

    This function provides command-line interface for data generation.
    Uses the new modular generator components.
    """
    parser = argparse.ArgumentParser(
        description="Generate large-scale synthetic data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--resumes", type=int, default=100, help="Number of resumes to generate (default: 100)"
    )
    parser.add_argument(
        "--jobs", type=int, default=100, help="Number of job postings to generate (default: 100)"
    )
    parser.add_argument(
        "--output-dir", default="data/generated", help="Output directory (default: data/generated)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "jsonl"],
        default="jsonl",
        help="Output format (default: jsonl)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting data generation...")
    logger.info(f"  Resumes: {args.resumes:,}")
    logger.info(f"  Jobs: {args.jobs:,}")
    logger.info(f"  Format: {args.format}")

    # Generate resumes
    logger.info("Generating resume data...")
    resume_gen = ResumeGenerator(seed=args.seed)
    resumes = [resume_gen.generate() for _ in range(args.resumes)]

    resume_file = output_dir / f"resumes.{args.format}"
    if args.format == "jsonl":
        DataExporter.to_jsonl(resumes, str(resume_file))
    else:
        DataExporter.to_json(resumes, str(resume_file))

    # Generate jobs
    logger.info("Generating job posting data...")
    job_gen = JobPostingGenerator(seed=args.seed)
    jobs = [job_gen.generate() for _ in range(args.jobs)]

    job_file = output_dir / f"jobs.{args.format}"
    if args.format == "jsonl":
        DataExporter.to_jsonl(jobs, str(job_file))
    else:
        DataExporter.to_json(jobs, str(job_file))

    logger.info(f"✓ Complete! Data saved to {output_dir}/")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        exit(1)
