---
name: evaluation
description: RAG evaluation framework for VedaAide using RAGAS metrics, synthetic test set generation, user feedback mechanisms, and DSPy optimization for prompt compilation
applyTo: "src/evaluation/**,src/core/rag/**"
keywords:
  - evaluation
  - ragas
  - metrics
  - feedback
  - optimization
  - faithfulness
  - relevance
  - recall
  - dspy
  - 评估
  - 反馈
  - RAGAS
  - 指标
  - 优化
  - 忠实度
  - 相关性
  - 质量评估
whenToUse: |
  When implementing:
  - RAGAS evaluation metrics (Faithfulness, Relevance, Recall)
  - Synthetic test set generation
  - DSPy prompt optimization
  - User feedback collection mechanisms
  - Evaluation reports and analysis
---

# VedaAide RAG Evaluation Strategy

## Evaluation Framework Overview

```
Training data
  ↓
Synthetic test set generation (TestsetGenerator)
  ↓
Agent answer generation
  ↓
RAGAS evaluation (Faithfulness, Relevance, Recall)
  ↓
DSPy compilation optimization (improve Prompt)
  ↓
User feedback collection
  ↓
Iterative improvement
```

## Evaluation Metrics

### 1. Faithfulness

**Definition**: Whether the answer is grounded in the retrieved context, without hallucinations

**Calculation**:
```
Given an answer and context, ask the LLM:
"Can every fact in this answer be found in the context?"
```

**Example**:
```
Context: "John has 5 years of Kubernetes experience"
Answer: "John has 5 years of Kubernetes experience and is proficient in container orchestration"
Faithfulness: 0.8  # "container orchestration" may not be in the original text
```

**Improvement methods**:
- Improve retrieval (ensure the correct documents are retrieved)
- Emphasize "based on the provided information" in the Prompt
- Use a more constrained model (gpt-4o vs gpt-3.5)

### 2. Relevance

**Definition**: Whether the retrieved context is relevant to the query

**Calculation**:
```
Given a query and context, ask the LLM:
"Is this context relevant to the query?"
```

**Example**:
```
Query: "Do you have database experience?"
Retrieved: "I have managed Kubernetes clusters"
Relevance: 0.3  # not relevant
```

**Improvement methods**:
- Optimize hybrid search weights (BM25 vs Vector)
- Improve data quality and indexing
- Use a better Embedding model

### 3. Recall

**Definition**: Whether all relevant documents that should be retrieved are retrieved

**Calculation**:
```
Compare retrieved results against the gold-standard document set
Recall = number of relevant documents retrieved / total number of relevant documents
```

**Example**:
```
Query: "Your cloud project experience"
Gold standard: [AWS project, Azure project, GCP project]
Retrieved: [AWS project, Azure project]
Recall: 0.67  # GCP was missed
```

**Improvement methods**:
- Increase `top_k` retrieval count
- Lower similarity threshold
- Improve data chunking strategy

## Generating Evaluation Test Sets

### Using LlamaIndex TestsetGenerator

```python
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.evaluation.dataset_generation import generate_qa_pairs

# Generate QA pairs from documents
documents = load_documents("data/resumes/")

# Generate 50 synthetic questions
qa_dataset = generate_qa_pairs(
    documents=documents,
    num_questions_per_chunk=3,
    language="en"
)

# Save dataset
qa_dataset.save("data/evaluation/qa_dataset_v1.json")

# View generated questions
for qa in qa_dataset.qa_pairs[:5]:
    print(f"Q: {qa.question}")
    print(f"A: {qa.answer}")
```

### Manually Curated Test Set

```python
# Critical scenario test cases
critical_test_cases = [
    {
        "query": "What is your most significant achievement?",
        "expected_context": "led project X, achieved Y results",
        "category": "achievement"
    },
    {
        "query": "Describe a technical challenge you faced",
        "expected_context": "debugging, performance optimization",
        "category": "problem_solving"
    },
    {
        "query": "How do you stay updated with new technologies?",
        "expected_context": "learning, conferences, side projects",
        "category": "growth_mindset"
    }
]

# Save in standard format
import json
with open("data/evaluation/critical_cases.json", "w") as f:
    json.dump(critical_test_cases, f, indent=2)
```

