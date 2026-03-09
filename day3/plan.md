## Day 3: Structured Models + Logging

### Goal

Add Pydantic models for request/response, fix system prompt handling, and implement structured logging for each model call.

#### Tasks

- **Review Day 2 Agent Loop (5 min)**
  - Recap CLI, prompt, and model call flow

- **Refactor for System Prompt (10 min)**
  - Move system prompt to a `role: system` message in the API payload

- **Add Pydantic Models (15 min)**
  - Define `ChatMessage` (role/content) and `LogEntry` (timestamp, model, tokens, latency, user input, response)

- **Implement Error Handling (10 min)**
  - Add try/except for network and API errors, print user-friendly messages

- **Add Structured Logging (15 min)**
  - Log each call as a JSON line in `logs.jsonl` with all fields

- **Test and Validate (10 min)**
  - Run several prompts, check `logs.jsonl` for correct entries

#### Done-for-today Checklist

- [ ] System prompt is a separate message
- [ ] Pydantic models in use
- [ ] Error handling covers network and API errors
- [ ] Each call logs to `logs.jsonl`
- [ ] Manual test: logs are correct

#### Stretch Goals

- Add multi-turn chat history
- Pretty-print logs to console
