"""
LLM provider abstraction layer.
Supports OpenAI-compatible APIs (OpenAI, Ollama, DeepSeek, etc.).
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import os


class LLMProvider(ABC):
    """Abstract base for LLM backends."""

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send a list of messages and return the assistant reply."""
        ...


# ---------------------------------------------------------------------------
# OpenAI-compatible provider
# ---------------------------------------------------------------------------

class OpenAICompatProvider(LLMProvider):
    """Covers OpenAI, Ollama, DeepSeek, and any OpenAI-compatible endpoint."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o-mini",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package is required. Install with: pip install openai"
            )

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            max_tokens=1024,
        )
        return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Dummy / fallback provider (used when no LLM is configured)
# ---------------------------------------------------------------------------

class DummyProvider(LLMProvider):
    """Fallback when no LLM is configured."""
    def chat(self, messages: List[Dict[str, str]]) -> str:
        user_msg = messages[-1]["content"] if messages else ""
        return (
            f"[未接入大模型] 收到你的消息：{user_msg}。\n\n"
            "请在项目根目录创建 .env 文件并配置 LLM_API_KEY 来接入大模型。"
        )


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """你是一位温暖、善解人意的情绪树洞，名字叫「小树」。你的职责是：
1. 认真倾听用户的情绪倾诉，给予共情和陪伴。
2. 用温柔自然的语气回应，像朋友聊天一样。
3. 对话结束时，如果合适，可以帮用户简单总结一下今天的心情。

注意：
- 回应简洁自然，200 字以内。
- 不要像机器人一样说话，要有人情味。
- 用户提到负面情绪时，先共情，再温和引导。"""


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_llm_provider() -> LLMProvider:
    """
    Return an LLM provider based on environment variables.

    Environment variables:
        LLM_PROVIDER: "openai" (default), "ollama", "deepseek", "openai-compat", "none"
        LLM_API_KEY:  API key (required for real providers)
        LLM_BASE_URL: Custom endpoint (optional, overrides default)
        LLM_MODEL:    Model name (optional)
    """
    provider_name = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("LLM_API_KEY", "").strip()

    # If explicitly set to "none" or no API key provided, use dummy
    if provider_name == "none" or not api_key:
        return DummyProvider()

    # Default base URLs per provider
    base_urls = {
        "openai": "https://api.openai.com/v1",
        "ollama": "http://localhost:11434/v1",
        "deepseek": "https://api.deepseek.com/v1",
    }
    base_url = os.getenv("LLM_BASE_URL", base_urls.get(provider_name, "https://api.openai.com/v1"))

    default_models = {
        "openai": "gpt-4o-mini",
        "ollama": "qwen2.5:7b",
        "deepseek": "deepseek-chat",
    }
    model = os.getenv("LLM_MODEL", default_models.get(provider_name, "gpt-4o-mini"))

    return OpenAICompatProvider(api_key=api_key, base_url=base_url, model=model)


def build_messages(user_content: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Build the full message list for the LLM, including system prompt and recent history."""
    messages = [{"role": "system", "content": _SYSTEM_PROMPT}]

    # Include last 20 messages as context (about 10 turns)
    for msg in history[-20:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_content})
    return messages
