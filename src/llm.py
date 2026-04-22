import os
from pydantic import SecretStr
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API_KEY is not set")

    base_url = "https://openrouter.ai/api/v1"
    secret_key = SecretStr(api_key)

    primary = ChatOpenAI(model="openrouter/auto",
                         api_key=secret_key, base_url=base_url)
    fallbacks = [
        ChatOpenAI(model="meta-llama/llama-3.3-70b-instruct",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="google/gemma-3-27b-it",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="google/gemma-3-12b-it:free",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="meta-llama/llama-guard-4-12b:free",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="minimax/minimax-m2.5:free",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="nousresearch/hermes-3-llama-3.1-405b:free",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="nvidia/nemotron-3-nano-30b-a3b:free",
                   api_key=secret_key, base_url=base_url),
        ChatOpenAI(model="nvidia/nemotron-3-super-120b-a12b:free",
                   api_key=secret_key, base_url=base_url),
    ]
    return primary.with_fallbacks(fallbacks)
