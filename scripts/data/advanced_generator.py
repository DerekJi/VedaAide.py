#!/usr/bin/env python3
"""
高级数据生成配置和排列组合系统。

支持：
- 多维度排列组合生成
- 权重和概率控制
- 数百万级别大规模生成
- 进度跟踪和增量生成
"""

import json
import logging
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================================
# 配置数据结构
# ============================================================================


@dataclass
class DimensionConfig:
    """维度配置"""

    name: str  # 维度名称
    values: List[str]  # 可选值
    weights: Optional[List[float]] = None  # 权重（可选）
    count_range: tuple = (1, 3)  # 每条记录选择的数量范围


@dataclass
class GenerationConfig:
    """生成配置"""

    resume_dimensions: Dict[str, DimensionConfig]
    job_dimensions: Dict[str, DimensionConfig]
    resume_count: int = 100000
    job_count: int = 50000
    correlation_rules: List[Dict[str, Any]] = None  # 维度之间的关联规则


# ============================================================================
# 高级生成器
# ============================================================================


class AdvancedDataGenerator:
    """支持排列组合和权重的高级数据生成器"""

    def __init__(self, config: GenerationConfig, seed: int = None):
        self.config = config
        self.random = random.Random(seed)
        self.resume_id = 0
        self.job_id = 0

    def _select_with_weights(
        self, values: List[str], weights: Optional[List[float]] = None, count: int = 1
    ) -> List[str]:
        """按权重选择值"""
        if weights is None:
            return self.random.sample(values, min(count, len(values)))

        # 使用加权随机选择
        selected = self.random.choices(values, weights=weights, k=count)
        return list(set(selected))  # 去重

    def _apply_correlation_rules(self, data: Dict[str, Any], rules: List[Dict]) -> Dict[str, Any]:
        """应用维度之间的关联规则"""
        if not rules:
            return data

        for rule in rules:
            condition = rule.get("condition")
            action = rule.get("action")

            # 检查条件是否满足
            if callable(condition) and condition(data):
                if callable(action):
                    action(data)

        return data

    def generate_resume_batch(self, count: int, batch_id: int = 0) -> List[Dict[str, Any]]:
        """生成一批简历"""
        resumes = []

        for i in range(count):
            self.resume_id += 1
            resume = {}

            # 按维度生成数据
            for dim_name, dim_config in self.config.resume_dimensions.items():
                num_select = self.random.randint(*dim_config.count_range)
                selected = self._select_with_weights(
                    dim_config.values, dim_config.weights, num_select
                )
                resume[dim_name] = selected

            # 应用关联规则
            if self.config.correlation_rules:
                resume = self._apply_correlation_rules(resume, self.config.correlation_rules)

            # 添加元数据
            resume["id"] = f"resume_{batch_id:02d}_{self.resume_id:08d}"
            resume["generated_at"] = str(Path(__file__).stat().st_mtime)

            resumes.append(resume)

            if (self.resume_id % 10000) == 0:
                logger.info(f"Generated {self.resume_id} resumes...")

        return resumes

    def generate_job_batch(self, count: int, batch_id: int = 0) -> List[Dict[str, Any]]:
        """生成一批岗位"""
        jobs = []

        for i in range(count):
            self.job_id += 1
            job = {}

            # 按维度生成数据
            for dim_name, dim_config in self.config.job_dimensions.items():
                num_select = self.random.randint(*dim_config.count_range)
                selected = self._select_with_weights(
                    dim_config.values, dim_config.weights, num_select
                )
                job[dim_name] = selected

            # 应用关联规则
            if self.config.correlation_rules:
                job = self._apply_correlation_rules(job, self.config.correlation_rules)

            # 添加元数据
            job["id"] = f"job_{batch_id:02d}_{self.job_id:08d}"
            job["generated_at"] = str(Path(__file__).stat().st_mtime)

            jobs.append(job)

            if (self.job_id % 10000) == 0:
                logger.info(f"Generated {self.job_id} jobs...")

        return jobs


# ============================================================================
# 预定义配置
# ============================================================================


