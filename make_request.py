from google.genai import types
from prompts import system_prompt
from functions.call_function import call_function, available_functions


def make_request(args, client, messages, function_results):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

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

    messages.append(types.Content(role="user", parts=function_results))

    promt_tokens, usage_tokens = (
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )
    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\nPrompt tokens: {promt_tokens}\nResponse tokens: {usage_tokens}"
        )

    if not function_results:
        print(response.text)

    return messages, function_results
