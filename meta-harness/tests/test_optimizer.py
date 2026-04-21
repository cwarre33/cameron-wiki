import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.loop.optimizer import OptimizerLoop


class TestOptimizerLoop:
    def test_single_iteration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "traces": {"root": str(Path(tmpdir) / "traces")},
                "loop": {"max_iterations": 1, "patience": 5, "subset_size": 2},
                "benchmark": {"name": "dummy", "task_dir": str(tmpdir), "command": "echo"},
            }

            # Create fake tasks file
            with open(Path(tmpdir) / "test.json", "w") as f:
                json.dump([{"id": "t1"}, {"id": "t2"}], f)

            # Create fake baseline harness
            baseline = Path(tmpdir) / "baseline"
            baseline.mkdir()
            (baseline / "__init__.py").write_text("")
            (baseline / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client): pass
    def run(self, task: str):
        return {"answer": "done", "history": []}
''')
            (baseline / "system_prompt.md").write_text("You are an agent.")
            (baseline / "tools.py").write_text("def execute_command(cmd): pass\n")
            (baseline / "context_manager.py").write_text("class ContextManager: pass\n")
            (baseline / "stop_conditions.py").write_text("class StopConditions: pass\n")

            loop = OptimizerLoop(config, baseline_harness=baseline)

            # Mock the adapter to return success
            loop.adapter.evaluate = MagicMock(return_value={"success": True, "trace": {}, "tokens": 50})

            loop.run()

            assert loop.trace_store.root.exists()
            assert (loop.trace_store.root / "iter_000" / "scores.json").exists()
