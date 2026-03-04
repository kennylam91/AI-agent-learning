## Day 1 Start (90–120 min)

* Follow your Day 1 scope in week1-plan.md: setup, run one script, review Python gotchas.
* In terminal, run:

``` python
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install pydantic python-dotenv openai (swap openai for your provider SDK if different)
```

### Build a tiny baseline (30 min)

* Create main.py with a main() entrypoint that loads .env, accepts one input, and prints a response placeholder.
* Add .env with API_KEY=... and verify script runs: python main.py.
* Add a 6–10 line README.md with run steps + required env vars.

### Python gotchas pass (20–30 min)

Quick drills: is None, mutable defaults, truthiness, unpacking, and basic type hints.
Write 3 tiny examples in main.py or a scratch file and run them.

### Done-for-today checklist

* venv works
* one script runs end-to-end
* README exists with exact run command
* you can explain the 4 gotchas above in your own words
