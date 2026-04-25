# Public Sample Datasets for VedaAide

## Overview

This directory contains publicly available sample datasets designed for RAG system evaluation, user testing, and development purposes. All data is synthetic and completely free of private or sensitive information.

## Dataset Components

### 1. Sample Resumes (`sample_resumes.json`)

**Purpose**: Provide diverse resume examples for retrieval and ranking evaluation.

**Format**: JSON array with resume objects

**Structure**:
```json
{
  "id": "resume_001",
  "name": "Sample Resume 1",
  "content": "..."
}
```

**Characteristics**:
- 5 sample resumes covering different seniority levels
- Diverse technical backgrounds (Backend, Product, Data Science, DevOps, Frontend)
- Realistic but fictional professional experiences
- Well-structured with skills, experience, and accomplishments sections
- Used for: retrieval ranking, similarity matching, resume parsing evaluation

### 2. Job Postings (`sample_job_postings.json`)

**Purpose**: Provide job descriptions for matching, ranking, and relevance evaluation.

**Format**: JSON array with job posting objects

**Structure**:
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

**Characteristics**:
- 5 diverse job postings
- Different job levels (Junior, Mid, Senior)
- Various departments (Engineering, Product, Data Science, DevOps)
- Realistic salary ranges and benefits
- Used for: job-resume matching, requirement extraction, ranking evaluation

### 3. Reading Comprehension (`sample_reading_comprehension.json`)

**Purpose**: Provide English comprehension questions for RAG system evaluation.

**Format**: JSON array with question objects

**Structure**:
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

**Characteristics**:
- 5 reading passages with questions
- Multiple choice format (4 options each)
- Topics: AI, Climate Change, History, Machine Learning, Environment
- Difficulty: Medium level (suitable for general audience)
- Used for: QA evaluation, comprehension testing, answer quality assessment

## Dataset Statistics

| Component | Count | Size |
|-----------|-------|------|
| Resumes | 5 | ~1.5 KB |
| Job Postings | 5 | ~3 KB |
| Reading Questions | 5 | ~2.5 KB |
| **Total** | **15** | **~7 KB** |

## Usage

### Python Integration

Load datasets in your Python code:

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

### RAG System Evaluation

These datasets can be used for:

1. **Retrieval Testing**: Upload documents to vector database and test retrieval quality
2. **Ranking Evaluation**: Test BM25 and semantic similarity ranking
3. **QA Evaluation**: Test question answering using reading comprehension passages
4. **Job-Resume Matching**: Evaluate matching algorithms

### Example Use Cases

1. **Evaluate retrieval quality**: Index resumes and query with job requirements
2. **Test ranking algorithms**: Compare BM25 vs semantic similarity scores
3. **QA system evaluation**: Test answer generation with comprehension questions
4. **User interface testing**: Display sample data in UI without using real data

## Adding More Data

To expand the datasets:

1. Create new items following the existing JSON schema
2. Ensure all data is synthetic and non-personal
3. Update dataset statistics in this README
4. Commit changes with clear messages

## Dataset Management Strategy

VedaAide supports a **three-tier data strategy** to balance quick development with robust evaluation:

### 🎯 Tier 1: Static Sample Data (Committed to Git)

**Location**: `data/public_samples/` (5 samples per type)

```python
from src.core.data import DataLoader

loader = DataLoader(source="static")
resumes = loader.get_resumes()        # 5 samples
jobs = loader.get_jobs()              # 5 samples
qa_pairs = loader.get_qa_pairs()      # 5 samples
```

**Characteristics**:
- ✅ Always available, zero dependencies
- ✅ Fast (instant load)
- ✅ Small (~7 KB total)
- ✅ Suitable for demos and documentation
- ❌ Too small for comprehensive testing

**Use Cases**:
- Quick feature demonstrations
- Documentation examples
- CI/CD smoke tests
- Onboarding new developers

---

### 🔧 Tier 2: Synthetic Data Generation (Development & Testing)

**Location**: `scripts/data/data_generator.py` (configurable count)

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

**Characteristics**:
- ✅ Highly configurable (any count)
- ✅ Reproducible (with seed)
- ✅ Diverse scenarios and variations
- ✅ Fast generation (seconds to minutes)
- ✅ No external dependencies
- ⚠️ Synthetic data (not real-world)
- ⚠️ May not capture edge cases

**Generator Features**:
- Based on combinatorial permutations of job levels, tech stacks, and locations
- Realistic but fictional companies, names, and descriptions
- Salary ranges match market levels by experience
- Customizable through `DataRepository` class

**Command Line Usage**:
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

**Use Cases**:
- Local development and iteration
- Unit and integration tests
- Performance benchmarking
- Testing edge cases with custom seeds
- CI/CD pipeline testing (moderate scale)

---

### 📊 Tier 3: Public Datasets (Real-World Evaluation)

