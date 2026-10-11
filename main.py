import argparse
import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt

from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    try:
        api_key = os.environ.get("QROQ_API_KEY")
        base_url = os.environ.get("QROQ_BASE_URL")
        if api_key is None:
            raise RuntimeError("Api key is not provided")
    except RuntimeError:
        print("Add openrouter api key to .env")

    client = OpenAI(base_url=base_url, api_key=api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(10):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages, 
            temperature=0,
            tools=available_functions
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Final response:\n{message.content}")
            break

        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")

            result_message = call_function(tool_call, function_args)
            messages.append(result_message)
            print(f'{_}/{tool_call.id}/{tool_call.function.name}/{tool_call.function.arguments}')
            print(f'{result_message}')
            if result_message["content"] is None:
                raise Exception("Content is empty.") 
            if args.verbose:
                print(f"-> {result_message['content']}")
            elif message.content:
                print(message.content)

        if response.usage is None:
            raise RuntimeError("Usage object is None")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

if __name__ == "__main__":
    main()