## Running RAGAS Evaluation

### Basic Evaluation

```python
from ragas import evaluate
from ragas.metrics import Faithfulness, Relevance, Recall

# Prepare data
predictions = [agent.query(q) for q in queries]
ground_truth_contexts = [retrieve(q) for q in queries]

# Run evaluation
results = evaluate(
    predictions=predictions,
    ground_truths=ground_truth_contexts,
    metrics=[Faithfulness(), Relevance(), Recall()]
)

# View results
print(f"Faithfulness: {results['faithfulness']:.3f}")
print(f"Relevance: {results['relevance']:.3f}")
print(f"Recall: {results['recall']:.3f}")

# Average score
avg_score = (
    results['faithfulness'] +
    results['relevance'] +
    results['recall']
) / 3
print(f"Average score: {avg_score:.3f}")
```

### Detailed Report

```python
# Get per-sample scores
for idx, (pred, gt) in enumerate(zip(predictions, ground_truth_contexts)):
    sample_results = evaluate_sample(pred, gt)
    print(f"Sample {idx}:")
    print(f"  Query: {queries[idx]}")
    print(f"  Prediction: {pred[:100]}...")
    print(f"  Faithfulness: {sample_results['faithfulness']:.3f}")
    print(f"  Relevance: {sample_results['relevance']:.3f}")
    print(f"  Recall: {sample_results['recall']:.3f}")
```

### Saving Evaluation Results

```python
import json
from datetime import datetime

evaluation_report = {
    "timestamp": datetime.now().isoformat(),
    "model": "gpt-4o",
    "num_samples": len(predictions),
    "metrics": {
        "faithfulness": results['faithfulness'],
        "relevance": results['relevance'],
        "recall": results['recall'],
        "average": avg_score
    },
    "per_sample_details": [
        {
            "query": q,
            "prediction": pred,
            "scores": evaluate_sample(pred, gt)
        }
        for q, pred, gt in zip(queries, predictions, ground_truth_contexts)
    ]
}

# Save
filename = f"data/evaluation/ragas_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w") as f:
    json.dump(evaluation_report, f, indent=2, ensure_ascii=False)

print(f"Report saved to {filename}")
```

## DSPy Compilation Optimization

### Compiling Optimal Prompt

```python
import dspy
from dspy.evaluation import evaluate
from src.core.rag.dspy_compiler import compile_prompt

# Define the task
class RAGTask(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(
            "context, question -> answer"
        )

    def forward(self, context, question):
        return self.generate_answer.forward(
            context=context,
            question=question
        )

# Define the evaluation metric
def metric_func(gold, pred, trace=None):
    """Evaluation function: whether the answer is correct."""
    # RAGAS metrics can be used here
    return faithfulness_score > 0.8

# Compile optimization
compiled_module = compile_prompt(
    task=RAGTask(),
    train_set=training_examples,  # 100 examples
    metric=metric_func,
    num_trials=50,  # try 50 times
    max_bootstrapped_demos=3,  # max 3 demos
    max_labeled_demos=16
)

# Use the compiled version
for test_query in test_queries:
    result = compiled_module.forward(
        context=retrieve(test_query),
        question=test_query
    )
    print(result.answer)
```

### Comparing Compilation Results

```python
# Original Prompt
original_results = evaluate(
    predictions=[original_agent.query(q) for q in test_queries],
    ground_truths=ground_truth_contexts,
    metrics=[Faithfulness(), Relevance()]
)

# Compiled optimized Prompt
compiled_results = evaluate(
    predictions=[compiled_agent.query(q) for q in test_queries],
    ground_truths=ground_truth_contexts,
    metrics=[Faithfulness(), Relevance()]
)

# Comparison
print(f"Original Faithfulness: {original_results['faithfulness']:.3f}")
print(f"Compiled Faithfulness: {compiled_results['faithfulness']:.3f}")
print(f"Improvement: {(compiled_results['faithfulness'] - original_results['faithfulness']) * 100:.1f}%")
```

## User Feedback Mechanism

### Collecting Feedback

(继续补充用户反馈部分...)
