from dotenv import load_dotenv
import os
import sys
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=api_key)
    prompt = ""
    flag = ""
    verbose = False

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        print("prompt must be provided as first argument")
        sys.exit(1)
    if len(sys.argv) > 2:
        flag = sys.argv[2]
    if flag == "--verbose":
        verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print(response.text)
    promt_tokens, usage_tokens = (
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    if verbose:
        print(
            f"User prompt: {prompt}\nPrompt tokens: {promt_tokens}\nResponse tokens: {usage_tokens}"
        )


if __name__ == "__main__":
    main()
