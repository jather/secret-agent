from dotenv import load_dotenv
import os
import sys
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("no api key found")


def main():
    parser = argparse.ArgumentParser(description="secret agent for coding")
    parser.add_argument("user_prompt", type=str, help="Prompt given by user")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    #  generate message
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    print(response.text)
    function_results = []
    if response.function_calls:
        for function in response.function_calls:
            function_call_result = call_function(function, args.verbose)
            if not function_call_result.parts:
                raise Exception(
                    "function call result should have non-empty .parts list"
                )
            if not function_call_result.parts[0].function_response:
                raise Exception(
                    "function call result function_response should not be None"
                )
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    promt_tokens, usage_tokens = (
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\nPrompt tokens: {promt_tokens}\nResponse tokens: {usage_tokens}"
        )


if __name__ == "__main__":
    main()
