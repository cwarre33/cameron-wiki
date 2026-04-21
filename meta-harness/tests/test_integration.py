import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.loop.optimizer import OptimizerLoop
from meta_harness.meta_agent.proposer import MetaAgent


class TestIntegration:
    def test_full_loop_with_mock_llm(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup tasks
            with open(Path(tmpdir) / "test.json", "w") as f:
                json.dump([{"id": "t1"}], f)

            # Setup baseline harness
            baseline = Path(tmpdir) / "baseline"
            baseline.mkdir()
            (baseline / "__init__.py").write_text("")
            (baseline / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client): pass
    def run(self, task: str):
        return {"answer": "42", "history": []}
''')
            (baseline / "system_prompt.md").write_text("You are an agent.")
            (baseline / "tools.py").write_text("def execute_command(cmd): pass\n")
            (baseline / "context_manager.py").write_text("class ContextManager: pass\n")
            (baseline / "stop_conditions.py").write_text("class StopConditions: pass\n")

            config = {
                "traces": {"root": str(Path(tmpdir) / "traces")},
                "loop": {"max_iterations": 2, "patience": 5, "subset_size": 1},
                "benchmark": {"name": "dummy", "task_dir": str(tmpdir), "command": "echo"},
            }

            loop = OptimizerLoop(config, baseline_harness=baseline)
            loop.adapter.evaluate = MagicMock(return_value={"success": True, "trace": {}, "tokens": 50})

            mock_llm = MagicMock()
            mock_llm.complete.return_value = {
                "content": (
                    "### FILE: agent.py\n"
                    "class Agent:\n"
                    "    def __init__(self, llm_client): pass\n"
                    "    def run(self, task: str):\n"
                    "        return {'answer': '42', 'history': []}\n"
                )
            }

            meta_agent = MetaAgent(llm_client=mock_llm)
            loop.set_meta_agent(meta_agent)

            loop.run()

            # Verify traces were saved
            assert (loop.trace_store.root / "iter_000" / "scores.json").exists()
            assert (loop.trace_store.root / "iter_001" / "scores.json").exists()
