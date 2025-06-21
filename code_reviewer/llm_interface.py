"""
LLM provider switchboard.
Default: local Ollama (`llama3.2` at http://localhost:11434/v1).
Switch provider/model by environment variables:

    export LLM_PROVIDER=openai
    export LLM_MODEL=gpt-4o
    export OPENAI_API_KEY=...

Supported providers so far: 'ollama', 'openai'.
Add more by extending `get_llm()`.
"""

from langchain_core.language_models import BaseLanguageModel
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
import os


def get_llm() -> BaseLanguageModel:
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    model_name = os.getenv("LLM_MODEL", "qwen3:8b-q4_K_M")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    if provider == "ollama":
        return ChatOllama(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=model_name,
            temperature=temperature,
            timeout=600,
        )

    if provider == "openai":
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            timeout=600,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER='{provider}'")
