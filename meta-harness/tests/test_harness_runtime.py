import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.harness.runtime import HarnessRuntime


class TestHarnessRuntime:
    def test_run_loads_and_executes_agent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "__init__.py").write_text("")
            (harness / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    def run(self, task: str):
        return {"answer": "42", "history": [{"content": "done"}]}
''')
            (harness / "system_prompt.md").write_text("You are an agent.")
            (harness / "tools.py").write_text("def execute_command(cmd): pass\n")
            (harness / "context_manager.py").write_text("class ContextManager: pass\n")
            (harness / "stop_conditions.py").write_text("class StopConditions: pass\n")

            runtime = HarnessRuntime(harness)
            mock_llm = MagicMock()
            result = runtime.run("What is 6*7?", mock_llm)

            assert result["answer"] == "42"
            assert len(result["history"]) == 1
