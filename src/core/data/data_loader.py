"""
统一的数据加载器 - 支持多个数据源的工厂模式实现

架构:
  DataSource (抽象基类)
    ├── StaticDataSource      (data/public_samples/)
    ├── GeneratedDataSource   (scripts/data/data_generator.py)
    ├── KaggleDataSource      (External - Kaggle API)
    └── HuggingFaceDataSource (External - Hugging Face Hub)
         ↓
  DataSourceFactory (工厂 - 负责实例化)
         ↓
  DataLoader (用户接口 - 统一API)
"""

import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional, Literal
from dataclasses import asdict

# 导入数据生成器
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts"))
from data.data_generator import (
    ResumeGenerator,
    JobPostingGenerator,
    ResumeRecord,
    JobPostingRecord,
)


# ============================================================================
# 数据源抽象基类
# ============================================================================

class DataSource(ABC):
    """数据源的抽象接口"""

    @abstractmethod
    def load_resumes(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """加载简历数据"""
        pass

    @abstractmethod
    def load_jobs(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """加载招聘岗位数据"""
        pass

    @abstractmethod
    def load_qa_pairs(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """加载Q&A对数据"""
        pass


# ============================================================================
# 具体数据源实现
# ============================================================================

class StaticDataSource(DataSource):
    """静态数据源 - 从 data/public_samples/ 加载"""

    def __init__(self, base_path: str = "data/public_samples"):
        self.base_path = Path(base_path)

    def _load_json_file(self, filename: str) -> List[Dict]:
        """通用JSON文件加载器"""
        file_path = self.base_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"静态数据文件未找到: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_resumes(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """从 sample_resumes.json 加载"""
        data = self._load_json_file("sample_resumes.json")
        return data[:count]

    def load_jobs(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """从 sample_job_postings.json 加载"""
        data = self._load_json_file("sample_job_postings.json")
        return data[:count]

    def load_qa_pairs(self, count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """从 sample_reading_comprehension.json 加载"""
        data = self._load_json_file("sample_reading_comprehension.json")
        return data[:count]


class GeneratedDataSource(DataSource):
    """生成式数据源 - 动态生成数据"""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

    def load_resumes(self, count: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """动态生成简历数据"""
        generator = ResumeGenerator(seed=self.seed)
        resumes = [generator.generate() for _ in range(count)]
        return [self._record_to_dict(r) for r in resumes]

    def load_jobs(self, count: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """动态生成招聘岗位数据"""
        generator = JobPostingGenerator(seed=self.seed)
        jobs = [generator.generate() for _ in range(count)]
        return [self._record_to_dict(j) for j in jobs]

    def load_qa_pairs(self, count: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """生成Q&A对（暂未实现）"""
        raise NotImplementedError("Q&A生成器尚未实现")

    @staticmethod
    def _record_to_dict(record) -> Dict[str, Any]:
        """将dataclass记录转换为字典"""
        return asdict(record)


class KaggleDataSource(DataSource):
    """Kaggle数据源 - 从Kaggle API下载"""

    def __init__(self, dataset_id: str = ""):
        self.dataset_id = dataset_id

    def load_resumes(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        """从Kaggle下载简历数据"""
        raise NotImplementedError(
            "Kaggle数据源实现中...\n"
            "使用: pip install kaggle\n"
            "设置: ~/.kaggle/kaggle.json (API密钥)"
        )

    def load_jobs(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        """从Kaggle下载招聘岗位数据"""
        raise NotImplementedError(
            "Kaggle数据源实现中...\n"
            "推荐数据集: 'Job Postings from LinkedIn, Indeed, Glassdoor'\n"
            "参考: https://www.kaggle.com/..."
        )

    def load_qa_pairs(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        raise NotImplementedError("Q&A Kaggle源尚未实现")


class HuggingFaceDataSource(DataSource):
    """Hugging Face Hub数据源"""

    def __init__(self, repo_id: str = ""):
        self.repo_id = repo_id

    def load_resumes(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        """从Hugging Face Hub下载简历数据"""
        raise NotImplementedError(
            "Hugging Face数据源实现中...\n"
            "使用: from huggingface_hub import hf_hub_download\n"
            "参考: https://huggingface.co/datasets"
        )

    def load_jobs(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        """从Hugging Face Hub下载招聘岗位数据"""
        raise NotImplementedError(
            "Hugging Face数据源实现中...\n"
            "使用: from huggingface_hub import hf_hub_download"
        )

    def load_qa_pairs(self, count: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        raise NotImplementedError("Q&A HF源尚未实现")


# ============================================================================
# 工厂类 - 管理数据源的创建
# ============================================================================

class DataSourceFactory:
    """数据源工厂 - 负责创建对应的数据源实例"""

    _sources: Dict[str, type] = {
        "static": StaticDataSource,
        "generated": GeneratedDataSource,
        "kaggle": KaggleDataSource,
        "huggingface": HuggingFaceDataSource,
        "hf": HuggingFaceDataSource,  # 别名
    }

    @classmethod
    def create(
        cls,
        source_type: Literal["static", "generated", "kaggle", "huggingface", "hf"],
        **kwargs
    ) -> DataSource:
        """
        创建数据源实例

        Args:
            source_type: 数据源类型
            **kwargs: 传递给数据源的参数

        Returns:
            DataSource 实例

        Raises:
            ValueError: 未知的数据源类型

        Examples:
            >>> source = DataSourceFactory.create("static")
            >>> source = DataSourceFactory.create("generated", seed=42)
            >>> source = DataSourceFactory.create("kaggle", dataset_id="...")
        """
        source_type = source_type.lower()

        if source_type not in cls._sources:
            raise ValueError(
                f"未知的数据源类型: {source_type}\n"
                f"支持的类型: {', '.join(cls._sources.keys())}"
            )

        source_class = cls._sources[source_type]
        return source_class(**kwargs)

    @classmethod
    def register(cls, name: str, source_class: type) -> None:
        """注册新的数据源类"""
        cls._sources[name.lower()] = source_class

    @classmethod
    def list_sources(cls) -> List[str]:
        """列出所有支持的数据源"""
        return list(cls._sources.keys())


# ============================================================================
# 用户接口 - DataLoader
# ============================================================================

class DataLoader:
    """
    统一的数据加载器接口

    使用工厂模式提供灵活的数据源管理。
    支持多个数据源：静态、生成、Kaggle、Hugging Face等。
    """

    def __init__(self, source: str = "static", **kwargs):
        """
        初始化DataLoader

        Args:
            source: 数据源类型 ("static", "generated", "kaggle", "huggingface")
            **kwargs: 传递给数据源的参数

        Examples:
            >>> # 使用静态数据
            >>> loader = DataLoader(source="static")
            >>> resumes = loader.get_resumes()

            >>> # 使用生成数据
            >>> loader = DataLoader(source="generated", seed=42)
            >>> jobs = loader.get_jobs(count=1000)

            >>> # 使用Kaggle数据
            >>> loader = DataLoader(source="kaggle", dataset_id="...")
            >>> resumes = loader.get_resumes(count=10000)
        """
        self.source_type = source
        self.source = DataSourceFactory.create(source, **kwargs)

    def get_resumes(self, count: int = 5) -> List[Dict[str, Any]]:
        """获取简历数据"""
        return self.source.load_resumes(count=count)

    def get_jobs(self, count: int = 5) -> List[Dict[str, Any]]:
        """获取招聘岗位数据"""
        return self.source.load_jobs(count=count)

    def get_qa_pairs(self, count: int = 5) -> List[Dict[str, Any]]:
        """获取Q&A对数据"""
        return self.source.load_qa_pairs(count=count)

    @staticmethod
    def available_sources() -> List[str]:
        """列出所有可用的数据源"""
        return DataSourceFactory.list_sources()

    @staticmethod
    def info(source_type: str = None) -> str:
        """显示数据源信息"""
        if source_type:
            sources = [source_type.lower()]
        else:
            sources = DataLoader.available_sources()

        info_text = "📊 Available Data Sources:\n"
        info_text += "=" * 50 + "\n"

        source_docs = {
            "static": {
                "desc": "Static sample data from Git repository",
                "path": "data/public_samples/",
                "size": "~7 KB",
                "count": "15 samples",
                "latency": "Instant",
                "use_case": "Quick demos, documentation, CI/CD",
            },
            "generated": {
                "desc": "Dynamically generated synthetic data",
                "path": "scripts/data/data_generator.py",
                "size": "On-demand (configurable)",
                "count": "1-100K+ records",
                "latency": "Seconds-Minutes",
                "use_case": "Development, testing, benchmarks",
            },
            "kaggle": {
                "desc": "Real-world data from Kaggle",
                "path": "External (requires API key)",
                "size": "50-200 MB",
                "count": "100K-500K records",
                "latency": "Minutes (first-time download)",
                "use_case": "Evaluation, production validation",
            },
            "huggingface": {
                "desc": "Datasets from Hugging Face Hub",
                "path": "External (hf_hub_download)",
                "size": "Variable",
                "count": "Variable",
                "latency": "Minutes (first-time download)",
                "use_case": "ML evaluation, research",
            },
        }

        for source in sources:
            if source in source_docs:
                doc = source_docs[source]
                info_text += f"\n{source.upper()}\n"
                info_text += "-" * 50 + "\n"
                for key, val in doc.items():
                    info_text += f"  {key:15}: {val}\n"

        return info_text


# ============================================================================
# 便利函数
# ============================================================================

def get_sample_data(
    data_type: Literal["resumes", "jobs", "qa"],
    source: str = "static",
    count: int = 5,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    快速获取样本数据的便利函数

    Args:
        data_type: 数据类型 ("resumes", "jobs", "qa")
        source: 数据源
        count: 获取数量
        **kwargs: 传递给DataLoader的参数

    Returns:
        数据列表

    Examples:
        >>> resumes = get_sample_data("resumes", source="static", count=10)
        >>> jobs = get_sample_data("jobs", source="generated", count=1000, seed=42)
    """
    loader = DataLoader(source=source, **kwargs)

    if data_type == "resumes":
        return loader.get_resumes(count=count)
    elif data_type == "jobs":
        return loader.get_jobs(count=count)
    elif data_type == "qa":
        return loader.get_qa_pairs(count=count)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


# ============================================================================
# 命令行接口
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="数据加载器 - 统一接口")
    parser.add_argument("--source", default="static", help="数据源类型")
    parser.add_argument(
        "--type", choices=["resumes", "jobs", "qa"], default="jobs"
    )
    parser.add_argument("--count", type=int, default=5, help="获取数量")
    parser.add_argument("--seed", type=int, default=None, help="生成数据的随机种子")
    parser.add_argument("--info", action="store_true", help="显示数据源信息")
    parser.add_argument("--list", action="store_true", help="列出所有数据源")

    args = parser.parse_args()

    if args.info:
        print(DataLoader.info(args.source))
    elif args.list:
        print("Available sources:", ", ".join(DataLoader.available_sources()))
    else:
        try:
            data = get_sample_data(
                args.type, source=args.source, count=args.count, seed=args.seed
            )
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            sys.exit(1)
