# VedaAide: Interview-Ready RAG Agent System

## 1. Project Vision

Build an intelligent Agent system that can simulate personalized interview conversations. By analyzing deidentified experience data, it uses Agentic RAG technology to provide realistic interactive experiences.

**Core Value Propositions**:
- **Technical Exploration**: An interview conversation tool demonstrating end-to-end RAG implementation (deidentification, indexing, retrieval, evaluation)
- **Systematic Design**: Showcase engineering rigor through observability, quantitative evaluation, and security practices
- **Learning Reference**: A complete reference implementation for developers to understand RAG industrial-grade practices (from development to evaluation)
- **Resource-Aware**: Implement a complete system using only available free/discounted resources

---

## 2. Technology Stack (Tech Stack)

### Core Language & LLM Orchestration
- **Development Language**: Python 3.10+
- **Orchestration**:
  - LangChain / LangGraph: Agent state management, multi-step planning, and tool invocation
  - LlamaIndex: Data layer retrieval augmentation supporting hierarchical indexing and hybrid search
  - DSPy: Prompt compilation and optimization, reducing manual tuning overhead

### Vector Database & Data Storage
- **Vector DB**: Qdrant (local Docker + cloud hosting options)
- **Persistent Storage**: Azure CosmosDB (NoSQL) - stores detailed data from each retrieval, supporting evaluation and replay
- **Data Deidentification**: Unified sensitive information masking layer ensuring data security during demos and evaluations

### Model Access (LLM & Embedding)
- **Local Inference**: Ollama (Llama-3 / Phi-3)
- **Cloud APIs**:
  - Azure OpenAI: gpt-4o, gpt-4o-mini (LLM), text-embedding-3-small (Embedding)
  - DeepSeek API (cost optimization alternative)

### Observability & Evaluation Framework
- **Tracing**:
  - LangFuse (LangSmith alternative): Local Docker + cloud hosting with superior cost efficiency and privacy control
  - Custom Observability Layer: Decorator-based interception of Query, Contexts, Answer → written to CosmosDB
- **Quality Evaluation**:
  - RAGAS: Quantitative assessment of Faithfulness, Relevance, Recall
  - Reference-free Evaluation: User feedback (thumbs up/down) as optimization signals
- **Monitoring & Alerts**: Cost tracking, retrieval quality anomaly detection, API rate limiting

### Cost-Optimized Resources
- ✓ Azure OpenAI Deployments (existing quota)
- ✓ Azure CosmosDB (Free Tier / budget-controlled)
- ✓ Azure Container Apps (deployment runtime)
- ✓ Azure KeyVault (secret management)
- ✓ GitHub Pages (documentation/demo)
- ✓ GitHub Container Registry (image storage)

---

## 3. Core Feature Design

### A. Hierarchical Data Indexing with Deidentification (LlamaIndex-focused)
- **Multi-dimensional Data Ingestion**: Resume, project retrospectives, technical blogs, interview Q&A pairs
- **Unified Deidentification Framework**: Pre-ingestion masking of SSN, phone, email, addresses as `[REDACTED]`, ensuring safety during demos and evaluations
- **Hierarchical Retrieval Strategy**: "Summary retrieval → sub-chunk pinpointing" recursive retrieval, allowing Agent to answer both high-level and granular details
- **Hybrid Search**: BM25 + Vector Search combined for precise matching on domain terms (Kubernetes, Redis, etc.)

### B. Agentic Workflow with Adaptive Strategy (LangChain/LangGraph-focused)
- **Tool Suite**:
  1. `Experience_Comparator`: Compares current JD with personal resume, auto-highlights gaps
  2. `Technical_Deep_Dive`: Retrieves in-depth cases and details from library for specific tech stacks
  3. `Interview_Strategy_Agent`: Dynamically adjusts response emphasis based on interviewer tone (HR vs technical)
- **Self-Reflection Loop**: Agent pre-evaluates "Do my retrieved materials fully answer this question?" → triggers secondary retrieval if needed
- **Multi-turn Conversation Memory**: Maintains dialogue history, prevents repetition and omissions, supports cross-question coherence

### C. Observability & Auditability
- **Complete Chain Tracing**: LangFuse records every Agent step, retrieval, tool call, and reasoning process
- **Retrieval Data Persistence**: Every retrieval's Query, Top-K results, relevance scores stored in CosmosDB enabling:
  - Post-analysis and optimization
  - Performance benchmarking
  - User feedback correlation
- **Cost Monitoring**: Real-time tracking of token consumption, API call frequency, model selection (local vs cloud)

### D. Automated Evaluation & Optimization Pipeline (RAGAS & DSPy)
- **Synthetic Test Set Generation**: Generate 50+ standard interview questions from personal documents (TestsetGenerator)
- **Multi-model Evaluation**:
  - Use gpt-4o as reference standard
  - Use gpt-4o-mini for cost-optimized quick evaluation
- **DSPy Compilation Optimization**: Compile optimal prompts for Azure OpenAI and Ollama separately, addressing local model comprehension limitations
- **Reference-free Feedback Loop**: User thumbs up/down on each response becomes ground truth label for iterative optimization
- **Offline Evaluation Reports**: Visualize Faithfulness, Relevance, Recall score trends

