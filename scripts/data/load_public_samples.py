#!/usr/bin/env python3
"""
Load and validate public sample datasets for VedaAide.

This script demonstrates how to load and work with the public sample datasets
for RAG system evaluation and testing.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List


class PublicSampleLoader:
    """Load and validate public sample datasets."""

    def __init__(self, data_dir: str = "data/public_samples"):
        """
        Initialize the loader.

        Args:
            data_dir: Directory containing public sample datasets
        """
        self.data_dir = Path(data_dir)

    def load_resumes(self) -> List[Dict[str, Any]]:
        """Load sample resumes."""
        file_path = self.data_dir / "sample_resumes.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Resumes file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_job_postings(self) -> List[Dict[str, Any]]:
        """Load sample job postings."""
        file_path = self.data_dir / "sample_job_postings.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Job postings file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_reading_comprehension(self) -> List[Dict[str, Any]]:
        """Load sample reading comprehension questions."""
        file_path = self.data_dir / "sample_reading_comprehension.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Reading comprehension file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load all datasets."""
        return {
            "resumes": self.load_resumes(),
            "job_postings": self.load_job_postings(),
            "reading_comprehension": self.load_reading_comprehension(),
        }

    def validate_resumes(self, resumes: List[Dict[str, Any]]) -> bool:
        """Validate resume data structure."""
        required_fields = {"id", "name", "content"}
        for resume in resumes:
            if not required_fields.issubset(resume.keys()):
                print(f"Invalid resume: missing required fields. Got: {resume.keys()}")
                return False
            if not isinstance(resume["id"], str) or not resume["id"]:
                print(f"Invalid resume id: {resume['id']}")
                return False
            if not isinstance(resume["content"], str) or len(resume["content"]) < 10:
                print(f"Invalid resume content length for {resume['id']}")
                return False
        return True

    def validate_job_postings(self, jobs: List[Dict[str, Any]]) -> bool:
        """Validate job posting data structure."""
        required_fields = {"id", "title", "company", "description", "requirements", "benefits"}
        for job in jobs:
            if not required_fields.issubset(job.keys()):
                print(f"Invalid job posting: missing required fields. Got: {job.keys()}")
                return False
            if not isinstance(job["requirements"], list) or len(job["requirements"]) == 0:
                print(f"Invalid requirements for job {job['id']}")
                return False
        return True

    def validate_reading_comprehension(self, questions: List[Dict[str, Any]]) -> bool:
        """Validate reading comprehension data structure."""
        required_fields = {"id", "passage", "question", "options", "correct_answer", "explanation"}
        for item in questions:
            if not required_fields.issubset(item.keys()):
                print(f"Invalid question: missing required fields. Got: {item.keys()}")
                return False
            if not isinstance(item["options"], list) or len(item["options"]) != 4:
                print(f"Invalid options for question {item['id']}")
                return False
            if item["correct_answer"] not in ["A", "B", "C", "D"]:
                print(f"Invalid correct_answer for question {item['id']}")
                return False
        return True

    def validate_all(self) -> bool:
        """Validate all datasets."""
        try:
            datasets = self.load_all()

            print("Validating resumes...")
            if not self.validate_resumes(datasets["resumes"]):
                return False
            print(f"✓ Resumes valid ({len(datasets['resumes'])} items)")

            print("Validating job postings...")
            if not self.validate_job_postings(datasets["job_postings"]):
                return False
            print(f"✓ Job postings valid ({len(datasets['job_postings'])} items)")

            print("Validating reading comprehension...")
            if not self.validate_reading_comprehension(datasets["reading_comprehension"]):
                return False
            print(f"✓ Reading comprehension valid ({len(datasets['reading_comprehension'])} items)")

            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def print_summary(self):
        """Print dataset summary."""
        try:
            datasets = self.load_all()

            print("\n" + "=" * 60)
            print("PUBLIC SAMPLE DATASETS SUMMARY")
            print("=" * 60)

            print(f"\nResumes: {len(datasets['resumes'])} items")
            for resume in datasets["resumes"]:
                content_preview = resume["content"][:50].replace("\n", " ") + "..."
                print(f"  - {resume['id']}: {resume['name']} ({len(resume['content'])} chars)")

            print(f"\nJob Postings: {len(datasets['job_postings'])} items")
            for job in datasets["job_postings"]:
                print(f"  - {job['id']}: {job['title']} at {job['company']} ({job['level']})")

            print(f"\nReading Comprehension: {len(datasets['reading_comprehension'])} items")
            for item in datasets["reading_comprehension"]:
                print(f"  - {item['id']}: {item['question'][:50]}...")

            print("\n" + "=" * 60)
        except Exception as e:
            print(f"Error printing summary: {e}")


def main():
    """Main entry point."""
    loader = PublicSampleLoader()

    print("Loading public sample datasets...")
    if loader.validate_all():
        print("\n✓ All datasets valid and ready to use!")
        loader.print_summary()
        return 0
    else:
        print("\n✗ Dataset validation failed!")
        return 1


if __name__ == "__main__":
    exit(main())
