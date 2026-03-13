import ast
import json
import operator
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import dotenv
import requests
from pathlib import Path
from pydantic import BaseModel
from os import walk

NOTES_DIR = Path(__file__).parent / "notes"
MAX_TOOL_CALLS = 3

# ─────────────────────────── Pydantic Models ───────────────────────────


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: Optional[List[Dict[str, Any]]] = None


class LogEntry(BaseModel):
    timestamp: datetime
    model: str
    tokens: int
    latency: int
    user_input: str
    response: str
    tool_used: Optional[List[str]] = None
    tool_input: Optional[List[str]] = None


class CalculatorInput(BaseModel):
    expression: str


class ReadNotesInput(BaseModel):
    filename: str


# ─────────────────────────── Tool Definitions ───────────────────────────

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a mathematical expression. "
                "Supports +, -, *, /, ** (power), // (floor div), % (mod), "
                "and unary minus. Use this tool for ALL arithmetic questions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "A valid math expression, e.g. '17 * 83', '2 ** 10', "
                            "'100 / 4'."
                        ),
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": ("Use this tool to list all the notes."),
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_notes",
            "description": "Use this tool to read the content of a specific note.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": ("Name of the node to be read the content."),
                    }
                },
                "required": ["filename"],
            },
        },
    },
]

# ─────────────────────────── Safe Calculator ───────────────────────────

_OPERATORS: Dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}


