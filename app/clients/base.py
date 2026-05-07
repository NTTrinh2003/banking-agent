from typing import Protocol, runtime_checkable

# message format: {"role": "...", "content": "..."}
Message = dict[str, str]

@runtime_checkable
class LLMClient(Protocol):
    def generate(self, prompt: str, *, json_mode: bool = False) -> str:
        ...

    def chat(self, messages: list[Message], *, json_mode: bool = False) -> str:
        ...