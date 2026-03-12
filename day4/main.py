import requests
import dotenv
import json
import time
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime
import ast
import operator


class ChatToolFunction(BaseModel):
    name: str
    description: str


class ChatTool(BaseModel):
    type: str
    function: ChatToolFunction


class ChatMessage(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: List[ChatTool]


class LogEntry(BaseModel):
    timestamp: datetime
    model: str
    tokens: int
    latency: int
    user_input: str
    response: str


class CalculatorInput(BaseModel):
    expression: str


def main():
    api_key = dotenv.dotenv_values().get("OPEN_ROUTER_API_KEY")

    if api_key is None:
        print("api_key is missing")
        return

    print("Hi, I'm Lora, your AI assistance. What can I help you today?")
    user_input = ""
    log_file = open("day4/logs.jsonl", "a", encoding="utf-8")
    system_chat = ChatMessage(
        role="system",
        content="""You are a helpful assistant. Answer clearly and concisely. 
            If you don\'t know, say no. Try to use the available tools if applicable. 
            If using tool, answer in JSON format, like : {"tool": "example_tool", "arguments": {"arg1": "value1"}}""",
    )
    chat_histories = [system_chat]
    while True:
        user_input = input("you: ")

        if user_input == "exit" or user_input == "quit":
            log_file.close()
            return

        user_chat_message = ChatMessage(role="user", content=user_input)
        chat_histories.append(user_chat_message)

        try:
            chatRequest = ChatRequest(
                model="stepfun/step-3.5-flash:free",
                messages=chat_histories,
                tools=[
                    ChatTool(
                        type="function",
                        function=ChatToolFunction(
                            name="calculate",
                            description="Calculate expression like add, sub, mul",
                        ),
                    )
                ],
            )

            call_llm(api_key, chat_histories, chatRequest)
            # <function=calculate>\n{"expression": "2 * 8"}\n</function>
            # if (str.startswith("<function=calculate>")):

            # log_entry = LogEntry(
            #     timestamp=datetime.now(),
            #     model=chatRequest.model,
            #     tokens=response_data["usage"]["total_tokens"],
            #     latency=int(latency_ms),
            #     user_input=user_input,
            #     response=response_content,
            # )
            # log_file.write(log_entry.model_dump_json() + "\n")
            # log_file.flush()
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


def call_llm(api_key, chat_histories, chatRequest):
    start_time = time.time()
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=chatRequest.model_dump_json(),
        headers={"Authorization": "Bearer " + api_key},
    )

    response.raise_for_status()
    latency_ms = (time.time() - start_time) * 1000
    response_data = response.json()
    choice = response_data["choices"][0]
    if choice["finish_reason"] == "tool_calls":
        last_call = choice["message"]["tool_calls"][-1]
        function = last_call["function"]
        if function["name"] == "calculate":
            arguments = function["arguments"]
            arg_json = json.loads(arguments)
            expression = arg_json["expression"]
            tool_result = calculate(expression)

            chat_histories.append(ChatMessage(role="tool", content=tool_result))
            call_llm(api_key, chat_histories, chatRequest)
    else:
        # Handle normal assistant responses and tool-call JSON payloads.
        response_content = choice["message"].get("content")
        if response_content is None:
            print("Lora: <no content>")
            return

        # Try to parse a JSON tool-invocation first; if it's plain text, print it.
        try:
            tool_call = json.loads(response_content)
        except json.JSONDecodeError:
            # Plain text answer from the assistant — print and append to history.
            print("Lora:", response_content)
            chat_histories.append(
                ChatMessage(role="assistant", content=response_content)
            )
            return

        # If parsed JSON looks like a tool call for the calculator, run it.
        if isinstance(tool_call, dict) and tool_call.get("tool") == "calculate":
            # Preserve the assistant message (the JSON payload) in history
            chat_histories.append(
                ChatMessage(role="assistant", content=response_content)
            )
            # Extract the expression safely
            arguments = tool_call.get("arguments") or {}
            expression = (
                arguments.get("expression") if isinstance(arguments, dict) else None
            )
            if expression:
                tool_result = calculate(expression)
                chat_histories.append(ChatMessage(role="tool", content=tool_result))
                call_llm(api_key, chat_histories, chatRequest)
            else:
                print("Lora: invalid tool call, missing expression")
        else:
            # Parsed JSON but not a recognized tool call — print it.
            print("Lora:", response_content)
            chat_histories.append(
                ChatMessage(role="assistant", content=response_content)
            )


def calculate(expression: str) -> str:
    node = ast.parse(expression, mode="eval")
    return str(_eval(node))


def _eval(node):
    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in operators:
            return operators[op_type](left, right)
    elif isinstance(node, ast.Expression):
        return _eval(node.body)


if __name__ == "__main__":
    # print(calculate("2+3"))
    main()
