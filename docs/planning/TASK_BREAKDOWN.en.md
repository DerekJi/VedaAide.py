# VedaAide Task Breakdown

Each task includes:
- **Objective**: Clear end state
- **Acceptance Criteria**: How to verify completion
- **Estimated Hours**: Time estimate
- **Priority**: P0/P1/P2

---

## Phase 1: Data Pipeline + CLI Scaffold (Week 1-2)

> Goal: Build a working baseline RAG pipeline and establish the CLI framework
> (command structure, LLM selection, parameter system) as the foundation for later phases.

### Task 1.1: Deploy Qdrant Local Dev Environment

**Objective**
- Run Qdrant in local Docker
- Create initial Collection
- Verify HTTP API and Python SDK connectivity

**Acceptance Criteria**
- `docker compose ps` shows qdrant service running
- `curl http://localhost:6333/health` returns 200
- Python script can connect and perform basic operations (insert vectors, search)

**Estimated Hours**: 2h | **Priority**: P0

---

### Task 1.2: Configure Environment Variables

**Objective**
- Create `.env.example` template (all required variables)
- Verify `python-dotenv` reads config correctly
- Document all variables

**Acceptance Criteria**
- `.env.example` includes Azure OpenAI Key, Qdrant URL, model names, etc.
- No hardcoded API keys in source code
- README has environment variable setup instructions

**Estimated Hours**: 1h | **Priority**: P0

**Related Files**
- `.env.example`
- `src/utils/config.py`

---

### Task 1.3: Build Data Deidentification Tool

**Objective**
- Implement masking functions: SSN, phone, email, address
- Write unit tests
- Validate performance and accuracy

**Acceptance Criteria**
- All deidentification functions coverage >= 90%
- Correctly handles edge cases (empty strings, multilingual, special chars)
- Performance: processes 1000 resumes in < 5 seconds
- No original PII found in deidentified output

**Estimated Hours**: 4h | **Priority**: P0

**Related Files**
- `src/core/retrieval/deidentifier.py`
- `tests/unit/test_deidentifier.py`

---

### Task 1.4: Prepare Public Sample Datasets

**Objective**
- Create mock resumes (>= 10) and job postings (>= 10)
- Ensure all data is PII-free
- Document data format

**Acceptance Criteria**
- All files under `data/public_samples/` with clear format
- Deidentification tool validates 100% pass on sample data
- `data/public_samples/README.md` updated

**Estimated Hours**: 3h | **Priority**: P0

**Related Files**
- `data/public_samples/`

---

### Task 1.5: LlamaIndex Document Indexing Pipeline (Baseline)

**Objective**
- Implement document loading (PDF, Markdown, plain text)
- Implement chunking strategy (recursive retrieval: summary -> sub-chunks)
- Vectorize with Azure OpenAI Embedding and write to Qdrant

**Acceptance Criteria**
- Successfully imports all documents from sample dataset
- Qdrant Collection contains expected number of vectors
- Unit tests cover core indexing logic >= 80%

**Estimated Hours**: 4h | **Priority**: P0

**Related Files**
- `src/core/retrieval/indexer.py`
- `tests/unit/test_indexer.py`

---

### Task 1.6: Baseline RAG Query Validation

**Objective**
- Implement simple RAG query: Query -> Retrieval -> Generation
- Validate baseline retrieval quality (scaffold acceptance)

**Acceptance Criteria**
- Successfully executes end-to-end queries
- Retrieves semantically relevant documents (manual relevance check >= 0.6)
- Single query latency < 5 seconds
- Integration tests written and passing

**Estimated Hours**: 3h | **Priority**: P0

**Related Files**
- `src/core/rag/pipeline.py`
- `tests/integration/test_rag_pipeline.py`

---

### Task 1.7: CLI Scaffold Design and Implementation

**Objective**
- Define CLI command structure (`index` / `chat` / `eval`)
- Implement LLM selection (`--llm azure|ollama|deepseek`)
- Implement common flags (`--verbose`, `--config`, `--collection`)
- Configure pyproject.toml CLI entry points
- Implement `vedaaide --help` and per-command help

**CLI Design Spec**