class PresetConfigs:
    """预定义的生成配置"""

    @staticmethod
    def create_tech_stack_config(preset: str = "balanced") -> GenerationConfig:
        """创建技术栈配置"""

        # 不同难度的技术栈
        preset_configs = {
            "balanced": {
                "tech_stack": DimensionConfig(
                    name="tech_stack",
                    values=[
                        "Python",
                        "Java",
                        "Go",
                        "Rust",
                        "Node.js",
                        "C#",
                        "PHP",
                        "Ruby",
                        "React",
                        "Vue.js",
                        "Angular",
                        "PostgreSQL",
                        "MongoDB",
                        "Redis",
                        "Docker",
                        "Kubernetes",
                        "Terraform",
                        "AWS",
                        "Azure",
                        "GCP",
                    ],
                    weights=[
                        0.15,
                        0.15,
                        0.12,
                        0.08,
                        0.10,
                        0.08,
                        0.06,
                        0.04,
                        0.06,
                        0.05,
                        0.03,
                        0.12,
                        0.08,
                        0.06,
                        0.10,
                        0.08,
                        0.05,
                        0.12,
                        0.08,
                        0.05,
                    ],
                    count_range=(5, 10),
                ),
                "seniority": DimensionConfig(
                    name="seniority",
                    values=["Junior", "Mid-level", "Senior", "Lead", "Staff"],
                    weights=[0.20, 0.35, 0.30, 0.10, 0.05],
                    count_range=(1, 1),
                ),
                "location": DimensionConfig(
                    name="location",
                    values=[
                        "Remote",
                        "San Francisco",
                        "New York",
                        "Seattle",
                        "Beijing",
                        "Shanghai",
                        "London",
                    ],
                    count_range=(1, 1),
                ),
            }
        }

        config = preset_configs.get(preset, preset_configs["balanced"])

        return GenerationConfig(
            resume_dimensions=config,
            job_dimensions=config,
            resume_count=100000,
            job_count=50000,
        )

    @staticmethod
    def create_matching_config() -> GenerationConfig:
        """创建用于测试匹配度的配置"""

        # 简历维度
        resume_dims = {
            "skills": DimensionConfig(
                name="skills",
                values=[
                    "Python",
                    "Java",
                    "Go",
                    "Kubernetes",
                    "PostgreSQL",
                    "MongoDB",
                    "AWS",
                    "Azure",
                    "Docker",
                    "React",
                    "TensorFlow",
                ],
                weights=[0.15, 0.15, 0.10, 0.12, 0.10, 0.08, 0.10, 0.08, 0.08, 0.06, 0.02],
                count_range=(5, 8),
            ),
            "experience_years": DimensionConfig(
                name="experience_years",
                values=["0-2", "2-5", "5-8", "8-10", "10+"],
                weights=[0.15, 0.30, 0.35, 0.15, 0.05],
                count_range=(1, 1),
            ),
            "previous_roles": DimensionConfig(
                name="previous_roles",
                values=[
                    "Backend Engineer",
                    "DevOps",
                    "Data Engineer",
                    "ML Engineer",
                    "Frontend",
                    "Full Stack",
                    "Engineering Manager",
                ],
                count_range=(2, 4),
            ),
        }

        # 岗位维度
        job_dims = {
            "required_skills": DimensionConfig(
                name="required_skills",
                values=[
                    "Python",
                    "Java",
                    "Go",
                    "Kubernetes",
                    "PostgreSQL",
                    "MongoDB",
                    "AWS",
                    "Azure",
                    "Docker",
                    "React",
                    "TensorFlow",
                ],
                weights=[0.15, 0.15, 0.10, 0.12, 0.10, 0.08, 0.10, 0.08, 0.08, 0.06, 0.02],
                count_range=(5, 8),
            ),
            "min_seniority": DimensionConfig(
                name="min_seniority",
                values=["Junior", "Mid-level", "Senior"],
                weights=[0.20, 0.50, 0.30],
                count_range=(1, 1),
            ),
            "job_level": DimensionConfig(
                name="job_level",
                values=["Individual Contributor", "Team Lead", "Manager", "Director"],
                weights=[0.60, 0.25, 0.10, 0.05],
                count_range=(1, 1),
            ),
        }

        # 关联规则：Junior职位不需要太多经验
        correlation_rules = [
            {
                "condition": lambda d: "Junior" in d.get("min_seniority", []),
                "action": lambda d: d.update({"required_skills": d.get("required_skills", [])[:5]}),
            }
        ]

        return GenerationConfig(
            resume_dimensions=resume_dims,
            job_dimensions=job_dims,
            resume_count=50000,
            job_count=25000,
            correlation_rules=correlation_rules,
        )


