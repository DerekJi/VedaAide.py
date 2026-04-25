# VedaAide: Interview-Ready RAG Agent System

## 1. Project Vision

Build an intelligent Agent system that simulates personalized interview conversations. By analyzing a deidentified experience library, it uses Agentic RAG technology to provide realistic interactive interview experiences.

**Core Value Propositions**:
- **Technical Showcase**: Demonstrate end-to-end RAG + Agent engineering capabilities to recruiters (LlamaIndex indexing, LangGraph Agent, DSPy optimization)
- **Runnable Demo**: Published as a CLI tool — recruiters can try it with `pip install vedaaide`
- **Learning Reference**: A practical example for developers to understand the complete RAG pipeline (from indexing to evaluation)
- **Focused & Practical**: Concentrate on RAG/Agent core capabilities; avoid spending time on infra/DevOps that isn't the showcase goal

---

## 2. Technology Stack

### Core Language & LLM Orchestration
- **Language**: Python 3.10+
- **Orchestration**:
  - LangChain / LangGraph: Agent state management, multi-step planning, and tool invocation
  - LlamaIndex: Data layer retrieval augmentation with hierarchical indexing and hybrid search
  - DSPy: Prompt compilation and optimization, reducing manual tuning overhead

### Vector Database & Configuration
- **Vector DB**: Qdrant (local Docker)
- **Config Management**: `.env` + `python-dotenv` (simple and direct, no KeyVault required)
- **Data Deidentification**: Unified sensitive information masking layer for demo safety

### Model Access (LLM & Embedding)
- **Local Inference**: Ollama (Llama-3 / Phi-3)
- **Cloud APIs**:
  - Azure OpenAI: gpt-4o, gpt-4o-mini (LLM), text-embedding-3-small (Embedding)
  - DeepSeek API (cost optimization alternative)

### Evaluation & Observability (Lightweight)
- **Chain Tracing**: LangFuse (local Docker, optional — for demonstrating Agent execution chains)
- **Quality Evaluation**: RAGAS (Faithfulness, Relevance, Recall metrics)

### Distribution
- ✓ PyPI package (`pip install vedaaide`)
- ✓ GitHub source (with sample datasets)
- ✓ GitHub Pages (documentation)

---

## 3. Core Features

### A. Hierarchical Data Indexing with Deidentification (LlamaIndex-focused)
- **Multi-dimensional Data Ingestion**: Resume, project retrospectives, technical blogs, interview Q&A pairs
- **Unified Deidentification Framework**: Pre-ingestion masking of SSN, phone, email, addresses as `[REDACTED]`, ensuring safety during demos
- **Hierarchical Retrieval Strategy**: "Summary retrieval → sub-chunk pinpointing" recursive retrieval, letting the Agent answer both high-level and granular questions
- **Hybrid Search**: BM25 + Vector Search for precise matching on domain terms (Kafka, Redis, etc.)

### B. Agentic Workflow with Adaptive Strategy (LangChain/LangGraph-focused)
- **Tool Suite**:
  1. `Experience_Comparator`: Compares current JD with personal resume, auto-highlights gaps
  2. `Technical_Deep_Dive`: Retrieves in-depth cases and details from library for specific tech stacks
  3. `Interview_Strategy_Agent`: Dynamically adjusts response emphasis based on interviewer tone (HR vs technical)
- **Self-Reflection Loop**: Agent pre-evaluates "Do my retrieved materials fully answer this question?" → triggers secondary retrieval if needed
- **Multi-turn Conversation Memory**: Maintains dialogue history, prevents repetition and omissions, supports cross-question coherence

### C. Evaluation Framework (RAGAS & DSPy)
- **Synthetic Test Set Generation**: Generate 50+ standard interview questions from personal documents (TestsetGenerator)
- **RAGAS Quantitative Evaluation**: Compute Faithfulness, Relevance, Recall
- **DSPy Compilation Optimization**: Compile optimal prompts for Azure OpenAI and Ollama separately, addressing local model limitations

### D. Observability (Optional Demo)
- **Local LangFuse Instance**: Existing `langfuse_storage/` data; can demonstrate complete Agent execution chains during demo
- **Use Case**: Diagnose hallucination root causes; show visibility into Retrieval → Reasoning pipeline

### E. CLI Tool
- **Install**: `pip install vedaaide`
- **Commands** (detailed UX design TBD):
  - `vedaaide index <docs_dir>`: index documents
  - `vedaaide chat`: start interview conversation
  - `vedaaide eval`: run RAGAS evaluation

---

## 4. Implementation Roadmap

### Phase 1: Data Pipeline Basics (Week 1-2)

**Environment Setup**
- Start local Qdrant (Docker)
- Configure `.env`: Azure OpenAI API Key, Qdrant connection info
- Optional: start local LangFuse (existing `langfuse_storage/`)

**Data Processing**
- Build deidentification tool: identify and mask SSN, phone, email, addresses
- Prepare public sample datasets (mock resumes, job postings)
- Use LlamaIndex for document cleaning, chunking, and vector ingestion

**Baseline Validation**
- Connect Azure OpenAI + LlamaIndex for basic RAG
- Validate Qdrant hybrid search (BM25 + Vector) quality
- Unit tests covering deidentification tool

### Phase 2: Agent Core (Week 3-4)

