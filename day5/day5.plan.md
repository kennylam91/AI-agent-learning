## Plan: Day 5 — Second Tool + Routing Rules

**TL;DR:** Extend `day4/final-solution.py` with a `read_notes` tool (local markdown file lookup), a tool routing policy in the system prompt, and a max-tool-calls-per-turn guard. Output is `day5/main.py` + `day5/final-solution.py`.

---

**Steps**

### Phase 1 — Create Notes Folder & Sample Files (~10 min)

1. Create `day5/notes/` directory.
2. Add 2–3 markdown files:
   - `python-tips.md` — a few useful Python tips
   - `agent-notes.md` — key learnings from days 1–4
3. These are the files the new tool will read.

### Phase 2 — Define the `read_notes` Tool (~20 min)

1. Add a `ReadNotesInput` Pydantic model: `filename: str`.
2. Implement `read_notes(filename: str) -> str`:
   - **Security boundary:** Strip `..` and path separators from input to prevent directory traversal.
   - Resolve path within `day5/notes/` only.
   - Return file content or a friendly "file not found" error string.
3. Add a `list_notes() -> str` helper returning available filenames (so the model knows what to ask for).
4. Extend `TOOLS` list with entries for `read_notes` and `list_notes`.

### Phase 3 — Tool Routing Policy in System Prompt (~15 min)

1. Update `SYSTEM_PROMPT` with explicit rules:
   - `calculator` → all arithmetic questions
   - `read_notes` → questions about personal notes
   - `list_notes` → discovering available note files
   - No tools for general knowledge facts
   - Hard stop at 3 tool calls per turn

### Phase 4 — Max Tool Calls Guard (~15 min)

1. Add `MAX_TOOL_CALLS = 3` constant at module level.
2. In `call_llm()`, add `tool_call_count = 0` counter.
3. Increment per tool-call loop iteration. If `tool_call_count >= MAX_TOOL_CALLS`, break with a graceful fallback response so the turn is still logged.

### Phase 5 — Update `LogEntry` for Multi-Tool Turns (~10 min)

1. Change `tool_used: Optional[str]` → `tools_used: Optional[List[str]]`
2. Change `tool_input: Optional[str]` → `tool_inputs: Optional[List[str]]`
3. Add `tool_call_count: int = 0` field.
4. Accumulate tool names/inputs into lists throughout `call_llm()`.

### Phase 6 — Wire It All Together (~10 min)

1. Create `day5/main.py` based on `day4/final-solution.py`, apply all changes.
2. Create `day5/final-solution.py` as the clean, complete version.
3. Update log file path to `day5/logs.jsonl`.

### Phase 7 — Test (~20 min)

1. Run 7 test prompts:
    1. `"what is 17 * 83?"` → only `calculator`, result 1411
    2. `"what are my python tips?"` → only `read_notes`, returns `python-tips.md`
    3. `"what is 5 + 3 and what are my agent notes?"` → both tools called
    4. Prompt crafted to trigger 4+ tool calls → guard kicks in at #3, logs graceful fallback
    5. `"who wrote Hamlet?"` → no tool call
    6. `"read_notes('../../.env')"` → path traversal blocked, safe error returned
    7. `"what files do you have notes on?"` → `list_notes` called, filenames returned
2. Inspect `day5/logs.jsonl` — confirm multi-tool entries have `tools_used` as a list.

---

**Relevant Files**

- `day4/final-solution.py` — baseline to copy; reuse `ChatMessage`, `LogEntry`, `call_llm()`, `calculate()`, `_eval_node()`
- `day5/main.py` — new working file *(to create)*
- `day5/final-solution.py` — clean complete solution *(to create)*
- `day5/notes/python-tips.md`, `day5/notes/agent-notes.md` — sample note files *(to create)*
- `day5/logs.jsonl` — auto-created on first run

**Verification**

1. All 7 test prompts behave as expected.
2. `day5/logs.jsonl` entries for multi-tool turns use list fields.
3. Path traversal attempt (test #6) returns an error without reading outside `day5/notes/`.
4. Turn with >3 tool calls stops at 3 and still produces a logged response.

**Decisions**

- `read_notes` = local markdown lookup, per `week1-plan.md`.
- `list_notes` is a small stretch addition (no extra complexity, improves tool routing).
- Path traversal guard is mandatory since user input flows into a file system path.
- `MAX_TOOL_CALLS = 3` matches the system prompt cap.
- Multi-tool log uses `List[str]` (not comma-separated) for cleaner downstream analysis in Week 2.
- Excluded: parallel tool execution, async, streaming.