```
vedaaide index <docs_dir>
    --llm azure|ollama|deepseek     # LLM backend for embedding
    --collection <name>             # Qdrant collection name (default: vedaaide)
    --recursive                     # Scan subdirectories recursively
    --verbose                       # Show detailed progress

vedaaide chat
    --llm azure|ollama|deepseek     # LLM backend for inference
    --model <model_name>            # Model name (e.g. llama3, gpt-4o-mini)
    --collection <name>             # Dataset collection to use
    --temperature <float>           # Temperature (default: 0.1)
    --top-k <int>                   # Retrieval Top-K (default: 5)
    --verbose                       # Show retrieved context

vedaaide eval
    --test-set <path>               # Path to test set
    --llm azure|ollama|deepseek     # LLM backend for evaluation
    --output <path>                 # Evaluation report output path
    --compare <v1_result> <v2_result>  # Compare two evaluation results
```

**Acceptance Criteria**
- `vedaaide --help` shows clear command descriptions
- `vedaaide index --help` shows all parameters
- `--llm azure` uses Azure OpenAI, `--llm ollama` uses Ollama
- Missing params show sensible defaults and friendly prompts
- Invalid params show clear error messages

**Estimated Hours**: 4h | **Priority**: P0

**Related Files**
- `src/cli/__main__.py`
- `src/cli/commands/`
- `pyproject.toml`

---

## Phase 2: RAG Quality Enhancement (Week 3-4)

> Goal: Upgrade the scaffold RAG to production-grade retrieval quality.
> Covers: deduplication, hybrid retrieval tuning, reranking, anti-hallucination.

### Task 2.1: Deduplication and Incremental Indexing

**Objective**
- Implement document fingerprinting (content hash) to prevent duplicate indexing
- Implement incremental update: only index new/modified documents
- Implement deletion: remove vectors for deleted documents from Qdrant

**Acceptance Criteria**
- Indexing same file twice does not produce duplicate vectors
- Modified file re-indexed: old vectors updated
- Deleted file re-indexed: corresponding vectors removed
- Unit test coverage >= 85%

**Estimated Hours**: 4h | **Priority**: P0

**Related Files**
- `src/core/retrieval/indexer.py`
- `tests/unit/test_indexer.py`

---

### Task 2.2: Hybrid Retrieval Tuning

**Objective**
- Tune BM25 / Vector weight fusion ratio
- Validate recall precision for technical terms (Kafka, Redis, etc.)
- Implement metadata filtering (by tech stack, time period, document type)
- Implement query preprocessing (expand abbreviations, normalize tech terms)

**Acceptance Criteria**
- Technical term recall rate >= 95%
- Metadata filtering: tech stack filter returns only relevant passages
- A/B test: hybrid vs. pure vector, relevance improvement >= 10%
- Unit tests cover hybrid fusion logic

**Estimated Hours**: 5h | **Priority**: P0

**Related Files**
- `src/core/retrieval/retriever.py`
- `tests/unit/test_retriever.py`

---

### Task 2.3: Reranking

**Objective**
- Integrate Cross-Encoder reranking (`sentence-transformers` or Azure Reranker)
- Implement two-stage retrieval: Recall -> Rerank
- Tune recall count (Top-N for rerank -> Top-K final)

**Acceptance Criteria**
- Reranked Top-3 relevance >= Recall stage Top-3 relevance
- Latency increase controlled within 1 second
- Unit tests cover Reranker interface >= 80%
- Integration tests verify two-stage retrieval flow

**Estimated Hours**: 5h | **Priority**: P0

**Related Files**
- `src/core/retrieval/retriever.py` (new: `TwoStageRetriever`)
- `tests/unit/test_retriever.py`

---

### Task 2.4: Anti-Hallucination

**Objective**
- Implement answer grounding: every answer fragment must trace back to source documents
- Implement confidence threshold: reject generation when retrieval score is below threshold, prompt "insufficient information"
- Implement source citation: append `[Source: ...]` to answers
- Implement Self-Check loop: LLM verifies answer consistency with context after generation

**Acceptance Criteria**
- For deliberately off-topic queries, system returns "no relevant information found" rather than fabricating
- All answers include traceable source citations
- Self-Check intercepts >= 80% of clearly wrong answers (validated on test set)
- Unit tests cover confidence logic and Self-Check flow

**Estimated Hours**: 6h | **Priority**: P0

**Related Files**
- `src/core/rag/pipeline.py` (new: `AnswerVerifier`)
- `tests/unit/test_rag_pipeline.py`