**LangGraph Agent**
- Define state machine: Query → Retrieval → Reasoning → Reflection → Response
- Implement three core tools: `ExperienceComparator`, `TechnicalDeepDive`, `InterviewStrategySelector`
- Multi-turn conversation memory management

**Initial CLI**
- `vedaaide index`: document indexing command
- `vedaaide chat`: interactive interview conversation

**Testing**
- Unit tests for all Agent tools
- Integration test: end-to-end RAG query flow

### Phase 3: Evaluation & Optimization (Week 5-6)

**RAGAS Evaluation**
- Synthetic test set (50+ interview questions)
- Compute Faithfulness, Relevance, Recall
- Generate evaluation reports

**DSPy Optimization**
- Compile prompts for Azure OpenAI and Ollama separately
- Compare RAGAS scores before and after optimization

**CLI Expansion**
- `vedaaide eval`: run evaluation command
- `vedaaide eval --compare`: compare evaluation results across configurations

### Phase 4: Release & Documentation (Week 7-8)

**PyPI Release**
- Finalize `pyproject.toml` (package config, CLI entry points)
- Write installation guide and quick-start documentation
- Publish to PyPI

**Documentation**
- README 5-minute quick start
- System design document
- Demo script (LangFuse chain visualization, RAGAS report)

### Future (TBD)

- CLI UX detailed design (user interaction flow, help documentation)

---

## 5. Key Practices

### Data Security & Privacy
- **Deidentification Strategy**: Pre-ingestion masking of SSN, phone, email, address as `[REDACTED]`
- **Demo Mode**: Repository includes fully deidentified public sample datasets — users can try without providing personal data

### Hybrid Search & Recall Optimization
- **Professional Terms Challenge**: Pure vector search may miss keywords like Kafka, Redis
- **Hybrid Search Config**:
  - BM25 weight: 0.3 (exact keyword matching)
  - Vector weight: 0.7 (semantic relevance)
  - Metadata Filtering: by tech stack, time period, project type
- **Recursive Retrieval**: document summary → relevant sections → specific paragraphs

### Model & Cost Strategy
- **Real-time conversations**: prefer Ollama (local, free) → gpt-4o-mini (low-cost) → gpt-4o (quality)
- **Offline evaluation**: batch with gpt-4o-mini, gpt-4o only when necessary
- **Configuration**: switch models via `.env`, no code changes needed

### Skills to JD Mapping
This project directly covers the core RAG/Agent requirements from JD-001:

| JD Requirement | Project Implementation |
|---|---|
| Production RAG systems end-to-end | Full pipeline: deidentification → indexing → hybrid retrieval → Agent → RAGAS evaluation |
| Vector databases (Qdrant, etc.) | Qdrant local, Hybrid Search (BM25 + Vector) optimization |
| LLM orchestration (LangChain, LlamaIndex, DSPy) | LangGraph Agent, LlamaIndex hierarchical indexing, DSPy compilation |
| Strong Python + modern LLM APIs | Python 3.10+, Azure OpenAI, Ollama, DeepSeek API |
| Evaluation (RAGAS, hallucination detection) | RAGAS quantitative eval, LangFuse tracing (optional) |
| Debug retrieval quality systematically | RAGAS metric analysis, LangFuse trace diagnosis, evaluation report comparison |

---

## 6. Interview Showcase Highlights

### Technical Depth

**Highlight 1: DSPy Compilation – local model approaching cloud quality**
- Demonstrate local Llama-3 via DSPy achieving near-gpt-3.5-turbo RAG performance
- Comparison charts: Ollama vs Azure OpenAI RAGAS scores, latency
- Key value: cost optimization + understanding prompt compilation principles

**Highlight 2: RAGAS Quantitative Evaluation – data-driven optimization**
- Present RAGAS reports before/after system iteration (Faithfulness, Relevance, Recall trends)
- Show how metrics pinpoint problems (low recall → retrieval strategy issue / low Faithfulness → generation issue)
- Key value: quantifiable, verifiable, continuous improvement

**Highlight 3: Hybrid Search Power**
- Compare pure vector search vs Hybrid Search retrieval quality
- Case study: BM25 + Vector precisely matching Kafka, Redis, CI/CD terminology
- Key value: understanding retrieval system design trade-offs

**Highlight 4: LangFuse Agent Execution Chain (optional demo)**
- Open local LangFuse dashboard showing a complete interview Agent execution tree
- Pinpoint hallucination root cause: retrieval precision or LLM reasoning issue
- Key value: observable, debuggable, reproducible

### Engineering Capability

**Highlight 5: Full-stack Data Deidentification**
- Show deidentification tool mechanics: identification, masking, verification
- Demonstrate transformation from raw resume to deidentified output
- Key value: privacy awareness, practical engineering considerations

**Highlight 6: CLI Tool Design** (after Phase 4)
- `pip install vedaaide` + 5-minute runnable demo
- Thoughtful command structure considering user experience
- Key value: engineering mindset, product thinking

---

## Related Documents

- **[Project Structure](../PROJECT_STRUCTURE.en.md)** - Codebase organization, naming conventions, test structure
- **[Agent Scenarios](AgentScenarios.en.md)** - Agent configuration for different use cases
- **[Basics](00.basics.en.md)** - Project constraints and design considerations
- **[Task Breakdown](TASK_BREAKDOWN.en.md)** - Detailed actionable task list
