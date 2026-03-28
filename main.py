from dotenv import load_dotenv
import os
from google import genai
import argparse
from google.genai import types
from make_request import make_request

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("no api key found")


def main():
    parser = argparse.ArgumentParser(description="secret agent for coding")
    parser.add_argument("user_prompt", type=str, help="Prompt given by user")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    function_results = []

    for _ in range(20):
        messages, function_results = make_request(
            args, client, messages, function_results
        )
        if not function_results:
            break
    else:
        print("was not able to complete task within 20 iterations")
        exit(1)


if __name__ == "__main__":
    main()
