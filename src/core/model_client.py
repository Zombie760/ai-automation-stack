"""
Model client for local AI servers.
For educational purposes only.

Supports LM Studio, Ollama, and any OpenAI-compatible API.
"""

import json
import logging
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError
from dataclasses import dataclass

log = logging.getLogger("model-client")


@dataclass
class ModelConfig:
    base_url: str = "http://127.0.0.1:1234/v1"
    model_name: str = "local-model"
    max_tokens: int = 2048
    temperature: float = 0.7
    timeout: int = 60


class ModelClient:
    """Client for OpenAI-compatible local model servers."""

    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()

    def complete(
        self,
        prompt: str,
        system: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, temperature=temperature, max_tokens=max_tokens)

    def chat(
        self,
        messages: list[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        payload = json.dumps({
            "model": self.config.model_name,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "stream": False,
        }).encode()

        req = Request(
            f"{self.config.base_url}/chat/completions",
            data=payload,
            method="POST",
        )
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=self.config.timeout) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]

    def models(self) -> list[str]:
        req = Request(f"{self.config.base_url}/models", method="GET")
        req.add_header("Content-Type", "application/json")

        try:
            with urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                return [m["id"] for m in data.get("data", [])]
        except (URLError, json.JSONDecodeError):
            return []

    def health(self) -> bool:
        try:
            return len(self.models()) > 0
        except Exception:
            return False
