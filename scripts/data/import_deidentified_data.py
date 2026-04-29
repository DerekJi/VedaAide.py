#!/usr/bin/env python3
"""Import and deidentify data, then index into Qdrant.

Pipeline:
  1. Load public sample data (resumes, job postings)
  2. Apply PII deidentification via Deidentifier
  3. Build DocumentRecord objects with versioning metadata
  4. Index into Qdrant via DocumentIndexer (LlamaIndex)
  5. Write index manifest for traceability

Usage:
    poetry run python scripts/data/import_deidentified_data.py
    poetry run python scripts/data/import_deidentified_data.py --dry-run
    poetry run python scripts/data/import_deidentified_data.py --qdrant-url http://localhost:6333
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.data.load_public_samples import PublicSampleLoader  # noqa: E402
from src.core.data.document_record import (  # noqa: E402
    DEFAULT_COLLECTION_NAME,
    DocumentIndexer,
    DocumentRecord,
)
from src.core.data.deidentifier import Deidentifier  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MANIFEST_PATH = "data/working_datasets/index_manifest.json"
MIN_DOCUMENTS = 10


def build_resume_record(raw: Dict[str, Any], deidentifier: Deidentifier) -> DocumentRecord:
    """Convert a raw resume dict into a deidentified DocumentRecord."""
    content = raw.get("content", "")
    deidentified_content = deidentifier.deidentify(content)
    metadata = {k: v for k, v in raw.items() if k not in ("content",)}
    return DocumentRecord(
        doc_id=raw["id"],
        doc_type="resume",
        content=deidentified_content,
        metadata=metadata,
    )


def build_job_record(raw: Dict[str, Any], deidentifier: Deidentifier) -> DocumentRecord:
    """Convert a raw job posting dict into a deidentified DocumentRecord."""
    # Flatten structured fields into a single content string
    requirements = "\n".join(f"- {r}" for r in raw.get("requirements", []))
    benefits = "\n".join(f"- {b}" for b in raw.get("benefits", []))
    content = (
        f"Title: {raw.get('title', '')}\n"
        f"Company: {raw.get('company', '')}\n"
        f"Location: {raw.get('location', '')}\n\n"
        f"Description:\n{raw.get('description', '')}\n\n"
        f"Requirements:\n{requirements}\n\n"
        f"Benefits:\n{benefits}"
    )
    deidentified_content = deidentifier.deidentify(content)
    metadata = {
        k: v for k, v in raw.items() if k not in ("description", "requirements", "benefits")
    }
    return DocumentRecord(
        doc_id=raw["id"],
        doc_type="job_posting",
        content=deidentified_content,
        metadata=metadata,
    )


def load_and_deidentify(
    data_dir: str = "data/public_samples",
) -> List[DocumentRecord]:
    """Load all sample data and apply deidentification.

    Args:
        data_dir: Path to directory containing sample JSON files.

    Returns:
        List of deidentified DocumentRecord objects.
    """
    loader = PublicSampleLoader(data_dir=data_dir)
    deidentifier = Deidentifier()

    records: List[DocumentRecord] = []

    logger.info("Loading resumes...")
    resumes = loader.load_resumes()
    for raw in resumes:
        records.append(build_resume_record(raw, deidentifier))
    logger.info("Loaded %d resumes", len(resumes))

    logger.info("Loading job postings...")
    jobs = loader.load_job_postings()
    for raw in jobs:
        records.append(build_job_record(raw, deidentifier))
    logger.info("Loaded %d job postings", len(jobs))

    logger.info("Total documents after deidentification: %d", len(records))
    return records


def verify_deidentification(records: List[DocumentRecord]) -> bool:
    """Verify no raw PII patterns remain in any record's content.

    Args:
        records: List of DocumentRecord objects to verify.

    Returns:
        True if all records pass verification.
    """
    deidentifier = Deidentifier()
    all_clean = True
    for rec in records:
        matches = deidentifier.detect(rec.content)
        if matches:
            logger.warning(
                "PII detected in %s (%s): %s",
                rec.doc_id,
                rec.doc_type,
                [m.type.value for m in matches],
            )
            all_clean = False
    return all_clean


def print_summary(records: List[DocumentRecord]) -> None:
    """Print a human-readable summary of loaded records."""
    by_type: Dict[str, int] = {}
    for rec in records:
        by_type[rec.doc_type] = by_type.get(rec.doc_type, 0) + 1
    print("\n--- Document Summary ---")
    for doc_type, count in sorted(by_type.items()):
        print(f"  {doc_type}: {count}")
    print(f"  TOTAL: {len(records)}")
    print("------------------------\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import and index deidentified data into Qdrant")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and deidentify data but skip Qdrant indexing",
    )
    parser.add_argument(
        "--qdrant-url",
        default="http://localhost:6333",
        help="Qdrant server URL (default: http://localhost:6333)",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION_NAME,
        help=f"Qdrant collection name (default: {DEFAULT_COLLECTION_NAME})",
    )
    parser.add_argument(
        "--data-dir",
        default="data/public_samples",
        help="Directory containing sample JSON files",
    )
    parser.add_argument(
        "--manifest",
        default=MANIFEST_PATH,
        help=f"Output path for index manifest (default: {MANIFEST_PATH})",
    )
    args = parser.parse_args()

    # Step 1: Load and deidentify
    records = load_and_deidentify(data_dir=args.data_dir)
    print_summary(records)

    # Step 2: Verify deidentification
    logger.info("Verifying deidentification...")
    if not verify_deidentification(records):
        logger.warning("Some records may still contain PII - check logs above")
    else:
        logger.info("Deidentification verified: no PII detected")

    # Step 3: Check minimum document count
    if len(records) < MIN_DOCUMENTS:
        logger.error("Insufficient documents: need %d, got %d", MIN_DOCUMENTS, len(records))
        return 1

    if args.dry_run:
        logger.info("--dry-run: skipping Qdrant indexing")
        print(json.dumps([{"doc_id": r.doc_id, "doc_type": r.doc_type} for r in records], indent=2))
        return 0

    # Step 4: Index into Qdrant
    indexer = DocumentIndexer(
        qdrant_url=args.qdrant_url,
        collection_name=args.collection,
    )
    logger.info(
        "Indexing %d documents into Qdrant collection '%s'...", len(records), args.collection
    )
    stats = indexer.index_documents(records)

    print("\n--- Index Stats ---")
    print(f"  Collection  : {stats.collection}")
    print(f"  Indexed     : {stats.indexed}")
    print(f"  Errors      : {stats.errors}")
    print(f"  Total vectors: {stats.total_vectors}")
    print("-------------------\n")

    # Step 5: Save manifest
    indexer.save_manifest(stats, records, args.manifest)
    logger.info("Pipeline complete.")

    return 0 if stats.errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
