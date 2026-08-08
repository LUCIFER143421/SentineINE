import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from gemini_analyzer import MODEL_ID, build_quota_error, get_max_output_tokens
from image_processor import MAX_IMAGE_DIMENSION


def get_api_key():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def print_config():
    print("SentinelNE Gemini diagnostics")
    print(f"Model: {MODEL_ID}")
    print(f"Max output tokens: {get_max_output_tokens()}")
    print(f"Max image dimension: {MAX_IMAGE_DIMENSION}")


def print_available_models(client):
    print("\nModels visible to this API key:")
    for model in client.models.list():
        supported_actions = ", ".join(getattr(model, "supported_actions", []) or [])
        print(f"- {model.name} ({supported_actions})")


def run_text_probe(client):
    print("\nRunning tiny text-only probe...")
    response = client.models.generate_content(
        model=MODEL_ID,
        contents="Reply with OK only.",
        config=types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=16,
        ),
    )
    print(f"Probe response: {response.text}")


def explain_error(error):
    error_text = str(error)
    error_lower = error_text.lower()
    print("\nGemini request failed.")
    if (
        "429" in error_text
        or "resource_exhausted" in error_lower
        or "quota" in error_lower
        or "rate limit" in error_lower
    ):
        print(build_quota_error(error_text))
        print("\nWhat this proves:")
        print("- The issue is with API quota/model access, not the uploaded image.")
        print("- If this tiny text-only probe fails, resizing images will not fix it.")
        print("- Check Google AI Studio / Google Cloud quota for this API key/project.")
    else:
        print(error_text)


def main():
    parser = argparse.ArgumentParser(
        description="Verify Gemini API key, model access, and quota before running the Streamlit app."
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models visible to the configured API key.",
    )
    args = parser.parse_args()

    print_config()
    api_key = get_api_key()
    if not api_key:
        print("\nMissing GEMINI_API_KEY. Add it to .env first.")
        return 1

    client = genai.Client(api_key=api_key)
    try:
        if args.list_models:
            print_available_models(client)
        run_text_probe(client)
    except Exception as error:
        explain_error(error)
        return 1

    print("\nGemini API key/model probe passed.")
    print("If the Streamlit app still fails only with images, lower MAX_IMAGE_DIMENSION.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