**Location**: Download on-demand from Kaggle, Hugging Face, or GitHub

```python
from src.core.data import DataLoader

# From Kaggle (requires API key setup)
loader = DataLoader(source="kaggle", dataset_id="...")
jobs = loader.get_jobs(count=100000)

# From Hugging Face Hub
loader = DataLoader(source="huggingface", repo_id="...")
resumes = loader.get_resumes(count=50000)
```

**Data Sources**:

#### Kaggle
- **Dataset**: "Job Postings from LinkedIn, Indeed, Glassdoor"
- **Records**: 100K-500K jobs across multiple regions
- **Size**: 50-200 MB
- **Setup**:
  ```bash
  pip install kaggle
  # Download API key from https://www.kaggle.com/settings/account
  # Place at ~/.kaggle/kaggle.json
  chmod 600 ~/.kaggle/kaggle.json
  ```
- **Cost**: Free (requires account)

#### Hugging Face Hub
- **Search**: https://huggingface.co/datasets?task_ids=task_ids,task_ids-other
- **Setup**:
  ```bash
  pip install huggingface-hub
  # Automatic login
  huggingface-cli login
  ```
- **Cost**: Free

#### GitHub Public Datasets
- **Examples**:
  - atulapra/Job-Market-Data
  - Other community job datasets
- **Setup**: `git clone` or download ZIP
- **Cost**: Free

**Characteristics**:
- ✅ Real-world data (actual job postings, resumes)
- ✅ Large scale (100K-500K+ records)
- ✅ Diverse industries and regions
- ✅ Production-ready
- ❌ Network dependency (first-time download)
- ❌ External dependencies (API keys, quotas)
- ❌ Slower to load (larger files)

**Use Cases**:
- Final evaluation and benchmarking
- Production model validation
- Real-world edge case discovery
- Research and publications
- Performance profiling at scale

---

### 📈 Recommended Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Lifecycle                     │
└─────────────────────────────────────────────────────────────┘

Day 1-2: Quick Prototyping
  ↓
  DataLoader(source="static")
  - Verify basic functionality
  - Test RAG pipeline structure
  - Validate output format

Day 3-5: Development & Testing
  ↓
  DataLoader(source="generated", seed=42)
  loader.get_jobs(count=1000)
  - Iterate on algorithms
  - Test retrieval quality
  - Profile performance locally

Week 1-2: Integration Testing
  ↓
  Mix Tier 2 + Tier 3:
    - Generated: Quick feedback loop
    - Kaggle: Realistic edge cases
  - Validate against real data
  - Fine-tune hyperparameters

Production Deployment
  ↓
  DataLoader(source="kaggle")  # or huggingface
  loader.get_jobs(count=100000)
  - Final validation
  - Scale testing
  - Production benchmarking
```

---

### 🎛️ DataLoader API Reference

```python
from src.core.data import DataLoader, get_sample_data

# Create a loader
loader = DataLoader(source="generated", seed=42)

# Load different data types
resumes = loader.get_resumes(count=1000)
jobs = loader.get_jobs(count=1000)
qa_pairs = loader.get_qa_pairs(count=500)

# Quick function for one-off loads
jobs = get_sample_data("jobs", source="static", count=10)

# List available sources
sources = DataLoader.available_sources()
# ['static', 'generated', 'kaggle', 'huggingface', 'hf']

# Show source information
print(DataLoader.info())  # All sources
print(DataLoader.info("generated"))  # Specific source

# Command line
$ python -m src.core.data --source generated --type jobs --count 1000 --seed 42
$ python -m src.core.data --list
$ python -m src.core.data --info
```

---

### 🔮 Future Extensions

The factory pattern enables easy addition of new sources:

```python
# Example: Add a custom data source
class CustomDataSource(DataSource):
    def load_resumes(self, count=5, **kwargs):
        # Your implementation
        pass

# Register it
DataSourceFactory.register("custom", CustomDataSource)

# Use it
loader = DataLoader(source="custom")
```

---

## Quality Standards

All data in this directory:
- ✅ Is completely synthetic (no real people or companies)
- ✅ Is free of sensitive information
- ✅ Follows consistent JSON formatting
- ✅ Includes metadata (IDs, descriptions)
- ✅ Is suitable for public sharing

## License

These datasets are provided as part of the VedaAide project for evaluation and testing purposes. Feel free to use them in your development and testing workflows.

## Related Tasks

- **Task 1.5**: Prepare public sample datasets ← **You are here**
- **Task 1.6**: Import and prepare deidentified data (uses these datasets)
- **Task 1.7**: Verify basic RAG pipeline (evaluates using these datasets)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-24 | Initial release with 5 resumes, 5 jobs, 5 reading questions |

---

**Last Updated**: 2026-04-24
**Maintainer**: VedaAide Team
