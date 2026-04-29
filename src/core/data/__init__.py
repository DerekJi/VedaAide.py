"""
数据加载模块 - 统一的数据源管理

支持多个数据源：
  - Static: 静态示例数据 (Tier 1)
  - Generated: 动态生成的合成数据 (Tier 2)
  - Kaggle: Kaggle公开数据集 (Tier 3)
  - HuggingFace: Hugging Face Hub (Tier 3)

支持的数据处理功能：
  - DocumentLoader: 从多种格式加载文档 (JSON, MD, TXT, PDF)
  - Deidentifier: PII 去识别和检测工具
  - DocumentRecord: 文档规范化和版本管理

使用示例：
  >>> from src.core.data import StructuredDataLoader, DocumentLoader, Deidentifier
  >>>
  >>> # 方式1：创建loader实例
  >>> loader = StructuredDataLoader(source="generated", seed=42)
  >>> jobs = loader.get_jobs(count=1000)
  >>>
  >>> # 文档加载
  >>> doc_loader = DocumentLoader()
  >>> docs = doc_loader.load_documents("data/samples/")
  >>>
  >>> # 去识别
  >>> deidentifier = Deidentifier()
  >>> text = deidentifier.deidentify("Contact: john@example.com, SSN: 123-45-6789")
"""

from src.core.data.deidentifier import (
    Deidentifier,
    SensitiveInfoType,
    deidentify_text,
    verify_text,
)
from src.core.data.document_loader import DocumentLoader
from src.core.data.document_loader_interface import IDocumentLoader
from src.core.data.document_record import DocumentIndexer, DocumentRecord, IndexStats
from src.core.data.structured_data_loader import (
    DataLoader,
    DataSource,
    DataSourceFactory,
    GeneratedDataSource,
    HuggingFaceDataSource,
    KaggleDataSource,
    StaticDataSource,
)

__all__ = [
    # Document loading
    "DocumentLoader",
    "IDocumentLoader",
    "document_record",
    "DocumentRecord",
    "IndexStats",
    # Data deidentification
    "Deidentifier",
    "SensitiveInfoType",
    "deidentify_text",
    "verify_text",
    # Structured data loading
    "DataLoader",
    "DataSource",
    "DataSourceFactory",
    "StaticDataSource",
    "GeneratedDataSource",
    "KaggleDataSource",
    "HuggingFaceDataSource",
]
