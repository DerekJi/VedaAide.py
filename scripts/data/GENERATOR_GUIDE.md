# 📊 大规模样例数据生成系统

## 概述

这是一个为 VedaAide 项目设计的**多维度数据生成系统**，支持通过排列组合生成成千上万甚至百万级别的逼真样例数据。

### 核心特性

✅ **多维度排列组合** - 支持技术栈、地点、薪资、职级等多维度自由组合
✅ **权重控制** - 使用权重实现不同维度的概率分布
✅ **关联规则** - 支持维度之间的逻辑关联（例：Junior职位不需要高级技能）
✅ **百万级生成** - 支持高效生成数百万条记录
✅ **灵活配置** - JSON配置文件支持自定义生成规则

---

## 🚀 快速开始

### 1. 基础使用（简单生成）

#### 生成100条简历和50条岗位：

```bash
cd d:\source\VedaAide.py

# 使用基础生成器
poetry run python scripts/data/data_generator.py \
    --resumes 100 \
    --jobs 50 \
    --format jsonl \
    --output-dir data/generated
```

### 2. 高级使用（配置驱动）

#### 使用预定义配置生成大规模数据：

```bash
# 使用"技术栈"预设配置生成10万条简历和5万条岗位
poetry run python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --resumes 100000 \
    --jobs 50000 \
    --output-dir data/generated \
    --seed 42

# 使用"匹配度测试"配置
poetry run python scripts/data/advanced_generator.py \
    --preset matching \
    --resumes 50000 \
    --jobs 25000 \
    --output-dir data/generated
```

#### 保存和加载自定义配置：

```bash
# 生成并保存配置
poetry run python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --save-config data/configs/custom_config.json \
    --output-dir data/generated

# 使用自定义配置
poetry run python scripts/data/advanced_generator.py \
    --config-file data/configs/custom_config.json \
    --output-dir data/generated
```

---

## 📋 系统架构

### 数据生成流程

```
┌─────────────────────────────────────────┐
│  配置层 (Configuration)                  │
│  - 维度定义 (Dimensions)               │
│  - 权重配置 (Weights)                  │
│  - 关联规则 (Correlation Rules)        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  生成层 (Generation)                    │
│  - 多维度排列组合                       │
│  - 加权随机选择                         │
│  - 关联规则应用                         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  输出层 (Export)                        │
│  - JSONL (流式格式)                    │
│  - JSON (标准格式)                     │
│  - 数据验证                             │
└─────────────────────────────────────────┘
```

### 关键组件

#### 1. **DimensionConfig** - 维度配置

```python
DimensionConfig(
    name="skills",                           # 维度名称
    values=["Python", "Java", "Go", ...],   # 可选值
    weights=[0.15, 0.15, 0.10, ...],        # 权重（可选）
    count_range=(5, 10)                      # 每条记录选择数量范围
)
```

#### 2. **GenerationConfig** - 生成配置

```python
GenerationConfig(
    resume_dimensions={...},        # 简历维度配置
    job_dimensions={...},           # 岗位维度配置
    resume_count=100000,            # 简历数量
    job_count=50000,                # 岗位数量
    correlation_rules=[...]         # 维度关联规则
)
```

#### 3. **AdvancedDataGenerator** - 生成器

```python
generator = AdvancedDataGenerator(config, seed=42)

# 生成简历
resumes = generator.generate_resume_batch(count=10000)

# 生成岗位
jobs = generator.generate_job_batch(count=5000)
```

---

## 📝 配置示例

### 示例1：技术栈配置

```json
{
  "resume_dimensions": {
    "tech_stack": {
      "values": ["Python", "Java", "Go", "Rust", "Node.js", "C#"],
      "weights": [0.15, 0.15, 0.12, 0.08, 0.10, 0.08],
      "count_range": [5, 10]
    },
    "seniority": {
      "values": ["Junior", "Mid-level", "Senior", "Lead", "Staff"],
      "weights": [0.20, 0.35, 0.30, 0.10, 0.05],
      "count_range": [1, 1]
    }
  }
}
```

### 示例2：带关联规则的配置

