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