# ============================================================================
# 配置文件管理
# ============================================================================


class ConfigManager:
    """配置文件管理"""

    @staticmethod
    def save_config(config: GenerationConfig, output_file: str):
        """保存配置为JSON"""
        config_dict = {
            "resume_dimensions": {},
            "job_dimensions": {},
            "resume_count": config.resume_count,
            "job_count": config.job_count,
        }

        for name, dim in config.resume_dimensions.items():
            config_dict["resume_dimensions"][name] = {
                "values": dim.values,
                "weights": dim.weights,
                "count_range": dim.count_range,
            }

        for name, dim in config.job_dimensions.items():
            config_dict["job_dimensions"][name] = {
                "values": dim.values,
                "weights": dim.weights,
                "count_range": dim.count_range,
            }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=2)

        logger.info(f"Configuration saved to {output_file}")

    @staticmethod
    def load_config(config_file: str) -> GenerationConfig:
        """从JSON加载配置"""
        with open(config_file, "r", encoding="utf-8") as f:
            config_dict = json.load(f)

        # 重建配置对象
        resume_dims = {}
        for name, dim_data in config_dict.get("resume_dimensions", {}).items():
            resume_dims[name] = DimensionConfig(
                name=name,
                values=dim_data.get("values", []),
                weights=dim_data.get("weights"),
                count_range=tuple(dim_data.get("count_range", (1, 3))),
            )

        job_dims = {}
        for name, dim_data in config_dict.get("job_dimensions", {}).items():
            job_dims[name] = DimensionConfig(
                name=name,
                values=dim_data.get("values", []),
                weights=dim_data.get("weights"),
                count_range=tuple(dim_data.get("count_range", (1, 3))),
            )

        return GenerationConfig(
            resume_dimensions=resume_dims,
            job_dimensions=job_dims,
            resume_count=config_dict.get("resume_count", 100000),
            job_count=config_dict.get("job_count", 50000),
        )


# ============================================================================
# 命令行工具
# ============================================================================


def cli_main():
    """命令行生成工具"""
    import argparse

    parser = argparse.ArgumentParser(description="高级样例数据生成器")
    parser.add_argument(
        "--preset", choices=["tech_stack", "matching"], default="tech_stack", help="使用预定义配置"
    )
    parser.add_argument("--resumes", type=int, default=None, help="简历数量")
    parser.add_argument("--jobs", type=int, default=None, help="岗位数量")
    parser.add_argument("--config-file", help="配置文件路径")
    parser.add_argument("--save-config", help="保存配置到文件")
    parser.add_argument("--output-dir", default="data/generated", help="输出目录")
    parser.add_argument("--seed", type=int, help="随机种子")

    args = parser.parse_args()

    # 加载或创建配置
    if args.config_file:
        config = ConfigManager.load_config(args.config_file)
    elif args.preset == "matching":
        config = PresetConfigs.create_matching_config()
    else:
        config = PresetConfigs.create_tech_stack_config()

    # 覆盖数量
    if args.resumes:
        config.resume_count = args.resumes
    if args.jobs:
        config.job_count = args.jobs

    # 保存配置
    if args.save_config:
        ConfigManager.save_config(config, args.save_config)

    # 生成数据
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Generating {config.resume_count} resumes and {config.job_count} jobs...")

    generator = AdvancedDataGenerator(config, seed=args.seed)

    # 生成简历
    resumes = generator.generate_resume_batch(config.resume_count)
    resume_file = output_dir / "resumes_advanced.jsonl"
    with open(resume_file, "w", encoding="utf-8") as f:
        for resume in resumes:
            f.write(json.dumps(resume, ensure_ascii=False) + "\n")
    logger.info(f"Saved {len(resumes)} resumes to {resume_file}")

    # 生成岗位
    jobs = generator.generate_job_batch(config.job_count)
    job_file = output_dir / "jobs_advanced.jsonl"
    with open(job_file, "w", encoding="utf-8") as f:
        for job in jobs:
            f.write(json.dumps(job, ensure_ascii=False) + "\n")
    logger.info(f"Saved {len(jobs)} jobs to {job_file}")


if __name__ == "__main__":
    cli_main()
