"""
数据加载模块 - 统一的数据源管理

支持多个数据源：
  - Static: 静态示例数据 (Tier 1)
  - Generated: 动态生成的合成数据 (Tier 2)
  - Kaggle: Kaggle公开数据集 (Tier 3)
  - HuggingFace: Hugging Face Hub (Tier 3)

使用示例：
  >>> from src.core.data import DataLoader, get_sample_data
  >>>
  >>> # 方式1：创建loader实例
  >>> loader = DataLoader(source="generated", seed=42)
  >>> jobs = loader.get_jobs(count=1000)
  >>>
  >>> # 方式2：快速函数
  >>> resumes = get_sample_data("resumes", source="static", count=10)
"""

from .data_loader import (
    DataLoader,
    DataSource,
    DataSourceFactory,
    GeneratedDataSource,
    HuggingFaceDataSource,
    KaggleDataSource,
    StaticDataSource,
)
from .indexer import DocumentIndexer, DocumentRecord, IndexStats

__all__ = [
    "DataLoader",
    "DataSource",
    "DataSourceFactory",
    "StaticDataSource",
    "GeneratedDataSource",
    "KaggleDataSource",
    "HuggingFaceDataSource",
    "DocumentIndexer",
    "DocumentRecord",
    "IndexStats",
]
