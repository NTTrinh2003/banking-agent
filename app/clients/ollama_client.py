"""
Run on Colab + Pinggy
Usage:
    from app.clients.ollama_client import OllamaClient
    client = get_ollama_client()
    client.chat([
        {"role": "system", "content": "You are a banking assistant."},
        {"role": "user", "content": "My transfer failed"},
    ])
"""

from functools import lru_cache
import requests

from app.clients.base import LLMClient, Message
from app.core.settings import get_settings

class OllamaClient(LLMClient):
    """
    HTTP Client for Ollama's /api/generate and /api/chat endpoints
    """

    def __init__(self, base_url: str, model: str, timeout: str):
        self._base_url = base_url
        self._model = model
        self._timeout = timeout
        self._session = requests.Session()

    @staticmethod
    def _normalize_url(url: str) -> str:
        url = url.rstrip("/")
        for suffix in ("/api/chat", "/api/generate"):
            if url.endswith(suffix):
                url = url[:-len(suffix)]
        return url

    def _ensure_configured(self) -> None:
        if not self._base_url:
            raise RuntimeError(
                "OLLAMA_URL is not set. Start the colab notebook, run the Pinggy "
                "tunnel (shh -p 443 -R0:localhost:11434 qr#a.pinggy.io), and put "
                "the public URL in your .env file."
            )

    def _post(self, endpoint: str, payload: dict) -> dict:
        """
        Shared HTTP POST endpoint for Ollama's /chat endpoint
        """
        self._ensure_configured()
        url = f"{self._base_url}{endpoint}"
        try:
            response = self._session.post(url, json=payload, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            raise RuntimeError(
                f"Ollama request timed out after {self._timeout} seconds. "
                f"First call after model load can be slow - try increasing OLLAMA_TIMEOUT."
            ) from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}") from e

    def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        """
        One-shot completion via /api/generate
        """
        payload: dict = {
            "model": self._model,
            "prompt": prompt,
            "stream": False, # Full response in one shot, no chunks
        }

        if json_mode:
            payload["format"] = "json"

        data = self._post("/api/generate", payload)
        return data.get("response", "")

    def chat(self, messages: list[Message], *, json_mode: bool = False) -> str:
        """
        Multi-turn completion via /api/chat endpoint
        """
        payload: dict = {
            "model": self._model,
            "messages": messages,
            "stream": False,
        }

        if json_mode:
            payload["format"] = "json"

        data = self._post("/api/chat", payload)
        return data.get("messages", {}).get("content", "")

@lru_cache
def get_ollama_client() -> OllamaClient:
    """
    Cached client accessor
    """
    settings = get_settings()
    return OllamaClient(
        base_url=settings.ollama_url,
        model=settings.ollama_model,
        timeout=settings.ollama_timeout,
    )