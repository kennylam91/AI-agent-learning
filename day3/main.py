import requests
import dotenv
import json
import time
from pydantic import BaseModel
from typing import List
from datetime import datetime


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]


class LogEntry(BaseModel):
    timestamp: datetime
    model: str
    tokens: int
    latency: int
    user_input: str
    response: str


def main():
    api_key = dotenv.dotenv_values().get("OPEN_ROUTER_API_KEY")

    if api_key is None:
        print("api_key is missing")
        return

    print("Hi, I'm Lora, your AI assistance. What can I help you today?")
    user_input = ""
    log_file = open("day3/logs.jsonl", "a", encoding="utf-8")
    system_chat = ChatMessage(
        role="system",
        content="You are a helpful assistant. Answer clearly and concisely. If you don't know, say no",
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
                model="stepfun/step-3.5-flash:free", messages=chat_histories
            )

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
            response_content = choice["message"]["content"]
            print(response_content)
            log_entry = LogEntry(
                timestamp=datetime.now(),
                model=chatRequest.model,
                tokens=response_data["usage"]["total_tokens"],
                latency=int(latency_ms),
                user_input=user_input,
                response=response_content,
            )
            log_file.write(log_entry.model_dump_json() + "\n")
            log_file.flush()
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


if __name__ == "__main__":
    main()