---

### Task 2.5: Contextual Compression

**Objective**
- Implement LLM-based context compression: extract key sentences relevant to the query from long passages
- Reduce noisy context, improve LLM generation quality
- Lower token consumption

**Acceptance Criteria**
- Compressed context length reduced by >= 30% vs. original
- RAGAS Faithfulness does not decrease vs. uncompressed version
- Token consumption reduced >= 20%
- Unit tests cover compression logic

**Estimated Hours**: 4h | **Priority**: P1

**Related Files**
- `src/core/retrieval/retriever.py` (new: `ContextCompressor`)
- `tests/unit/test_retriever.py`

---

### Task 2.6: RAG Quality Integration Tests

**Objective**
- Write end-to-end tests covering dedup, hybrid retrieval, reranking, anti-hallucination full pipeline
- Establish baseline evaluation metrics (for comparison in later phases)

**Acceptance Criteria**
- All RAG quality feature integration tests passing
- Baseline RAGAS metrics recorded (Faithfulness / Relevance / Recall)
- Tests cover edge cases: zero-result queries, very long documents, mixed languages

**Estimated Hours**: 3h | **Priority**: P1

**Related Files**
- `tests/integration/test_rag_pipeline.py`

---

## Phase 3: Agent Core (Week 5-6)

> Goal: Build Agent workflow on top of high-quality RAG, enabling multi-turn interview simulation.

### Application Scenarios Overview

The Agent built in this phase will serve the following three core application scenarios (see [AgentScenarios.en.md](AgentScenarios.en.md) for full details):

1. **Deep Interview Agent for Personal Resumes**: Proactively guides interview conversations — identifies multiple relevant experiences, calls the `Skill_Analyzer` tool to compare JD vs. resume fit, uses multi-step reasoning to prioritize answers, and asks follow-up questions after responding (e.g., "Would you like to hear about my Flink optimization details?").
2. **Fully Automated Recruitment Assistant**: Given a JD, automatically searches the resume pool for the best candidate and drafts a recommendation letter. If the match score is below 70%, it autonomously expands the search scope and integrates `Salary_Calculator` and `Email_Generator` tools.
3. **Private Technical Debt / Documentation Scanner Agent**: Ingests code snippets, technical docs, and error logs from past years, performs cross-document horizontal comparison of technical strategy evolution, and actively investigates the reasons behind technical changes.

> **Evaluation Basis**: The RAGAS synthetic test set in Phase 4 (Task 4.1) must be designed around these three scenarios, covering Agent capabilities such as proactive questioning, tool use, multi-turn memory, and self-correction.

### Task 3.1: Design and Implement Agent State Machine

**Objective**
- Define Agent state using LangGraph
- Implement five core state nodes: Query -> Retrieval -> Reasoning -> Reflection -> Response
- Write state transition logic

**Acceptance Criteria**
- Agent successfully executes complete state transitions
- Unit tests cover all state nodes >= 85%
- Code clearly documents each state's inputs/outputs/transition conditions

**Estimated Hours**: 5h | **Priority**: P0

**Related Files**
- `src/core/agent/state.py`
- `src/core/agent/graph.py`
- `tests/unit/test_agent_state_machine.py`

---

### Task 3.2: Implement Three Core Agent Tools

**Objective**
- Implement `ExperienceComparator`: match JD vs resume, flag gaps
- Implement `TechnicalDeepDive`: deep retrieval on specific tech stack content
- Implement `InterviewStrategySelector`: adjust response based on question style (HR/technical)

**Acceptance Criteria**
- Each tool has unit tests >= 80% coverage
- Integration tests verify tools work within Agent
- Error handling is robust (null, timeout, etc.)

**Estimated Hours**: 6h | **Priority**: P0

**Related Files**
- `src/core/agent/tools.py`
- `tests/unit/test_agent_tools.py`

---

### Task 3.3: Implement Multi-Turn Conversation Memory

**Objective**
- Implement conversation history storage and retrieval (in-memory, no database)
- Implement context awareness (avoid repeating answers)
- Validate coherence over long conversations (10+ turns)

**Acceptance Criteria**
- Agent correctly references previous answers (no repetition)
- Long conversation test passes (10 turns without gaps or repetition)
- Unit tests cover memory management logic

**Estimated Hours**: 3h | **Priority**: P1

