"""Unified data loader - Factory pattern implementation for multiple sources.

Architecture:
  DataSource (abstract base class)
    ├── StaticDataSource      (data/public_samples/)
    ├── GeneratedDataSource   (scripts.data.generator)
    ├── KaggleDataSource      (External - Kaggle API)
    └── HuggingFaceDataSource (External - Hugging Face Hub)
         ↓
  DataSourceFactory (factory - handles instantiation)
         ↓
  DataLoader (user interface - unified API)
"""

import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

try:
    from scripts.data.generator import JobPostingGenerator, ResumeGenerator
except ImportError:
    # Fallback if generators not available
    ResumeGenerator = None  # type: ignore
    JobPostingGenerator = None  # type: ignore


class DataSource(ABC):
    """Abstract interface for all data sources."""

    @abstractmethod
    def load_resumes(self, count: int = 5, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load resume records from the data source.

        Args:
            count: Number of records to load.
            **kwargs: Additional source-specific parameters.

        Returns:
            List of resume dictionaries.
        """

    @abstractmethod
    def load_jobs(self, count: int = 5, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load job posting records from the data source.

        Args:
            count: Number of records to load.
            **kwargs: Additional source-specific parameters.

        Returns:
            List of job posting dictionaries.
        """

    @abstractmethod
    def load_qa_pairs(self, count: int = 5, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load Q&A pair records from the data source.

        Args:
            count: Number of records to load.
            **kwargs: Additional source-specific parameters.

        Returns:
            List of Q&A pair dictionaries.
        """


class StaticDataSource(DataSource):
    """Load data from static JSON files (data/public_samples/)."""

    def __init__(self, base_path: str = "data/public_samples") -> None:
        """Initialize the static data source.

        Args:
            base_path: Path to directory with sample data files.
        """
        self.base_path = Path(base_path)

    def _load_json_file(self, filename: str) -> Any:
        """Load and parse a JSON file.

        Args:
            filename: Name of the JSON file.

        Returns:
            Parsed JSON data.

        Raises:
            FileNotFoundError: If file doesn't exist.
        """
        file_path = self.base_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_resumes(self, count: int = 5, **kwargs: Any) -> Any:
        """Load resumes from sample_resumes.json."""
        data = self._load_json_file("sample_resumes.json")
        return data[:count]

    def load_jobs(self, count: int = 5, **kwargs: Any) -> Any:
        """Load job postings from sample_job_postings.json."""
        data = self._load_json_file("sample_job_postings.json")
        return data[:count]

    def load_qa_pairs(self, count: int = 5, **kwargs: Any) -> Any:
        """Load Q&A pairs from sample_reading_comprehension.json."""
        data = self._load_json_file("sample_reading_comprehension.json")
        return data[:count]


class GeneratedDataSource(DataSource):
    """Generate synthetic data dynamically."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the generated data source.

        Args:
            seed: Random seed for reproducibility.
        """
        if ResumeGenerator is None:
            raise ImportError(
                "ResumeGenerator not available. Ensure scripts.data.generator is in Python path."
            )
        self.seed = seed

    def load_resumes(self, count: int = 100, **kwargs: Any) -> List[Dict[str, Any]]:
        """Generate synthetic resume records."""
        generator = ResumeGenerator(seed=self.seed)
        resumes = [generator.generate() for _ in range(count)]
        return [asdict(r) for r in resumes]

    def load_jobs(self, count: int = 100, **kwargs: Any) -> List[Dict[str, Any]]:
        """Generate synthetic job posting records."""
        generator = JobPostingGenerator(seed=self.seed)
        jobs = [generator.generate() for _ in range(count)]
        return [asdict(j) for j in jobs]

    def load_qa_pairs(self, count: int = 100, **kwargs: Any) -> List[Dict[str, Any]]:
        """Generate synthetic Q&A pairs."""
        raise NotImplementedError("Q&A generation not yet implemented")


class KaggleDataSource(DataSource):
    """Load data from Kaggle datasets via API."""

    def __init__(self, dataset_id: str = "") -> None:
        """Initialize Kaggle data source.

        Args:
            dataset_id: Kaggle dataset identifier.
        """
        self.dataset_id = dataset_id

    def load_resumes(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load resume data from Kaggle."""
        raise NotImplementedError("Kaggle integration not yet implemented")

    def load_jobs(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load job postings from Kaggle."""
        raise NotImplementedError("Kaggle integration not yet implemented")

    def load_qa_pairs(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load Q&A pairs from Kaggle."""
        raise NotImplementedError("Kaggle integration not yet implemented")


class HuggingFaceDataSource(DataSource):
    """Load data from Hugging Face Hub datasets."""

    def __init__(self, repo_id: str = "") -> None:
        """Initialize Hugging Face data source.

        Args:
            repo_id: Hugging Face repository identifier.
        """
        self.repo_id = repo_id

    def load_resumes(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load resume data from Hugging Face Hub."""
        raise NotImplementedError("HF integration not yet implemented")

    def load_jobs(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load job postings from Hugging Face Hub."""
        raise NotImplementedError("HF integration not yet implemented")

    def load_qa_pairs(self, count: int = 1000, **kwargs: Any) -> List[Dict[str, Any]]:
        """Load Q&A pairs from Hugging Face Hub."""
        raise NotImplementedError("HF integration not yet implemented")


class DataSourceFactory:
    """Factory for creating data source instances."""

    _sources: Dict[str, Type[DataSource]] = {
        "static": StaticDataSource,
        "generated": GeneratedDataSource,
        "kaggle": KaggleDataSource,
        "huggingface": HuggingFaceDataSource,
    }

    @classmethod
    def create(cls, source_type: str, **kwargs: Any) -> DataSource:
        """Create a data source instance.

        Args:
            source_type: Type of source (static, generated, kaggle, huggingface).
            **kwargs: Arguments passed to the source's __init__.

        Returns:
            Instantiated DataSource subclass.

        Raises:
            ValueError: If source_type is unknown.
        """
        source_type_lower = source_type.lower()
        if source_type_lower not in cls._sources:
            available = ", ".join(cls._sources.keys())
            raise ValueError(f"Unknown source type: {source_type_lower}. Available: {available}")

        source_class = cls._sources[source_type_lower]
        return source_class(**kwargs)

    @classmethod
    def list_sources(cls: Type["DataSourceFactory"]) -> List[str]:
        """List all available data source types."""
        return list(cls._sources.keys())


class DataLoader:
    """Unified data loader interface using factory pattern.

    Supports multiple data sources: static files, generated data,
    Kaggle datasets, and Hugging Face Hub.
    """

    def __init__(self, source: str = "static", **kwargs: Any) -> None:
        """Initialize DataLoader with specified source.

        Args:
            source: Data source type (static, generated, kaggle, huggingface).
                Default: 'static'.
            **kwargs: Arguments passed to the source's __init__.
        """
        self._source = DataSourceFactory.create(source, **kwargs)

    def get_resumes(self, count: int = 5) -> List[Dict[str, Any]]:
        """Load resume records.

        Args:
            count: Number of records to load.

        Returns:
            List of resume dictionaries.
        """
        return self._source.load_resumes(count=count)

    def get_jobs(self, count: int = 5) -> List[Dict[str, Any]]:
        """Load job posting records.

        Args:
            count: Number of records to load.

        Returns:
            List of job posting dictionaries.
        """
        return self._source.load_jobs(count=count)

    def get_qa_pairs(self, count: int = 5) -> List[Dict[str, Any]]:
        """Load Q&A pair records.

        Args:
            count: Number of records to load.

        Returns:
            List of Q&A pair dictionaries.
        """
        return self._source.load_qa_pairs(count=count)

    @staticmethod
    def available_sources() -> List[str]:
        """List all available data sources."""
        return DataSourceFactory.list_sources()
