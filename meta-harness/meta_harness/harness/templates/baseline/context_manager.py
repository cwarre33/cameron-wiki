import pathlib


class ContextManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def build_context(self, task: str, history: list[dict]) -> list[dict]:
        messages = [
            {"role": "system", "content": self._load_system_prompt()},
            {"role": "user", "content": task},
        ]
        for entry in history:
            if isinstance(entry, dict) and "content" in entry:
                messages.append({"role": "assistant", "content": entry["content"]})
            else:
                messages.append({"role": "assistant", "content": str(entry)})
        return messages

    def _load_system_prompt(self) -> str:
        path = pathlib.Path(__file__).parent / "system_prompt.md"
        with open(path) as f:
            return f.read()
