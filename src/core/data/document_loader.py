"""
Supports multiple document formats:
- JSON (structured documents with id, name, content)
- Markdown (*.md files)
- Plain text (*.txt files)
- PDF (*.pdf files - text-based only, requires PyPDF)

Note on PDF Support:
    PDF files with extractable text are supported. However, scanned PDFs or PDFs
    containing embedded images without text layers may not be processed correctly.
    Images within PDFs may be silently ignored. For OCR support of scanned PDFs,
    consider implementing Azure Computer Vision OCR separately.

Usage:
    loader = DocumentLoader()
    loader.load_documents("data/public_samples/", recursive=True)
    print(f"Indexed {loader.document_count} documents")
"""

import json
import logging
from pathlib import Path

from llama_index.core import Document

from .document_loader_interface import IDocumentLoader

# PDF support via PyPDF
try:
    from PyPDF2 import PdfReader

    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

logger = logging.getLogger(__name__)


class DocumentLoader(IDocumentLoader):
    def __init__(self):
        self.document_count = 0

    def load_json_documents(self, file_path: Path) -> list[Document]:
        """
        Load documents from JSON file.

        Expected format: List of objects with 'id', 'name', and 'content' fields.

        Args:
            file_path: Path to JSON file

        Returns:
            List of Document objects
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            documents = []

            # Handle list of objects
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    if isinstance(item, dict):
                        doc_id = item.get("id", f"{file_path.stem}_{idx}")
                        content = item.get("content", "")
                        name = item.get("name", f"Document {idx + 1}")

                        if content:
                            doc = Document(
                                doc_id=doc_id,
                                text=content,
                                metadata={
                                    "source": str(file_path),
                                    "doc_name": name,
                                    "format": "json",
                                    "chunk_index": 0,
                                },
                            )
                            documents.append(doc)

            logger.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file {file_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return []

    def load_markdown_documents(self, file_path: Path) -> list[Document]:
        """
        Load document from Markdown file.

        Args:
            file_path: Path to Markdown file

        Returns:
            List with single Document object
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            doc = Document(
                doc_id=file_path.stem,
                text=content,
                metadata={
                    "source": str(file_path),
                    "format": "markdown",
                    "chunk_index": 0,
                },
            )

            logger.info(f"Loaded markdown document from {file_path}")
            return [doc]

        except Exception as e:
            logger.error(f"Error loading markdown file {file_path}: {e}")
            return []

    def load_text_documents(self, file_path: Path) -> list[Document]:
        """
        Load document from plain text file.

        Args:
            file_path: Path to text file

        Returns:
            List with single Document object
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            doc = Document(
                doc_id=file_path.stem,
                text=content,
                metadata={
                    "source": str(file_path),
                    "format": "text",
                    "chunk_index": 0,
                },
            )

            logger.info(f"Loaded text document from {file_path}")
            return [doc]

        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {e}")
            return []

    def load_pdf_documents(self, file_path: Path) -> list[Document]:
        """
        Load document from PDF file (text-based).

        Extracts text from PDF files using PyPDF2. Only works with PDFs that have
        extractable text. Scanned PDFs, image-based PDFs, or PDFs with embedded
        images without text layers may not work correctly - images will be silently
        ignored and may result in missing or incomplete content.

        For scanned PDF support with OCR capability, consider implementing
        Azure Computer Vision API separately.

        Args:
            file_path: Path to PDF file

        Returns:
            List with single Document object (or empty list if extraction fails)
        """
        if not PYPDF_AVAILABLE:
            logger.warning(
                f"PyPDF2 not installed. Cannot load PDF file {file_path}. "
                "Install with: pip install PyPDF2 or poetry add PyPDF2"
            )
            return []

        try:
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                text_content = ""

                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            # Add page marker for reference
                            text_content += f"\n[Page {page_num + 1}]\n{page_text}"
                        else:
                            logger.warning(
                                f"Could not extract text from page {page_num + 1} in {file_path}. "
                                "This page may be a scanned image or have a different encoding."
                            )
                    except Exception as e:
                        logger.warning(
                            f"Error extracting text from page {page_num + 1} in {file_path}: {e}"
                        )
                        continue

            if not text_content.strip():
                logger.warning(
                    f"No text content could be extracted from {file_path}. "
                    "This PDF may be scanned or image-based. OCR support not available."
                )
                return []

            doc = Document(
                doc_id=file_path.stem,
                text=text_content,
                metadata={
                    "source": str(file_path),
                    "format": "pdf",
                    "pages": len(pdf_reader.pages),
                    "chunk_index": 0,
                },
            )

            logger.info(f"Loaded PDF document from {file_path} ({len(pdf_reader.pages)} pages)")
            return [doc]

        except Exception as e:
            logger.error(f"Error loading PDF file {file_path}: {e}")
            return []

    def load_documents(
        self,
        directory: Path,
        recursive: bool = True,
    ) -> list[Document]:
        """
        Load documents from directory supporting multiple formats.

        Supported formats: JSON, Markdown, TXT, PDF (text-based)

        Args:
            directory: Directory containing documents
            recursive: Whether to scan subdirectories

        Returns:
            List of loaded Document objects
        """
        directory = Path(directory)
        if not directory.exists():
            logger.error(f"Directory not found: {directory}")
            return []

        documents = []

        # Determine file patterns to search
        patterns = ["*.json", "*.md", "*.txt", "*.pdf"]
        if recursive:
            patterns = [f"**/{p}" for p in patterns]

        # Load documents by format
        for pattern in patterns:
            for file_path in directory.glob(pattern):
                if file_path.suffix == ".json":
                    documents.extend(self.load_json_documents(file_path))
                elif file_path.suffix == ".md":
                    documents.extend(self.load_markdown_documents(file_path))
                elif file_path.suffix == ".txt":
                    documents.extend(self.load_text_documents(file_path))
                elif file_path.suffix == ".pdf":
                    documents.extend(self.load_pdf_documents(file_path))

        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
