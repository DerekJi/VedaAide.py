# VedaAide 公开示例数据集

## 概览

本目录包含用于 RAG 系统评估、用户测试与开发演示的公开示例数据。所有数据均为合成数据，不包含真实个人隐私信息。

## 数据集组成

### 1. 简历样本（sample_resumes.json）

用途：用于检索、排序与匹配评估。

格式：JSON 数组。

结构示例：

```json
{
  "id": "resume_001",
  "name": "Sample Resume 1",
  "content": "..."
}
```

特点：
- 共 10 份简历样本
- 覆盖不同技术方向与资历层级
- 内容真实风格但均为虚构
- 适用于检索相关性、相似度匹配、简历解析评估

### 2. 岗位样本（sample_job_postings.json）

用途：用于岗位匹配、相关性排序与需求抽取评估。

格式：JSON 数组。

结构示例：

```json
{
  "id": "job_001",
  "title": "Senior Software Engineer - Backend",
  "company": "TechCorp Inc",
  "location": "Remote",
  "level": "Senior",
  "salary_min": 150000,
  "salary_max": 200000,
  "description": "...",
  "requirements": [...],
  "benefits": [...]
}
```

特点：
- 共 10 个岗位样本
- 覆盖 Junior / Mid / Senior 等级
- 覆盖工程、产品、数据、运维等方向
- 适用于岗位-简历匹配、需求抽取、排序评估

### 3. 阅读理解样本（sample_reading_comprehension.json）

用途：用于英文问答与理解能力评估。

格式：JSON 数组。

结构示例：

```json
{
  "id": "reading_001",
  "passage": "...",
  "question": "...",
  "options": [...],
  "correct_answer": "B",
  "explanation": "..."
}
```

特点：
- 共 5 组阅读理解题
- 四选一选择题格式
- 可用于问答质量与解释质量评估

## 数据统计

| 组件 | 数量 | 大小 |
|------|------|------|
| 简历 | 10 | ~3.5 KB |
| 岗位 | 10 | ~7 KB |
| 阅读理解 | 5 | ~2.5 KB |
| 总计 | 25 | ~13 KB |

## 使用方式

### Python 代码加载

```python
import json

# Load resumes
with open('data/public_samples/sample_resumes.json', 'r') as f:
    resumes = json.load(f)

# Load job postings
with open('data/public_samples/sample_job_postings.json', 'r') as f:
    jobs = json.load(f)

# Load reading comprehension
with open('data/public_samples/sample_reading_comprehension.json', 'r') as f:
    questions = json.load(f)

# Use in RAG evaluation
for resume in resumes:
    print(f"Resume ID: {resume['id']}")
    print(f"Content preview: {resume['content'][:100]}...")
```

### RAG 评估场景

可用于：
1. 检索效果测试
2. 排序算法评估（BM25 vs 向量检索）
3. 问答质量评估
4. 岗位-简历匹配验证

## 数据扩展建议

1. 按现有 JSON Schema 新增样本。
2. 保持纯合成数据，不引入真实个人信息。
3. 更新本文件中的统计信息。
4. 使用清晰的提交信息记录变更。

## 三层数据策略

### Tier 1：静态样本数据（纳入版本管理）

位置：data/public_samples/（10 份简历，10 份岗位，5 份 QA）

```python
from src.core.data import DataLoader

loader = DataLoader(source="static")
resumes = loader.get_resumes()        # 10 samples
jobs = loader.get_jobs()              # 10 samples
qa_pairs = loader.get_qa_pairs()      # 5 samples
```

特点：
- 始终可用、无外部依赖
- 加载快
- 适合演示与快速验证

### Tier 2：合成数据生成（开发与测试）

位置：scripts/data/data_generator.py（数量可配置）

```python
from src.core.data import DataLoader

# Generate 1000 resumes and 1000 jobs
loader = DataLoader(source="generated", seed=42)
resumes = loader.get_resumes(count=1000)
jobs = loader.get_jobs(count=1000)

# Or generate with different seed for variety
loader2 = DataLoader(source="generated", seed=123)
more_jobs = loader2.get_jobs(count=500)
```

命令行示例：

```bash
# Generate to JSON
python scripts/data/data_generator.py \
  --resumes 1000 \
  --jobs 1000 \
  --output-dir data/working_datasets \
  --format json \
  --seed 42

# Generate to JSONL (better for large datasets)
python scripts/data/data_generator.py \
  --resumes 10000 \
  --jobs 10000 \
  --output-dir data/working_datasets \
  --format jsonl
```

### Tier 3：公共真实数据集（评估）

位置：按需从 Kaggle、Hugging Face 或 GitHub 下载。

```python
from src.core.data import DataLoader

# From Kaggle (requires API key setup)
loader = DataLoader(source="kaggle", dataset_id="...")
jobs = loader.get_jobs(count=100000)

# From Hugging Face Hub
loader = DataLoader(source="huggingface", repo_id="...")
resumes = loader.get_resumes(count=50000)
```

更多细节可参考英文版：[README.md](README.md)。