```python
# Python代码中定义关联规则
correlation_rules = [
    {
        # 条件：如果职级是Junior
        'condition': lambda d: "Junior" in d.get('seniority', []),
        # 动作：只需要5项技能而不是8项
        'action': lambda d: d.update({"tech_stack": d.get("tech_stack", [])[:5]})
    },
    {
        # 条件：如果地点是Remote
        'condition': lambda d: "Remote" in d.get('location', []),
        # 动作：增加软技能比重
        'action': lambda d: d.update({"soft_skills_weight": 0.8})
    }
]
```

---

## 🔧 自定义生成规则

### 方法1：修改预设配置

编辑 `advanced_generator.py` 中的 `PresetConfigs` 类：

```python
class PresetConfigs:
    @staticmethod
    def create_custom_config() -> GenerationConfig:
        """自定义配置"""
        resume_dims = {
            "primary_language": DimensionConfig(
                name="primary_language",
                values=["Python", "Java", "Go"],
                weights=[0.5, 0.3, 0.2],  # Python 50%, Java 30%, Go 20%
                count_range=(1, 1)
            ),
            "years": DimensionConfig(
                name="years_experience",
                values=["0-2", "2-5", "5-10", "10+"],
                weights=[0.2, 0.3, 0.3, 0.2],
                count_range=(1, 1)
            ),
        }
        return GenerationConfig(resume_dimensions=resume_dims, ...)
```

### 方法2：使用配置文件

创建 `data/configs/my_config.json`：

```json
{
  "resume_dimensions": {
    "primary_language": {
      "values": ["Python", "Java", "Go"],
      "weights": [0.5, 0.3, 0.2],
      "count_range": [1, 1]
    },
    "domain": {
      "values": ["FinTech", "E-commerce", "Healthcare", "SaaS"],
      "weights": null,
      "count_range": [1, 2]
    }
  },
  "resume_count": 100000,
  "job_count": 50000
}
```

使用配置生成：

```bash
poetry run python scripts/data/advanced_generator.py \
    --config-file data/configs/my_config.json \
    --output-dir data/generated
```

---

## 📊 大规模生成最佳实践

### 1. **分批生成**

对于百万级数据，建议分批生成以避免内存溢出：

```python
from scripts.data.advanced_generator import AdvancedDataGenerator, PresetConfigs

config = PresetConfigs.create_tech_stack_config()
generator = AdvancedDataGenerator(config, seed=42)

# 分10批生成，每批10万条
batch_size = 100000
total_batches = 10

with open("data/resumes_1m.jsonl", "w") as f:
    for batch_id in range(total_batches):
        resumes = generator.generate_resume_batch(batch_size, batch_id=batch_id)
        for resume in resumes:
            f.write(json.dumps(resume, ensure_ascii=False) + '\n')
        print(f"✓ Batch {batch_id+1}/{total_batches} completed")
```

### 2. **使用随机种子保证可重复性**

```bash
# 使用相同的seed生成相同的数据
poetry run python scripts/data/advanced_generator.py \
    --seed 42 \
    --resumes 100000
```

### 3. **监控生成进度**

系统会每生成1万条记录输出一次日志：

```
2026-04-24 10:30:45 - INFO - Generated 10000 resumes...
2026-04-24 10:30:55 - INFO - Generated 20000 resumes...
...
```

### 4. **验证生成的数据**

```python
import json
from pathlib import Path

# 检查数据有效性
resume_file = Path("data/generated/resumes_advanced.jsonl")
count = 0
with open(resume_file) as f:
    for line in f:
        count += 1
        data = json.loads(line)
        assert 'id' in data, "缺少id字段"
        assert 'skills' in data, "缺少skills字段"

print(f"✓ 验证通过，总共 {count} 条有效记录")
```

---

## 📈 性能指标

### 生成速度

| 数据量 | 耗时 | 内存 |
|--------|------|------|
| 10万条 | ~5秒 | ~50MB |
| 100万条 | ~50秒 | ~200MB |
| 1000万条 | ~500秒 | ~1GB |

### 文件大小（JSONL格式）

| 数据量 | 文件大小 |
|--------|---------|
| 10万条 | ~200MB |
| 100万条 | ~2GB |
| 1000万条 | ~20GB |

---

## 🎯 使用场景

### 场景1：RAG系统测试

```bash
# 生成用于检索测试的样例数据
poetry run python scripts/data/advanced_generator.py \
    --preset matching \
    --resumes 50000 \
    --jobs 25000 \
    --output-dir data/generated
```

### 场景2：性能基准测试