**Related Files**
- `src/core/agent/memory.py`
- `tests/unit/test_agent_memory.py`

---

### Task 3.4: Complete CLI `vedaaide chat`

**Objective**
- Wire Agent workflow into Phase 1 CLI scaffold
- Implement interactive conversation mode (streaming / non-streaming option)
- Implement conversation log saving (optional, `--save-log`)

**Acceptance Criteria**
- `vedaaide chat` completes at least 5 turns of conversation
- Streaming mode provides smooth user experience
- All Phase 1 CLI params (`--llm`, `--model`, `--top-k`, etc.) work correctly

**Estimated Hours**: 3h | **Priority**: P0

**Related Files**
- `src/cli/commands/chat.py`

---

### Task 3.5: LangFuse Local Integration (Optional, for Demo)

**Objective**
- Add LangFuse trace recording for main Agent steps
- Verify full execution chain visible in LangFuse UI

**Acceptance Criteria**
- LangFuse Dashboard (http://localhost:3000) shows Agent execution tree
- All RAG steps and tool calls have trace records
- LangFuse is an **optional dependency** — code runs normally without it

**Estimated Hours**: 3h | **Priority**: P2

**Related Files**
- `src/infrastructure/observability/tracing.py`

---

### Task 3.6: Integration Test — End-to-End Agent Workflow

**Objective**
- Run complete workflow test with deidentified sample data
- Validate Agent multi-turn conversation and tool invocation

**Acceptance Criteria**
- Successfully executes 5+ complete conversation turns
- No PII exposure detected
- Integration tests written and passing

**Estimated Hours**: 3h | **Priority**: P1

**Related Files**
- `tests/integration/test_end_to_end_workflow.py`

---

## Phase 4: Evaluation and DSPy Optimization (Week 7-8)

> Goal: Quantify RAG quality, optimize prompts with DSPy, establish continuous evaluation.

### Task 4.1: Generate Synthetic Test Set

**Objective**
- Generate 50+ interview questions using LlamaIndex TestsetGenerator
- Manually review question quality
- Save test set

**Acceptance Criteria**
- At least 50 diverse questions generated
- Questions cover multiple skill areas (architecture, coding, project experience, etc.)
- Manual review passes with quality score >= 4/5

**Estimated Hours**: 3h | **Priority**: P0

**Related Files**
- `scripts/evaluation/generate_test_set.py`
- `data/test_sets/`

---

### Task 4.2: Implement RAGAS Evaluation Script

**Objective**
- Implement Faithfulness, Relevance, Recall evaluation
- Support batch evaluation
- Generate evaluation report (JSON + visualization)

**Acceptance Criteria**
- Can fully evaluate 50 questions
- Evaluation results stored as structured JSON
- Basic visualization report generated
- Code coverage >= 80%

**Estimated Hours**: 5h | **Priority**: P0

**Related Files**
- `src/core/evaluation/ragas_evaluator.py`
- `scripts/evaluation/run_ragas.py`
- `tests/unit/test_ragas_evaluator.py`

---

### Task 4.3: DSPy Prompt Compilation Optimization

**Objective**
- Compile optimized prompts for Azure OpenAI
- Compile optimized prompts for Ollama
- Generate RAGAS before/after comparison report

**Acceptance Criteria**
- Optimized RAGAS scores >= pre-optimization scores
- Token consumption reduced (where applicable)
- A/B comparison data recorded in `data/evaluation-results/`

**Estimated Hours**: 6h | **Priority**: P1

**Related Files**
- `src/core/rag/dspy_compiler.py`
- `scripts/evaluation/optimize_prompts.py`

---

### Task 4.4: CLI Evaluation Command (`vedaaide eval`)

**Objective**
- Wire RAGAS evaluation into Phase 1 CLI scaffold
- Implement `vedaaide eval`: run RAGAS and output report
- Implement `vedaaide eval --compare <v1> <v2>`: compare two evaluation results

**Acceptance Criteria**
- `vedaaide eval` runs complete evaluation pipeline
- Outputs clear evaluation summary to terminal
- Report saved to `data/evaluation-results/`
- Phase 1 `--llm` parameter controls evaluation LLM backend

**Estimated Hours**: 3h | **Priority**: P1

**Related Files**
- `src/cli/commands/evaluate.py`

---

## Phase 5: Publishing and Documentation (Week 9-10)

> Goal: Package and publish as an installable PyPI package; complete docs and CI/CD.

### Task 5.1: Complete pyproject.toml Package Config

**Objective**
- Configure package metadata (name, version, description, classifiers)
- Confirm CLI entry points match Phase 1 definition
- Configure optional dependencies (`langfuse`, etc.)

**Acceptance Criteria**
- `poetry build` successfully generates dist/ files
- `pip install dist/*.whl` → `vedaaide --help` works
- `pip install vedaaide[langfuse]` installs LangFuse optional dependency

**Estimated Hours**: 2h | **Priority**: P0

**Related Files**
- `pyproject.toml`

---

### Task 5.2: GitHub Actions CI/CD

**Objective**
- Create test workflow: auto-run unit tests on push
- Create release workflow: auto-publish to PyPI on tag

**Acceptance Criteria**
- Unit tests run automatically before PR merge
- `git tag v1.0.0` triggers auto-publish to PyPI
- Clear error messages on CI failure

**Estimated Hours**: 3h | **Priority**: P0

**Related Files**
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`

---

### Task 5.3: Polish README (5-Minute Quick Start)

**Objective**
- User can install and run basic demo within 5 minutes
- CN/EN synchronized
- Include installation, configuration, CLI usage (with full parameter reference)

**Acceptance Criteria**
- Following README steps, all commands execute successfully
- `pip install vedaaide` + configure `.env` + `vedaaide chat` full flow works
- Chinese (README.cn.md) and English (README.md) are in sync

**Estimated Hours**: 3h | **Priority**: P0

---

### Task 5.4: Publish to PyPI

**Objective**
- Register PyPI account (if not already done)
- Configure GitHub Secrets (PyPI token)
- Publish first version (v0.1.0)

**Acceptance Criteria**
- `pip install vedaaide` installs successfully from PyPI
- `vedaaide --help` works after install
- PyPI page shows correct description and version

**Estimated Hours**: 1h | **Priority**: P0

---

## Appendix: Priority Summary

| Phase | Task | Priority | Est. Hours |
|-------|------|----------|------------|
| Phase 1 | 1.1 Deploy Qdrant | P0 | 2h |
| Phase 1 | 1.2 Environment Variables | P0 | 1h |
| Phase 1 | 1.3 Deidentification Tool | P0 | 4h |
| Phase 1 | 1.4 Public Sample Data | P0 | 3h |
| Phase 1 | 1.5 LlamaIndex Indexing Pipeline | P0 | 4h |
| Phase 1 | 1.6 Baseline RAG Validation | P0 | 3h |
| Phase 1 | 1.7 CLI Scaffold | P0 | 4h |
| Phase 2 | 2.1 Deduplication & Incremental Index | P0 | 4h |
| Phase 2 | 2.2 Hybrid Retrieval Tuning | P0 | 5h |
| Phase 2 | 2.3 Reranking | P0 | 5h |
| Phase 2 | 2.4 Anti-Hallucination | P0 | 6h |
| Phase 2 | 2.5 Contextual Compression | P1 | 4h |
| Phase 2 | 2.6 RAG Quality Integration Tests | P1 | 3h |
| Phase 3 | 3.1 Agent State Machine | P0 | 5h |
| Phase 3 | 3.2 Three Core Tools | P0 | 6h |
| Phase 3 | 3.3 Multi-Turn Memory | P1 | 3h |
| Phase 3 | 3.4 Complete CLI chat | P0 | 3h |
| Phase 3 | 3.5 LangFuse Integration | P2 | 3h |
| Phase 3 | 3.6 End-to-End Integration Tests | P1 | 3h |
| Phase 4 | 4.1 Synthetic Test Set | P0 | 3h |
| Phase 4 | 4.2 RAGAS Evaluation Script | P0 | 5h |
| Phase 4 | 4.3 DSPy Optimization | P1 | 6h |
| Phase 4 | 4.4 CLI eval Command | P1 | 3h |
| Phase 5 | 5.1 pyproject.toml Config | P0 | 2h |
| Phase 5 | 5.2 GitHub Actions CI/CD | P0 | 3h |
| Phase 5 | 5.3 Polish README | P0 | 3h |
| Phase 5 | 5.4 Publish to PyPI | P0 | 1h |
| **Total** | | | **~87 hours** |
