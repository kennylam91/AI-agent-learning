#### Week 1 Execution Plan (Day-by-Day)

Assume 90–120 minutes per day. If you have less time, do the Must-Do items first.

**Day 1 — Python setup + clean baseline**

Must-Do:

- Create project venv and install core packages (LLM SDK, pydantic, python-dotenv)
- Confirm you can run a single Python script end-to-end
- Review Python gotchas relevant to agent code (`is None`, mutable defaults, unpacking)

Output:

- One runnable script with a `main()` entrypoint
- Minimal `README` note with run command and env vars

**Day 2 — First model call loop**

Must-Do:

- Build `input -> prompt -> model -> output` loop in CLI
- Add system prompt for role, tone, and boundaries
- Handle API errors cleanly (timeout/network/auth)

Output:

- Agent answers text prompts in terminal
- Basic error messages instead of crashes

**Day 3 — Structured models + logging**

Must-Do:

- Add pydantic models for request/response payloads
- Add structured logs: timestamp, latency, model, token usage (if available)
- Capture failed calls separately from successful calls

Output:

- Predictable input/output schema
- Logs that help debug bad responses quickly

**Day 4 — Tool calling (single tool)**

Must-Do:

- Implement one tool (start with deterministic tool like calculator or text search)
- Validate tool arguments with pydantic
- Return tool result back into the agent response loop

Output:

- Agent can decide to call one tool and continue response generation

**Day 5 — Tool calling (second tool) + routing rules**

Must-Do:

- Add second tool (e.g., local markdown lookup)
- Add clear tool usage policy in system prompt
- Prevent tool overuse with simple constraints (max calls per turn)

Output:

- Agent can select between two tools appropriately
- Fewer unnecessary tool calls

**Day 6 — Guardrails + reliability pass**

Must-Do:

- Add input checks (empty/very long prompt handling)
- Add output checks (fallback if response is empty or malformed)
- Add retry strategy with cap (e.g., 1–2 retries)

Output:

- Agent fails gracefully and recovers from transient issues

**Day 7 — Mini evaluation + recap**

Must-Do:

- Create 15 test prompts (easy, ambiguous, adversarial, tool-needed)
- Score each run on correctness, clarity, and tool-use quality
- Record top 5 failures and likely fixes

Output:

- Simple Week 1 scorecard and next-week priorities

#### Week 1 Done Criteria

- CLI agent runs consistently with one command
- Agent can answer directly and call at least one tool correctly
- Logs show latency + failure reasons
- At least 15 test prompts executed with notes

#### Week 1 Stretch (Only if Ahead)

- Add response streaming in terminal
- Add conversation memory for last 3 turns
- Add one prompt-injection check before tool execution

---