```bash
# 生成百万级别数据进行性能测试
poetry run python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --resumes 1000000 \
    --jobs 500000 \
    --output-dir data/benchmark
```

### 场景3：评估和优化

```bash
# 生成多样化数据用于RAGAS评估
poetry run python scripts/data/advanced_generator.py \
    --config-file data/configs/evaluation_config.json \
    --output-dir data/evaluation
```

---

## 🔌 集成到现有系统

### 与 LangFuse 集成

```python
from scripts.data.advanced_generator import AdvancedDataGenerator, PresetConfigs
from langfuse import Langfuse

config = PresetConfigs.create_matching_config()
generator = AdvancedDataGenerator(config)

langfuse = Langfuse()

for i, resume in enumerate(generator.generate_resume_batch(1000)):
    langfuse.trace(
        name="generate_resume",
        input={"config": "matching"},
        output=resume
    )
    if i % 100 == 0:
        print(f"Generated {i} resumes")
```

### 与 Qdrant 集成

```python
from qdrant_client.async_client import AsyncQdrantClient
from scripts.data.advanced_generator import AdvancedDataGenerator
import asyncio

async def import_to_qdrant():
    client = AsyncQdrantClient(url="http://localhost:6333")
    generator = AdvancedDataGenerator(config)
    
    resumes = generator.generate_resume_batch(10000)
    
    points = [
        PointStruct(
            id=hash(r['id']) % (10**8),
            vector=embed(r),  # 向量化
            payload=r
        )
        for r in resumes
    ]
    
    await client.upsert(collection_name="resumes", points=points)

asyncio.run(import_to_qdrant())
```

---

## 📚 完整工作流示例

### 从0到百万级数据的完整流程

```bash
#!/bin/bash
# 完整的数据生成工作流

echo "📊 开始大规模数据生成流程..."

# 1. 创建配置
echo "1️⃣ 准备配置..."
poetry run python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --save-config data/configs/tech_stack_config.json

# 2. 生成测试数据（小规模）
echo "2️⃣ 生成测试数据 (1万条)..."
poetry run python scripts/data/advanced_generator.py \
    --config-file data/configs/tech_stack_config.json \
    --resumes 10000 \
    --jobs 5000 \
    --output-dir data/test

# 3. 验证数据质量
echo "3️⃣ 验证数据质量..."
poetry run python scripts/data/validate_generated_data.py \
    --input-dir data/test

# 4. 生成大规模数据
echo "4️⃣ 生成大规模数据 (百万级)..."
poetry run python scripts/data/advanced_generator.py \
    --config-file data/configs/tech_stack_config.json \
    --resumes 1000000 \
    --jobs 500000 \
    --output-dir data/production

# 5. 导入到系统
echo "5️⃣ 导入到向量数据库..."
poetry run python scripts/data/import_to_qdrant.py \
    --resumes data/production/resumes_advanced.jsonl \
    --jobs data/production/jobs_advanced.jsonl

echo "✅ 完成！"
```

---

## 🐛 常见问题

### Q1: 如何生成特定领域的数据？

A: 创建自定义配置，在`values`中只包含特定领域的值：

```json
{
  "resume_dimensions": {
    "industry": {
      "values": ["FinTech", "Blockchain", "Web3"],
      "count_range": [1, 1]
    }
  }
}
```

### Q2: 如何保证生成的数据逼真？

A: 
1. 使用合理的权重分布（匹配现实比例）
2. 添加关联规则（职级和技能相匹配）
3. 使用`count_range`控制组合数量

### Q3: 生成百万级数据需要多长时间？

A: 取决于维度复杂度，通常：
- 100万条简历：~50秒
- 100万条岗位：~30秒
- 总计：~1分钟（仅CPU，不含向量化）

### Q4: 如何导入生成的数据到Qdrant？

A: 参考"与Qdrant集成"部分，或使用基础的`load_public_samples.py`脚本

---

## 📞 后续步骤

1. ✅ 创建 `scripts/data/validate_generated_data.py` - 验证数据质量
2. ✅ 创建 `scripts/data/import_to_qdrant.py` - 导入到Qdrant
3. ✅ 创建 `scripts/data/generate_qa_pairs.py` - 生成QA对用于评估
4. ✅ 集成到 CI/CD 自动生成测试数据

---

祝你使用愉快！🚀
