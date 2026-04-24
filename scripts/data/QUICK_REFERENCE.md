# 🚀 数据生成系统 - 快速参考

## 核心概念

你的需求是**通过基础数据的排列组合，自动生成大规模样例数据**。

本系统提供了完整的解决方案：

```
基础数据库(技术栈、职级、地点等)
           ↓
         排列组合规则
           ↓
        加权分布
           ↓
     生成百万级数据
```

---

## 三种使用方式

### 🎯 方式1：快速演示（立即体验）

```bash
cd /d/source/VedaAide.py

# 运行演示脚本
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/demo_generation.py
```

**输出**：
- 100条基础简历 + 50条岗位
- 10000条排列组合简历 + 5000条岗位
- 配置管理演示
- 统计数据分析

---

### 🔧 方式2：基础生成（简单快速）

```bash
# 生成1000条简历，500条岗位
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/data_generator.py \
    --resumes 1000 \
    --jobs 500 \
    --format jsonl \
    --output-dir data/my_data
```

**特点**：
- 随机生成逼真数据
- 支持简单参数配置
- 适合快速测试

---

### 💪 方式3：高级生成（大规模可控）

#### 使用预设配置：

```bash
# 方式3a：使用预设配置（推荐）
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --resumes 100000 \
    --jobs 50000 \
    --output-dir data/large_scale \
    --seed 42
```

#### 使用自定义配置：

```bash
# 方式3b：先保存配置
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --save-config data/my_config.json

# 修改data/my_config.json...

# 然后用配置生成
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --config-file data/my_config.json \
    --resumes 1000000 \
    --jobs 500000
```

---

## 📊 可用的预设配置

### 1. `tech_stack`（技术栈配置）- 默认

适合于通用的招聘场景，包含：
- **技术栈维度**：20个常见技术栈
- **职级维度**：Junior ~ Staff
- **地点维度**：14个全球主要城市
- **特点**：权重分布模拟现实分布

生成示例：
```json
{
  "tech_stack": ["Python", "Docker", "PostgreSQL", "Go", "Angular", "Java"],
  "seniority": ["Mid-level"],
  "location": ["Beijing"]
}
```

### 2. `matching`（匹配度测试配置）

适合于测试简历-岗位匹配算法，包含：
- **技术技能维度**：11个关键技术
- **经验年限维度**：5个等级
- **职位等级维度**：4个等级
- **特点**：支持计算匹配率

生成示例：
```json
{
  "skills": ["Python", "Kubernetes", "AWS"],
  "experience_years": ["5-8"],
  "job_level": ["Individual Contributor"]
}
```

---

## 🎨 自定义配置（JSON格式）

创建 `data/configs/my_config.json`：

```json
{
  "resume_dimensions": {
    "primary_language": {
      "values": ["Python", "Java", "Go", "Rust"],
      "weights": [0.5, 0.3, 0.15, 0.05],
      "count_range": [1, 1]
    },
    "years_experience": {
      "values": ["0-2", "2-5", "5-10", "10+"],
      "weights": [0.2, 0.3, 0.35, 0.15],
      "count_range": [1, 1]
    },
    "industry": {
      "values": ["FinTech", "E-commerce", "Healthcare", "SaaS"],
      "count_range": [1, 2]
    }
  },
  "job_dimensions": {
    "required_languages": {
      "values": ["Python", "Java", "Go", "Rust"],
      "weights": [0.5, 0.3, 0.15, 0.05],
      "count_range": [2, 4]
    }
  },
  "resume_count": 100000,
  "job_count": 50000
}
```

然后使用：
```bash
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --config-file data/configs/my_config.json
```

---

## 📈 生成规模参考

| 数据量 | 耗时 | 内存 | 文件大小 |
|--------|------|------|---------|
| 1万 | ~0.5秒 | ~20MB | ~20MB |
| 10万 | ~5秒 | ~50MB | ~200MB |
| **100万** | ~50秒 | ~200MB | ~2GB |
| 1000万 | ~500秒 | ~1GB | ~20GB |

💡 **推荐**：开发/测试阶段使用10万条，生产环境100万+条

---

## 🔀 权重和概率

### 什么是权重？

权重决定了每个值被选中的概率。例如：

```json
{
  "values": ["Python", "Java", "Go"],
  "weights": [0.5, 0.3, 0.2]
}
```

- Python被选中的概率：50%
- Java被选中的概率：30%
- Go被选中的概率：20%

### 设置权重的原则

1. **模拟现实分布**：
   ```json
   {
     "values": ["Senior", "Mid-level", "Junior"],
     "weights": [0.30, 0.50, 0.20]
   }
   ```
   （中级工程师最多，初级次之，高级最少）

2. **关键技术更常见**：
   ```json
   {
     "values": ["Python", "JavaScript", "Go", "Rust"],
     "weights": [0.40, 0.35, 0.15, 0.10]
   }
   ```

3. **地理分布**：
   ```json
   {
     "values": ["Remote", "San Francisco", "Beijing"],
     "weights": [0.50, 0.30, 0.20]
   }
   ```

---

## 💾 数据格式

### JSONL格式（推荐大规模）

每行一条JSON记录，易于流式处理：

```jsonl
{"tech_stack": ["Python", "Docker"], "seniority": ["Senior"], "location": ["Remote"], "id": "resume_000001"}
{"tech_stack": ["Java", "Kubernetes"], "seniority": ["Mid-level"], "location": ["Beijing"], "id": "resume_000002"}
```

