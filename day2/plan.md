## Day 2: First Model Call Loop

### Goal
Build a minimal agent loop: input → prompt → model → output, running in the terminal. Add a system prompt for role/tone, and handle API errors gracefully.

---

### 1. Review Day 1 Baseline (5 min)
- Confirm venv and dependencies are working.
- Ensure main.py runs and .env is loaded.

### 2. Design the Model Call Loop (10 min)
- Sketch the flow: user input → build prompt → call model → print response.
- Decide on a system prompt (role, tone, boundaries).
- Choose a model provider (OpenAI, Azure, etc.) and check API key in .env.

### 3. Implement CLI Input/Output (10 min)
- Accept user input in a loop (e.g., input("You: ")).
- Print agent/model response to terminal.
- Add an exit command (e.g., 'exit' or 'quit').

### 4. Add System Prompt (10 min)
- Define a system prompt string (e.g., "You are a helpful assistant...").
- Prepend system prompt to user input when building the model request.

### 5. Make the Model API Call (20 min)
- Use the provider SDK to send the prompt and get a response.
- Parse and print the model's reply.
- Handle API errors: network, timeout, auth (try/except, print user-friendly error).

### 6. Test and Refine (15 min)
- Try several user prompts, including edge cases (empty, long, nonsense).
- Confirm errors are handled without crashing.
- Adjust system prompt for tone/boundaries as needed.

### 7. Done-for-today Checklist
- [ ] CLI loop: input → model → output
- [ ] System prompt is included
- [ ] Handles API errors gracefully
- [ ] Agent answers text prompts in terminal
- [ ] No crashes on bad input or API errors

---

**Stretch:**
- Add basic logging (print request/response pairs).
- Support multi-turn (keep chat history in a list).
