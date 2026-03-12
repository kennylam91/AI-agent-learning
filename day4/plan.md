# Day 4 — Tool Calling (Single Tool)

## TL;DR

Extend the Day 3 agent with a single calculator tool using the OpenRouter / OpenAI function-calling protocol. The model can request the `calculator` tool; the agent executes the calculation safely and feeds the result back into the conversation before producing a final answer.

## Goal

Agent can decide to call one tool (calculator) and feed the validated result back into the conversation loop.

## Steps

### Phase 1 — Define the Tool (~15 min)

- Add a `CalculatorInput` Pydantic model with: `expression: str`.
- Implement a safe `calculate(expression: str) -> str` using `ast` and a manual node evaluator (no raw `eval`).
- Define `TOOLS` as an array in the OpenAI function schema format (name, description, parameters JSON schema).

### Phase 2 — Wire Tools into the API Request (~10 min)

- Ensure request payload includes `tools` when calling the API.
- Use `model_dump(exclude_none=True)` to avoid sending null fields the API may reject.

### Phase 3 — Handle Tool Call Response (~20 min)

- After receiving the model response, check `finish_reason` or the assistant message for `tool_calls`.
- If a tool call is requested:
  - Extract `function.arguments` JSON, validate with `CalculatorInput`.
  - Run `calculate()` and obtain a result string (or a safe error message).
  - Append the assistant's tool-call message (role: `assistant`, content: `null`, `tool_calls: [...]`) to history.
  - Append a `tool` role message containing the result to history.
  - Re-send the updated conversation to get the final assistant reply.
- Otherwise, treat as a normal response and log it.

### Phase 4 — Logging (~10 min)

- Extend `LogEntry` with `tool_used: Optional[str]` and `tool_input: Optional[str]`.
- When a tool is used, populate these fields and include them in `logs.jsonl`.

### Phase 5 — System Prompt (~5 min)

- Update the system prompt to name the calculator tool and instruct the model to use it for arithmetic queries.

### Phase 6 — Test (~15 min)

- Test cases:
  1. "what is 17 * 83?" → should call `calculator`, log `tool_used: calculator`, answer `1411`.
  2. "who wrote Hamlet?" → no tool call, direct answer.
  3. "2 to the power of 10" → tool invoked, returns `1024`.
  4. Bad expression (e.g., `1/0`) → tool returns error string; agent relays it gracefully.
- Verify `day4/logs.jsonl` entries contain any tool usage fields when used.

## Decisions / Notes

- Use `ast.parse` with a whitelist of nodes to evaluate math expressions safely.
- Keep single tool for Day 4; add a second tool and routing rules on Day 5.
- Use `exclude_none=True` when serializing Pydantic models to avoid `null` fields in payloads.

## Files to touch

- `day4/main.py` — new starter copied from `day3/main.py` + TODOs and safe calculator helper
- `day4/plan.md` — this file

## Done Criteria

- Agent can call a calculator tool and return final answer in a single turn.
- Logs include `tool_used` and `tool_input` when applicable.
- System prompt mentions tools and usage rules.
