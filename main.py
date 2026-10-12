import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

if api_key is None:
    raise RuntimeError("API key not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]

def main():

    for i in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
            )

        if response.usage is None:
            raise RuntimeError("Usage information not found in the response")

        if args.verbose is True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls == None:
            print(f"Final response: {message.content}")
            return
        else:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, verbose=args.verbose)
                if result_message["content"] is None:
                    raise Exception
                if args.verbose is True:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)

        if i == 19:
            sys.exit("Max responses reached without a final answer. Exiting.")
            return

if __name__ == "__main__":
    main()