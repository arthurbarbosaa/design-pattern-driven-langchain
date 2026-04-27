import os
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


PRIMARY_MODEL = "openrouter/auto"
FALLBACK_MODELS = [
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemma-3-27b-it",
    "google/gemma-3-12b-it:free",
    "meta-llama/llama-guard-4-12b:free",
    "minimax/minimax-m2.5:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
]


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API_KEY is not set")

    base_url = "https://openrouter.ai/api/v1"
    secret_key = SecretStr(api_key)

    primary = ChatOpenAI(model=PRIMARY_MODEL,
                         api_key=secret_key, base_url=base_url)
    fallbacks = [
        ChatOpenAI(model=model_name, api_key=secret_key, base_url=base_url)
        for model_name in FALLBACK_MODELS
    ]
    return primary.with_fallbacks(fallbacks)


def get_runtime_model(result: dict) -> str:
    raw_result = result.get("raw") if isinstance(result, dict) else None
    response_metadata = getattr(raw_result, "response_metadata", {})
    if isinstance(response_metadata, dict):
        return response_metadata.get("model_name", "unknown")
    return "unknown"
