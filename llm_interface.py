from abc import ABC, abstractmethod
from typing import Any


class LLMClient(ABC):
    """LLM-agnostic interface. Implement this for Anthropic, OpenAI, local models, etc."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Return raw model text output."""
        raise NotImplementedError
