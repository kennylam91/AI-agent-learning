#### Week 2 Execution Plan (Day-by-Day)

Goal: Ground agent answers in your own documents using a RAG pipeline.

Assume 90–120 minutes per day. If you have less time, do the Must-Do items first.

---

**Day 8 — Document ingestion basics**

Must-Do:

- Load plain text and markdown files from a local folder
- Parse each file into raw string content with metadata (filepath, filename, modified date)
- Write a pydantic model for a `Document` (content, source, metadata)

Output:

- `ingest.py` that loads a folder and returns a list of `Document` objects
- At least 5 sample docs ready to use for the rest of the week

---

**Day 9 — Chunking strategy**

Must-Do:

- Split documents into smaller chunks (target 200–400 tokens per chunk)
- Use header- and paragraph-aware splitting, not naive character splits
- Preserve source metadata on every chunk (source file, section heading, chunk index)

Output:

- `chunker.py` with a `chunk_document(doc) -> list[Chunk]` function
- Pydantic `Chunk` model with `text`, `source`, `chunk_index`, `metadata`
- Quick sanity check: print chunk count and average token length per doc

---

**Day 10 — Embeddings + vector store**

Must-Do:

- Choose and install an embedding model (e.g., `sentence-transformers` or provider SDK embedding endpoint)
- Embed all chunks and store them in a local vector store (start with Chroma or FAISS)
- Persist the index to disk so you do not re-embed on every run

Output:

- `embedder.py` that embeds a list of chunks and upserts into the vector store
- Index saved to a local folder (e.g., `vector_store/`)
- Verify you can reopen the index without re-embedding

---

**Day 11 — Retrieval pipeline**

Must-Do:

- Implement `retrieve(query: str, top_k: int) -> list[Chunk]` using vector similarity search
- Log retrieval scores alongside chunk text to spot low-confidence results
- Add a minimum score threshold to filter out irrelevant chunks

Output:

- `retriever.py` with `retrieve()` function
- Test with 5 queries, inspect top-3 results per query manually
- At least one query where the threshold correctly filters a weak match

---

**Day 12 — RAG answering pipeline**

Must-Do:

- Build a prompt template that injects retrieved chunks as context
- Instruct the model to only answer from provided context; if unsupported, say so explicitly
- Include citations (source filename + chunk index) in the model's response format

Output:

- `rag_agent.py` with a `ask(query) -> AnswerWithCitations` flow
- Pydantic `AnswerWithCitations` model: `answer`, `citations: list[str]`
- Agent refuses to speculate when no relevant context is found

---

**Day 13 — Integration + end-to-end test**

Must-Do:

- Wire ingest → chunk → embed → retrieve → answer into one CLI command
- Add structured logs for: query, chunks retrieved, scores, latency, token usage
- Handle edge cases: empty query, no chunks above threshold, missing vector store

Output:

- Single `main.py` (or updated entry point) that runs full RAG flow from the terminal
- Logs written to `logs.jsonl` with retrieval + generation details
- Graceful error messages for all three edge cases above

---

**Day 14 — RAG evaluation + recap**

Must-Do:

- Create 15 RAG-specific test prompts across 3 categories:
  - **Grounded** (answer clearly in docs)
  - **Partially grounded** (only some info in docs)
  - **Out-of-scope** (answer not in docs at all)
- Score each run: correct answer, correct citation, correct refusal
- Record top 5 failures (wrong retrieval, hallucinated citation, ignored context) and likely fixes

Output:

- `eval/week2_prompts.json` or `.md` with prompts, expected behavior, and scores
- Week 2 scorecard with pass/fail counts per category
- Prioritized list of retrieval and prompting fixes for Week 3

---

#### Week 2 Done Criteria

- Documents load and chunk cleanly with metadata preserved end-to-end
- Vector store persists and retrieves correctly across runs
- Agent cites sources in responses and refuses unsupported claims
- Structured logs capture retrieval scores, latency, and token usage
- At least 15 RAG test prompts executed with scored results

---

#### Week 2 Stretch (Only if Ahead)

- Add reranking step (cross-encoder or LLM-based) after top-k retrieval
- Support hybrid search: BM25 keyword + vector similarity combined
- Add a simple web UI (Streamlit or Gradio) to browse answers and citations
- Track embedding drift: alert if new docs fall outside existing embedding distribution

---

#### Packages to Install This Week

```
pip install chromadb sentence-transformers tiktoken
```

Or if using provider embeddings:

```
pip install chromadb tiktoken
```

---

#### Concepts to Understand Before Day 10

- **Chunking strategy tradeoffs**: large chunks = more context but noisier retrieval; small chunks = precise but may lose context
- **Cosine similarity vs dot product**: know which your vector store uses by default
- **Retrieval precision vs recall**: a low threshold finds more but includes noise; tune carefully
- **Context window budget**: total tokens for system prompt + retrieved chunks + query must fit within model limit
