import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.system import DEFAULT_SYSTEM_PROMPT
from functions.call_functions import AVAILABLE_FUNCTIONS, call_function


GEMINI_API_KEY_ENV_VAR = "GEMINI_API_KEY"
MODEL = "gemini-2.5-flash"
MAX_MODEL_REQUESTS = 20


def main():
    load_dotenv()
    api_key = os.environ.get(GEMINI_API_KEY_ENV_VAR)
    if not api_key:
        raise Exception(GEMINI_API_KEY_ENV_VAR)
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Prompt for AI chatbot.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    finished = False
    for _ in range(MAX_MODEL_REQUESTS):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=DEFAULT_SYSTEM_PROMPT,
                temperature=0,
                tools=AVAILABLE_FUNCTIONS,
            ),
        )

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.function_calls:
            func_responses = []
            for function_call in response.function_calls:
                func_call_result = call_function(function_call, verbose)
                first_part = func_call_result.parts[0]
                if not first_part.function_response or not first_part.function_response.response:
                    raise Exception(f"Error when calling function {function_call.name}. Response was None.")
                func_responses.append(first_part)
                if verbose:
                    print(f"-> {first_part.function_response.response}")
            messages.append(types.Content(role="user", parts=func_responses))
        else:
            print(f"Response:\n{response.text}")
            finished = True
            break
    if not finished:
        print(f"Model did not finish after {MAX_MODEL_REQUESTS} iterations.")
        exit(1)



if __name__ == "__main__":
    main()
