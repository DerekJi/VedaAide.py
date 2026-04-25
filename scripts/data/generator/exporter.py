"""Data export utilities for various formats."""

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import List, Union

from .models import JobPostingRecord, ResumeRecord

logger = logging.getLogger(__name__)


class DataExporter:
    """Exports records to various file formats (JSON, JSONL).

    This exporter handles serialization of ResumeRecord and JobPostingRecord
    objects to standardized file formats suitable for bulk processing.
    """

    @staticmethod
    def to_jsonl(records: List[Union[ResumeRecord, JobPostingRecord]], output_file: str) -> None:
        """Export records to JSONL format (newline-delimited JSON).

        JSONL format is memory-efficient for large datasets as each line
        is a complete JSON object.

        Args:
            records: List of records to export.
            output_file: Path to output file.

        Raises:
            IOError: If file cannot be written.
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                for record in records:
                    if isinstance(record, (ResumeRecord, JobPostingRecord)):
                        json_str = json.dumps(asdict(record), ensure_ascii=False)
                    else:
                        json_str = json.dumps(record, ensure_ascii=False)
                    f.write(json_str + "\n")

            logger.info(f"Exported {len(records)} records to {output_file}")
        except IOError as e:
            logger.error(f"Failed to export to {output_file}: {e}")
            raise

    @staticmethod
    def to_json(records: List[Union[ResumeRecord, JobPostingRecord]], output_file: str) -> None:
        """Export records to JSON format (JSON array).

        Note: This loads entire file into memory. For large datasets,
        use to_jsonl() instead.

        Args:
            records: List of records to export.
            output_file: Path to output file.

        Raises:
            IOError: If file cannot be written.
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = []
        for record in records:
            if isinstance(record, (ResumeRecord, JobPostingRecord)):
                data.append(asdict(record))
            else:
                data.append(record)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"Exported {len(records)} records to {output_file}")
        except IOError as e:
            logger.error(f"Failed to export to {output_file}: {e}")
            raise
