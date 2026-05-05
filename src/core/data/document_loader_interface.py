from abc import ABC, abstractmethod
from pathlib import Path

from llama_index.core import Document


class IDocumentLoader(ABC):
    """
    Abstract interface for document loading.

    Defines the contract that all document loader implementations must follow.
    Similar to .NET interfaces, this allows for multiple implementations and
    easy testing through dependency injection.

    Example of custom implementation:
        class CachedDocumentLoader(IDocumentLoader):
            def __init__(self, ttl_seconds: int = 3600):
                self.ttl_seconds = ttl_seconds
                self.cache = {}

            def load_documents(self, directory: Path, recursive: bool = True) -> list[Document]:
                # Implementation with caching
                pass
    """

    @abstractmethod
    def load_documents(self, directory: Path, recursive: bool = True) -> list[Document]:
        """Load documents from a directory."""
        pass

    @abstractmethod
    def load_json_documents(self, file_path: Path) -> list[Document]:
        """Load documents from a JSON file."""
        pass

    @abstractmethod
    def load_markdown_documents(self, file_path: Path) -> list[Document]:
        """Load documents from a Markdown file."""
        pass

    @abstractmethod
    def load_text_documents(self, file_path: Path) -> list[Document]:
        """Load documents from a text file."""
        pass

    @abstractmethod
    def load_pdf_documents(self, file_path: Path) -> list[Document]:
        """Load documents from a PDF file."""
        pass