def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate a whitelisted AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand)
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Safely evaluate a math expression string and return the result as a string."""
    try:
        validated = CalculatorInput(expression=expression)
        tree = ast.parse(validated.expression, mode="eval")
        result = _eval_node(tree)
        # Return integer string when the result is a whole number
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as exc:
        return f"Error: {exc}"


# ─────────────────────────── Read notes ───────────────────────────


def read_notes(filename: str) -> str:
    split_list = str.split(filename, "/")
    sanitized_filename = split_list[-1]
    complete_filename = (
        sanitized_filename
        if sanitized_filename.endswith(".md")
        else sanitized_filename + ".md"
    )
    path = NOTES_DIR / complete_filename
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "file not found"


def list_notes() -> str:
    notes = []
    for _, _, filenames in walk(NOTES_DIR):
        for filename in filenames:
            if filename.endswith(".md"):
                notes.append(filename)
    return ", ".join(notes)


# ─────────────────────────── LLM Loop ───────────────────────────

MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

SYSTEM_PROMPT = (
    "You are a helpful assistant named Lora. Answer clearly and concisely.\n"
    "You have access to a 'calculator' tool for arithmetic, 'list_notes' and 'read_notes' for working with notes.\n"
    "You MUST use the calculator tool whenever the user asks a math or arithmetic "
    "question instead of computing it yourself.\n"
    "You MUST use the list_notes and read_notes tools whenever the users asks question regarding notes.\n"
    "For questions which is not related to math or notes, answer directly. \n"
    "If the error 'Max tool calls 'happens, answer that you cannot proceed the requested action."
    "If you don't know something, say so."
)


def call_llm(
    api_key: str,
    chat_histories: List[ChatMessage],
    log_file,
    user_input: str,
    call_state: dict,
) -> dict:
    """
    Send the current conversation to the LLM and handle the response.
    Loops internally to handle tool-call → result → final-answer cycles.
    Logs the final answer (with any tool metadata) once per user turn.
    """
    tool_used: Optional[str] = None
    tool_input: Optional[str] = None
    total_latency: float = 0.0
    total_tokens: int = 0

    while True:
        request_payload = ChatRequest(
            model=MODEL,
            messages=chat_histories,
            tools=TOOLS,
        )
        # exclude_none=True prevents sending null fields the API may reject
        payload_json = json.dumps(request_payload.model_dump(exclude_none=True))

        start = time.time()
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            data=payload_json,
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
            },
        )
        if not response.ok:
            try:
                error_body = response.json()
            except Exception:
                error_body = response.text
            raise requests.HTTPError(
                f"{response.status_code} {response.reason} — API error: {error_body}",
                response=response,
            )
        latency_ms = (time.time() - start) * 1000
        total_latency += latency_ms

        response_data = response.json()
        total_tokens = response_data.get("usage", {}).get("total_tokens", total_tokens)
        choice = response_data["choices"][0]
        finish_reason = choice.get("finish_reason")
        assistant_message = choice["message"]

        # ── Tool call branch ──
        if finish_reason == "tool_calls":
            tool_calls: List[Dict[str, Any]] = assistant_message.get("tool_calls", [])

            # Append the assistant's tool-call message to history (content may be null)
            chat_histories.append(
                ChatMessage(
                    role="assistant",
                    content=assistant_message.get("content"),
                    tool_calls=tool_calls,
                )
            )

            # Execute each requested tool and feed results back
            tool_used: list = []
            tool_input: list = []
            for tc in tool_calls:
                fn = tc["function"]
                fn_name: str = fn["name"]
                fn_args_raw: str = fn["arguments"]

                if call_state.get("tool_call_count") >= MAX_TOOL_CALLS:
                    result = "Error: Max tool calls."
                    chat_histories.append(
                        ChatMessage(
                            role="tool",
                            tool_call_id=tc["id"],
                            content=result,
                        )
                    )
                    continue

                if (
                    fn_name == "calculator"
                    or fn_name == "list_notes"
                    or fn_name == "read_notes"
                ):
                    try:
                        call_state["tool_call_count"] += 1
                        arg_json = json.loads(fn_args_raw)
                        if fn_name == "calculator":
                            expression = CalculatorInput(**arg_json).expression
                            result = calculate(expression)
                        elif fn_name == "read_notes":
                            filename = ReadNotesInput(**arg_json).filename
                            result = read_notes(filename)
                        else:
                            result = list_notes()

                    except Exception as exc:
                        result = f"Error: could not parse arguments — {exc}"

                    tool_used.append(fn_name)
                    tool_input.append(fn_args_raw)
                else:
                    result = f"Error: unknown tool '{fn_name}'"

                chat_histories.append(
                    ChatMessage(
                        role="tool",
                        tool_call_id=tc["id"],
                        content=result,
                    )
                )

            # Loop back to get the final answer after tool execution
            continue

        # ── Normal text response ──
        response_content: str = assistant_message.get("content") or ""
        print("Lora:", response_content)
        chat_histories.append(ChatMessage(role="assistant", content=response_content))

        # Write a single log entry per user turn (includes tool metadata if used)
        log_entry = LogEntry(
            timestamp=datetime.now(),
            model=MODEL,
            tokens=total_tokens,
            latency=int(total_latency),
            user_input=user_input,
            response=response_content,
            tool_used=tool_used,
            tool_input=tool_input,
        )
        log_file.write(log_entry.model_dump_json(exclude_none=True) + "\n")
        log_file.flush()
        break


# ─────────────────────────── Main ───────────────────────────


def main() -> None:
    api_key = dotenv.dotenv_values().get("OPEN_ROUTER_API_KEY")
    if api_key is None:
        print("api_key is missing")
        return

    print("Hi, I'm Lora, your AI assistant. What can I help you with today?")
    print("(type 'exit' or 'quit' to stop)\n")

    log_file = open("day5/logs.jsonl", "a", encoding="utf-8")
    chat_histories: List[ChatMessage] = [
        ChatMessage(role="system", content=SYSTEM_PROMPT)
    ]

    call_state = {"tool_call_count": 0}
    while True:
        user_input = input("you: ")

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            log_file.close()
            return

        chat_histories.append(ChatMessage(role="user", content=user_input))

        try:
            call_llm(api_key, chat_histories, log_file, user_input, call_state)
        except Exception as exc:
            print(f"An error occurred: {exc}")


if __name__ == "__main__":
    main()
    # print(list_notes())
    # print(read_notes("python-tips"))