### E. Multi-scenario Support
- **Recruitment Scenario**: 1-1 interview simulation with recruiter role-playing
- **Demo Scenario**: Tech talks, recruiting pitches, capability verification
- **Learning Scenario**: RAG system diagnosis, prompt engineering, evaluation methodology reference

---

## 4. Implementation Roadmap

### Phase 1: Infrastructure & Data Pipeline (Week 1-2)

**Infrastructure Setup**
- Deploy local Qdrant Docker and Ollama
- Configure Azure CosmosDB (NoSQL) connection pool and indexing strategies
- Set up LangFuse (local Docker container + optional cloud hosting)
- Configure Azure KeyVault for API keys and connection strings

**Data Processing**
- Build deidentification tool: identify and mask SSN, phone, email, addresses, etc.
- Prepare public sample datasets (mock resumes, job postings, English reading comprehension, etc.)
- Structure and ingest resume, projects using LlamaIndex (support user's own data or public datasets)
- Build multi-dimensional data model (resume, projects, Q&A, blogs)
- Establish data versioning for evaluation tracking

**Integration Verification**
- Connect Azure OpenAI + LlamaIndex for baseline RAG
- Validate Qdrant retrieval quality (reranking, recall)
- Establish basic logging and tracing framework

### Phase 2: Agent & Observability (Week 3-4)

**Agent Core**
- Define Agent state machine with LangGraph: Query → Retrieval → Reasoning → Reflection → Response
- Implement three core tools: Experience_Comparator, Technical_Deep_Dive, Interview_Strategy_Agent
- Multi-turn conversation memory management preventing repetition

**Observability & Persistence**
- Decorator-based auto-observability: intercept Query, Top-K Contexts, LLM Response → CosmosDB
- LangFuse integration: complete Agent execution tree
- Establish feedback mechanism for each response (User Feedback field)
- Cost dashboard: token consumption, API call stats, model usage distribution

**Testing & Optimization**
- Manual testing with deidentified data on basic workflows
- Qualitative evaluation on common question types

### Phase 3: Evaluation Framework & Intelligent Optimization (Week 5-6)

**RAGAS Evaluation Pipeline**
- Generate 50+ synthetic interview questions from documents (TestsetGenerator)
- Implement RAGAS evaluation: Faithfulness, Relevance, Recall
- Use gpt-4o as reference, gpt-4o-mini for cost-effective rapid evaluation
- Generate evaluation reports (visualization of score trends, problem classification stats)

**DSPy Compilation Optimization**
- Prompt compilation optimization for Azure OpenAI
- Prompt compilation optimization for Ollama local models
- Compare local vs cloud model evaluation results, determine optimal config

**Closed-loop Feedback**
- Reference-free feedback loop: thumbs up/down → label accumulation → prompt/retrieval strategy tuning
- Anomaly detection: identify high-frequency error patterns for precise optimization
- Continuous benchmarking: establish performance baseline, track improvement

### Phase 4: Demo & Documentation (Optional)

- Prepare interview demo scripts: showcase DSPy optimization, LangFuse tracing, RAGAS reports
- Document system design and lessons learned
- Publish GitHub Pages technical articles (observable RAG system design)

---

## 5. Key Details & Best Practices

### Data Security & Privacy
- **Deidentification Strategy**: Pre-ingestion masking of SSN, phone, email, address as `[REDACTED]`
- **Multi-stage Deidentification**: raw data → deidentified storage → CosmosDB persistence → LangFuse tracing, with verification at each stage
- **Demo Mode**: One-click switch to fully deidentified demo dataset for external presentations

### Performance & Cost Optimization
- **Async Evaluation**: RAGAS is time/token-intensive; use background tasks (Celery or asyncio), non-blocking to real-time responses
- **Model Selection Strategy**:
  - Real-time: prioritize Ollama (local, free) → gpt-4o-mini (low-cost) → gpt-4o (quality-critical)
  - Offline evaluation: batch use gpt-4o-mini, gpt-4o only when necessary
- **Vector DB Optimization**:
  - Enable Qdrant Hybrid Search (BM25 + Vector) for domain terms
  - Tune top_k, similarity_threshold for recall/precision balance
  - Regular cleanup of redundant vectors for storage cost control

### Observability & Auditability
- **Tracing**:
  - LangFuse records complete Agent execution tree
  - CosmosDB persists Query, Context, Score, Response for each retrieval
  - Custom metrics: retrieval latency, token consumption, model selection
- **Alerting**:
  - Retrieval recall anomaly: alert when < 0.5
  - Evaluation score decline: alert when Faithfulness drops > 5%
  - Cost overage: alert at 80% of monthly budget

### Hybrid Search & Recall Optimization
- **Professional Terms Challenge**: Pure vector search may miss keywords like Kubernetes, Redis
- **Hybrid Search Config**:
  - BM25 weight: 0.3 (exact keyword matching)
  - Vector weight: 0.7 (semantic relevance)
  - Support Metadata Filtering: by tech stack, time period, project type
- **Recursive Retrieval**: document summary → relevant sections → specific paragraphs for multi-level precision

### Reference-free Monitoring & Feedback
- **Feedback Mechanism**:
  - Collect 👍 / 👎 after each response
  - Write feedback to CosmosDB linked to Query, Context, Response, User ID
  - Analyze feedback distribution periodically for high-frequency error patterns
- **Iterative Optimization**:
  - Low-score questions → manual analysis → adjust Prompt / retrieval / data
  - Version comparison: A/B test new vs old Prompt on same question set

### Skills to JD Mapping
This project directly covers all core JD-001 requirements:

| JD Requirement | Project Implementation |
|---|---|
| Production RAG systems end-to-end | Complete pipeline: data deidentification → indexing → retrieval → Agent → evaluation |
| Vector databases (Qdrant, etc.) | Qdrant local + cloud, Hybrid Search optimization |
| LLM orchestration (LangChain, LlamaIndex, DSPy) | LangGraph Agent, LlamaIndex hierarchical indexing, DSPy compilation |
| Strong Python + modern LLM APIs | Python 3.10+, Azure OpenAI, Ollama, DeepSeek API |
| Evaluation (RAGAS, hallucination detection) | RAGAS quantitative eval, reference-free feedback, anomaly alerts |
| Debug retrieval quality systematically | CosmosDB persistence, LangFuse tracing, visualization analysis |

---

## 6. Interview Showcase Highlights

### Technical Depth Highlights

**Highlight 1: DSPy Compilation – 0.5ms inference with near-GPT-3.5 quality**
- Demonstrate local Llama-3 via DSPy achieving gpt-3.5-turbo-level RAG performance without changing a line of prompt
- Comparison charts: Ollama vs Azure OpenAI in evaluation scores, latency, cost
- Win: Cost ↓ 99%, Latency ↓ 90%, Quality ↑ near-parity

**Highlight 2: LangFuse Complete Tracing – diagnosing hallucinations**
- Open LangFuse dashboard showing complete execution tree of one interview Agent run
- Pinpoint hallucination root cause: retrieval precision issue or LLM reasoning flaw?
- Demonstrate CosmosDB data replay for precise issue diagnosis and iterative improvement
- Win: Observable, auditable, reproducible

**Highlight 3: RAGAS Quantitative Evaluation – data-driven optimization**
- Present RAGAS reports before/after system iteration:
  - Faithfulness: 0.75 → 0.92 (via data quality improvement)
  - Relevance: 0.80 → 0.95 (via Hybrid Search tuning)
  - Recall: 0.70 → 0.88 (via hierarchical indexing)
- Data-backed proof of Agent reliability on "resume matching"
- Win: Quantifiable, verifiable, continuous improvement

**Highlight 4: Multi-model Cost Optimization – production-grade system design**
- Demonstrate intelligent model selection (Ollama → gpt-4o-mini → gpt-4o) for cost control
- Token consumption monitoring dashboard with real-time cost calculation
- Monthly cost comparison: gpt-4o-only vs hybrid local Ollama
- Win: Engineering mindset, cost consciousness, production-ready

### System Design Highlights

**Highlight 5: Full-stack Data Deidentification**
- Show deidentification tool mechanics: identification, masking, verification
- Demonstrate complete transformation from raw resume to deidentified output
- Multi-stage validation: storage layer, tracing layer, presentation layer all scrubbed
- Win: Privacy-first, production-grade security considerations

**Highlight 6: Hybrid Search Power**
- Compare pure vector search vs Hybrid Search retrieval quality
- Case study: BM25 + Vector precisely matches Kubernetes, Redis, CI/CD terminology
- Metadata Filtering in action: tech stack and time-based fine-grained filtering
- Win: Thoughtful engineering, real-world considerations

### Capability Highlights

**Highlight 7: Reference-free Continuous Improvement Loop**
- Show how user feedback converts to improvement signals
- Example: low-score question set → pattern recognition → prompt tuning → new/old A/B test
- Data from last 3 iterations showing improvement trajectory
- Win: Closed-loop thinking, data-driven decisions

**Highlight 8: Engineering Best Practices**
- Code structure: modularity, single responsibility, testability
- Config management: environment variables, KeyVault integration, secure secret storage
- Async patterns: evaluation, logging via background tasks, non-blocking real-time response
- Version control: code tags, data snapshots, evaluation reports per iteration
- Win: high code quality standards

---

## Appendix: Quick Reference

### Key Technologies
- **LLM Orchestration**: LangChain, LangGraph, DSPy
- **Data Processing**: LlamaIndex (indexing & retrieval)
- **Vector Search**: Qdrant (hybrid search with BM25)
- **Data Storage**: Azure CosmosDB (retrieval persistence)
- **Evaluation**: RAGAS (quantitative quality metrics)
- **Tracing**: LangFuse (observable RAG)
- **Models**: Azure OpenAI (gpt-4o), Ollama (local inference)

### Success Metrics
- Faithfulness ≥ 0.90
- Relevance ≥ 0.90
- Recall ≥ 0.85
- Average retrieval latency ≤ 500ms
- Monthly cost ≤ $50 (with free tier optimization)
