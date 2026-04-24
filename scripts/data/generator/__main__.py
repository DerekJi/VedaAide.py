"""Command-line interface for data generation.

This module provides CLI functionality to generate synthetic resume and job
posting data in bulk, with support for different output formats and seeds.

Usage:
    python -m scripts.data.generator --resumes 1000 --jobs 500 --output-dir data/generated
    python -m scripts.data.generator --help
"""

import argparse
import logging
from pathlib import Path
from typing import Optional

from .exporter import DataExporter
from .job_posting import JobPostingGenerator
from .resume import ResumeGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main(
    num_resumes: int = 100,
    num_jobs: int = 100,
    output_dir: str = "data/generated",
    output_format: str = "jsonl",
    seed: Optional[int] = None,
) -> None:
    """Generate synthetic resume and job posting data.

    Args:
        num_resumes: Number of resume records to generate.
        num_jobs: Number of job posting records to generate.
        output_dir: Directory to save output files.
        output_format: Output format (json or jsonl).
        seed: Random seed for reproducibility.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("Starting data generation...")
    logger.info(f"  Resumes: {num_resumes:,}")
    logger.info(f"  Jobs: {num_jobs:,}")
    logger.info(f"  Format: {output_format}")

    # Generate resumes
    logger.info("Generating resume data...")
    resume_gen = ResumeGenerator(seed=seed)
    resumes = [resume_gen.generate() for _ in range(num_resumes)]

    resume_file = output_path / f"resumes.{output_format}"
    if output_format == "jsonl":
        DataExporter.to_jsonl(resumes, str(resume_file))
    else:
        DataExporter.to_json(resumes, str(resume_file))

    # Generate jobs
    logger.info("Generating job posting data...")
    job_gen = JobPostingGenerator(seed=seed)
    jobs = [job_gen.generate() for _ in range(num_jobs)]

    job_file = output_path / f"jobs.{output_format}"
    if output_format == "jsonl":
        DataExporter.to_jsonl(jobs, str(job_file))
    else:
        DataExporter.to_json(jobs, str(job_file))

    logger.info(f"✓ Complete! Data saved to {output_path}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic resume and job posting data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m scripts.data.generator --resumes 1000 --jobs 500\n"
            "  python -m scripts.data.generator --seed 42 --format json\n"
        ),
    )
    parser.add_argument(
        "--resumes",
        type=int,
        default=100,
        help="Number of resume records to generate (default: 100)",
    )
    parser.add_argument(
        "--jobs", type=int, default=100, help="Number of job records to generate (default: 100)"
    )
    parser.add_argument(
        "--output-dir",
        default="data/generated",
        help="Output directory for generated files (default: data/generated)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "jsonl"],
        default="jsonl",
        help="Output format: json or jsonl (default: jsonl)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility (default: None)"
    )

    args = parser.parse_args()

    try:
        main(
            num_resumes=args.resumes,
            num_jobs=args.jobs,
            output_dir=args.output_dir,
            output_format=args.format,
            seed=args.seed,
        )
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        exit(1)
