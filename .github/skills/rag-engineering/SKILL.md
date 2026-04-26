---
name: rag-engineering
description: Best practices for VedaAide's RAG (Retrieval-Augmented Generation) system, covering architecture design, hybrid search optimization, vector database management, and prompt engineering
applyTo: "src/core/retrieval/**,src/core/rag/**,src/core/embedding/**"
keywords:
  - retrieval
  - rag
  - embedding
  - qdrant
  - ranking
  - hybrid-search
  - vector
  - semantic
  - 检索
  - RAG
  - 嵌入
  - 向量
  - 重排序
  - 混合搜索
  - 语义搜索
  - 向量数据库
whenToUse: |
  When implementing or optimizing:
  - Hybrid search strategies (BM25 + Vector)
  - Qdrant vector database operations
  - Embedding models and chunking strategies
  - Retrieval pipeline architecture
  - Metadata filtering for context search
---

# RAG Engineering for VedaAide

## RAG Architecture Principles

### Key Components

1. **Data Preparation**
   - Raw data → Cleaning & Deidentification → Chunking → Embedding → Vector DB

2. **Retrieval**
   - Query Embedding → Vector Search → Hybrid Search → Reranking

3. **Generation**
   - Context Assembly → Prompt Engineering → LLM Generation

4. **Evaluation**
   - RAGAS Quantitative Evaluation
   - Reference-free User Feedback

### VedaAide Specific Implementation

```
User Query
  ↓
[Deidentifier] - Deidentification Check
  ↓
[Agent State Machine] - Decision Routing
  ├→ [Experience_Comparator Tool]
  ├→ [Technical_Deep_Dive Tool]
  └→ [Interview_Strategy Tool]
  ↓
[Retrieval Pipeline]
  ├→ Query Embedding (text-embedding-3-small)
  ├→ Qdrant Hybrid Search (BM25 + Vector)
  ├→ Reranking (optional)
  └→ Context Assembly
  ↓
[LLM Generation]
  ├→ Prompt Manager (version control)
  ├→ Azure OpenAI / Ollama
  └→ DSPy Optimization
  ↓
[Self-Reflection]
  └→ Quality check, re-retrieve if needed
  ↓
[Observability]
  ├→ LangFuse Tracing
  ├→ CosmosDB Persistence
  └→ Metrics Collection
  ↓
Final Response
```

## Retrieval Optimization

### Hybrid Search

In VedaAide, resumes contain many technical terms (Kafka, Redis, CI/CD, etc.). Pure vector retrieval often misses important keywords.

**Configuration Example**:
```python
from src.core.retrieval.retriever import HybridRetriever

retriever = HybridRetriever(
    bm25_weight=0.3,  # keyword matching weight
    vector_weight=0.7,  # semantic relevance weight
    top_k=5
)

# Automatically combines BM25 + Vector Search
results = retriever.retrieve("Kafka streaming platform experience")
# Results include both exact "Kafka" matches and semantically related experience
```

### Metadata Filtering

```python
# Filter by tech stack
results = retriever.retrieve(
    "backend development",
    filters={
        "tech_stack": {"$in": ["Python", "Go", "Java"]},
        "year_range": {"$gte": 2020}
    }
)

# Filter by project type
results = retriever.retrieve(
    "cloud infrastructure",
    filters={
        "project_type": "infrastructure"
    }
)
```

### Recursive Retrieval

```python
# LlamaIndex supports multi-level retrieval
from llama_index.indices.document_summary import DocumentSummaryIndex

# Level 1: Summary-level retrieval
summaries = summary_index.retrieve("Kafka experience")

# Level 2: Detailed chunks of related documents
detailed_results = detail_index.retrieve_for_summaries(summaries)

# Level 3: Precise passages (if needed)
precise_chunks = chunk_index.retrieve_for_documents(detailed_results)
```

## Vector Database Management

### Qdrant Configuration

```python
from src.infrastructure.db.qdrant import QdrantClient

client = QdrantClient(
    url="http://localhost:6333",  # local development
    # or url="https://your-qdrant-cloud.qdrant.io"  # cloud
    api_key="your-api-key"
)

# Create collection (if needed)
client.create_collection(
    collection_name="resumes",
    vector_size=1536,  # text-embedding-3-small dimension
    distance="cosine"
)

# Persist vectors
embeddings = embedding_model.embed_documents(texts)
client.upsert_vectors(
    collection_name="resumes",
    vectors=embeddings,
    payloads=metadata  # store text, source, etc.
)
```

### Index Update Strategy

**Incremental Update**:
```python
# When adding new documents, only compute new embeddings
new_doc = Document(text="New experience...", metadata={...})
new_embedding = embedding_model.embed(new_doc.text)
client.upsert(
    collection_name="resumes",
    ids=[new_doc.id],
    vectors=[new_embedding],
    payloads=[new_doc.metadata]
)
```

**Batch Update**:
```python
# When deidentification rules change, reprocess entire dataset
documents = load_raw_documents()
deidentified = deidentifier.process_batch(documents)
embeddings = embedding_model.embed_documents([d.text for d in deidentified])
client.recreate_and_upsert(
    collection_name="resumes",
    vectors=embeddings,
    payloads=[d.metadata for d in deidentified]
)
```

## Prompt Management

### Prompt Version Control

Maintain Prompt versions in `config/prompts/`:

```yaml
# system_prompts.yaml
interview_system_v1:
  template: |
    You are an expert recruiter evaluating a candidate.
    Be fair, thorough, and strategic.

    Candidate Experience:
    {experiences}

    Job Description:
    {jd}

    Question: {question}

  temperature: 0.7
  max_tokens: 1000

interview_system_v2:
  template: |
    You are an expert HR/Technical Interviewer.
    Provide strategic, insightful feedback based on the candidate's background.
    ...
  temperature: 0.6
  max_tokens: 1200
```
