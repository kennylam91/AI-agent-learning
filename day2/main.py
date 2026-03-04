import requests
import dotenv
import json


def main():
    api_key = dotenv.dotenv_values().get("OPEN_ROUTER_API_KEY")

    if api_key is None:
        print("api_key is missing")
        return

    print("Hi, I'm Lora, your AI assistance. What can I help you today?")
    user_input = ""
    while True:
        user_input = input("you: ")

        if user_input == "exit" or user_input == "quit":
            return

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(
                {
                    "model": "stepfun/step-3.5-flash:free",
                    "messages": [{"role": "user", "content": buildPrompt(user_input)}],
                }
            ),
            headers={"Authorization": "Bearer " + api_key},
        )

        response.raise_for_status()
        response_data = response.json()
        choice = response_data["choices"][0]
        print(f"AI: {choice['message']['content']}")


def buildPrompt(userInput: str) -> str:
    return f"You are a helpful assistant. Answer clearly and concisely. If you don't know, say no. Here's the user prompt: {userInput}"


if __name__ == "__main__":
    main()