**优点**：
- 支持流式读取（内存友好）
- 易于分片处理
- 适合百万级数据

### JSON格式（推荐查看、测试）

所有记录放在一个数组：

```bash
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/data_generator.py \
    --resumes 100 \
    --format json
```

**优点**：
- 结构清晰
- 易于查看
- 适合小规模数据

---

## 📊 数据验证

### 查看数据

```bash
# 查看前5条简历
head -5 data/generated/resumes_advanced.jsonl

# 用jq格式化查看
head -1 data/generated/resumes_advanced.jsonl | python -m json.tool
```

### 统计数据

```python
import json
from pathlib import Path
from collections import Counter

# 统计技术栈分布
skills_counter = Counter()
with open("data/generated/resumes_advanced.jsonl") as f:
    for line in f:
        data = json.loads(line)
        skills_counter.update(data.get("tech_stack", []))

# 显示Top 10
for skill, count in skills_counter.most_common(10):
    print(f"{skill}: {count}")
```

---

## 🛠️ Python API 使用

### 直接使用生成器

```python
from scripts.data.data_generator import ResumeGenerator, JobPostingGenerator

# 基础生成器
resume_gen = ResumeGenerator(seed=42)
jobs_gen = JobPostingGenerator(seed=42)

# 生成数据
for i in range(1000):
    resume = resume_gen.generate()
    job = jobs_gen.generate()
    print(resume.id, job.id)
```

### 使用高级生成器

```python
from scripts.data.advanced_generator import (
    AdvancedDataGenerator, PresetConfigs
)

# 创建配置
config = PresetConfigs.create_tech_stack_config()

# 创建生成器
generator = AdvancedDataGenerator(config, seed=42)

# 生成批次
resumes = generator.generate_resume_batch(10000)
jobs = generator.generate_job_batch(5000)

# 导出
import json
with open("output.jsonl", "w") as f:
    for resume in resumes:
        f.write(json.dumps(resume, ensure_ascii=False) + '\n')
```

---

## 📝 实际例子

### 例1：生成用于评估的测试集

```bash
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --preset matching \
    --resumes 10000 \
    --jobs 5000 \
    --output-dir data/evaluation
```

### 例2：生成性能基准测试数据

```bash
/d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
    --preset tech_stack \
    --resumes 1000000 \
    --jobs 500000 \
    --output-dir data/benchmark \
    --seed 42  # 保证可重复
```

### 例3：分批生成百万级数据

```bash
for batch in {1..10}; do
    /d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
        --preset tech_stack \
        --resumes 100000 \
        --jobs 50000 \
        --output-dir data/batch_$batch \
        --seed $batch
done

# 合并所有批次
cat data/batch_*/resumes_advanced.jsonl > data/final_resumes.jsonl
cat data/batch_*/jobs_advanced.jsonl > data/final_jobs.jsonl
```

---

## ❓ 常见问题

### Q: 数据要有多逼真？

A: 取决于用途：
- **开发测试**：简单随机即可 → 用方式2
- **RAG评估**：要求多维度合理组合 → 用方式3
- **性能基准**：要求大规模且多样 → 用方式3 + 百万级

### Q: 能否生成特定分布的数据？

A: 完全可以！修改权重：
```json
{
  "values": ["Python", "Java", "Go"],
  "weights": [0.8, 0.15, 0.05]  // Python占80%
}
```

### Q: 如何确保可重复性？

A: 使用 `--seed` 参数：
```bash
--seed 42
```

相同的seed会生成相同的数据。

### Q: 生成的数据能否直接导入Qdrant？

A: 是的，生成的JSONL格式可以直接用于向量化和导入。
见 GENERATOR_GUIDE.md 的"与Qdrant集成"部分。

---

## 📁 文件结构

```
scripts/data/
├── data_generator.py          ← 基础生成器
├── advanced_generator.py      ← 高级排列组合生成器
├── demo_generation.py         ← 演示脚本
├── GENERATOR_GUIDE.md         ← 完整指南
└── QUICK_REFERENCE.md         ← 本文件

data/
├── generated_demo/            ← 演示输出
│   ├── resumes_basic.jsonl
│   ├── jobs_basic.jsonl
│   ├── resumes_advanced_demo.jsonl
│   └── jobs_advanced_demo.jsonl
└── configs_demo/
    └── sample_config.json     ← 示例配置
```

---

## 🎓 学习路径

### 初级：快速体验
1. 运行演示脚本
2. 查看生成的数据格式
3. 理解权重和维度概念

### 中级：基础使用
1. 尝试不同的参数生成数据
2. 自定义简单的JSON配置
3. 理解JSONL格式优势

### 高级：大规模应用
1. 设计复杂的维度关联
2. 优化权重分布
3. 整合到完整的RAG管道

---

## 🚀 下一步

1. **运行演示**：
   ```bash
   /d/source/VedaAide.py/.venv/Scripts/python scripts/data/demo_generation.py
   ```

2. **查看数据**：
   ```bash
   cat data/generated_demo/resumes_advanced_demo.jsonl | head -1
   ```

3. **生成大规模数据**：
   ```bash
   /d/source/VedaAide.py/.venv/Scripts/python scripts/data/advanced_generator.py \
       --preset tech_stack \
       --resumes 100000 \
       --jobs 50000
   ```

4. **读完整指南**：
   [scripts/data/GENERATOR_GUIDE.md](GENERATOR_GUIDE.md)

---

**祝你使用愉快！🎉**
