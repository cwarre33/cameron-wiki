from .context_manager import ContextManager
from .stop_conditions import StopConditions
from .tools import execute_command, read_file, submit


class Agent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.tools = {
            "execute_command": execute_command,
            "read_file": read_file,
            "submit": submit,
        }
        self.context_manager = ContextManager()
        self.stop_conditions = StopConditions()

    def run(self, task: str) -> dict:
        history = []
        while not self.stop_conditions.should_stop(history):
            context = self.context_manager.build_context(task, history)
            response = self.llm_client.complete(context, tools=self.tools)
            history.append(response)
        return {"history": history, "answer": self._extract_answer(history)}

    def _extract_answer(self, history: list[dict]) -> str:
        for entry in reversed(history):
            if isinstance(entry, dict) and entry.get("action") == "submit":
                return entry.get("answer", "")
        return ""
