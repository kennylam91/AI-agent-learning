## Plan: Text-First AI Agent Roadmap (4 Weeks)

Your project is mostly text-based, so this roadmap focuses on LLM application engineering, not deep model training.
You only need enough AI/ML ecosystem knowledge to make strong architecture choices and debug behavior.

---

### What to Learn (Priority Order)

1. **Prompting and agent orchestration** — system prompts, tool calling, memory strategy, retries, fallbacks.
2. **RAG for text** — chunking, embeddings, retrieval quality, reranking, citations.
3. **Evaluation** — task-based eval sets, pass/fail rubrics, hallucination tracking, latency/cost tracking.
4. **Safety and guardrails** — input filtering, output validation, policy handling, prompt-injection defense.
5. **Minimal ML ecosystem literacy** — embeddings, tokenization, context windows, model tradeoffs.

---

### Week 1 — Python + Agent Foundations

Goal: Be productive in Python while implementing a basic text agent loop.

1. Python essentials for agent code:

- Type hints, dataclasses/pydantic models, async/await
- Common gotchas: mutable defaults, truthiness, `is None`, unpacking

1. Build a simple loop:

- Input -> system prompt -> model call -> output
- Add structured logging (request, response, latency, tokens)

1. Add tool-calling skeleton:

- Define 2 tools (e.g., calculator, local file lookup)
- Validate tool args with pydantic

**Deliverable:** CLI text agent that answers and calls at least one tool reliably.

---

### Week 2 — Text RAG Pipeline

Goal: Ground answers in your own documents.

1. Ingestion pipeline:

- Load text files/markdown
- Chunk by semantic boundaries (paragraph/header-aware)
- Store metadata (source, section, timestamp)

1. Retrieval pipeline:

- Embeddings + vector store
- Top-k retrieval with optional reranking

1. Answering pipeline:

- Prompt template with source-grounding constraints
- Return citation snippets in output

**Deliverable:** RAG-enabled agent that cites sources and avoids unsupported claims.

---

### Week 3 — Quality, Safety, and Robustness

Goal: Make the text agent production-safe.

1. Evaluation harness:

- Create 30–50 real user-style test prompts
- Define rubrics: correctness, groundedness, tone, refusal behavior

1. Safety controls:

- Prompt-injection checks on retrieved content
- Output schema validation and post-processing guardrails

1. Reliability patterns:

- Timeout/retry strategy
- Graceful fallback model
- Error classes for model/tool/retrieval failures

**Deliverable:** Repeatable eval script + safety checks with measurable pass rate.

---

### Week 4 — Optimization + Deployment Readiness

Goal: Make it fast, affordable, and maintainable.

1. Performance tuning:

- Reduce token usage in prompts
- Improve chunk size and retrieval parameters
- Cache embeddings and frequent responses

1. Model strategy:

- Compare 2–3 models on your eval set
- Choose default + fallback based on quality/latency/cost

1. Operational readiness:

- Add monitoring metrics: success rate, latency, cost per request
- Document runbook for failures and model changes

**Deliverable:** Agent service with baseline metrics and clear operating playbook.

---

### AI/ML Ecosystem: What You Can Skip (For Now)

You can postpone these unless your scope changes:

- Training models from scratch
- Advanced deep learning math/derivations
- Heavy PyTorch training loops
- Complex CV/audio pipelines

---

### Minimal AI/ML Concepts You Still Need

1. **Tokenization** and context window limits
2. **Embeddings** and vector similarity basics
3. **Retrieval precision vs recall** tradeoff
4. **Temperature/top-p** and determinism tradeoffs
5. **Hallucination modes** and mitigation patterns

---

### Suggested Stack for Text Agents (Practical Default)

- Python 3.11+
- FastAPI (if serving APIs)
- Pydantic for tool/input/output schemas
- LLM SDK of your provider
- Vector DB (start simple: Chroma/FAISS/local, then upgrade if needed)
- `pytest` + custom eval runner for regression checks

---

### Weekly Checkpoints

- **Week 1:** Agent loop + tool call works end-to-end
- **Week 2:** RAG answers include citations from your corpus
- **Week 3:** Eval suite and guardrails catch major failures
- **Week 4:** Latency/cost improved with documented model strategy

---

### Decision Rule

For a text-first agent project, use this split:

- **70%** agent engineering (prompts, tools, RAG, evaluation, safety)
- **20%** platform/software engineering (APIs, logging, monitoring, CI)
- **10%** AI/ML theory (just enough to make good decisions)
