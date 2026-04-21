import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from meta_harness.benchmark.terminalbench import TerminalBenchAdapter


class TestBenchmarkAdapter:
    def test_load_tasks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks = [{"id": "t1"}, {"id": "t2"}]
            task_file = Path(tmpdir) / "test.json"
            with open(task_file, "w") as f:
                json.dump(tasks, f)

            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command="echo '{}' ")
            loaded = adapter.load_tasks(split="test")
            assert len(loaded) == 2
            assert loaded[0]["id"] == "t1"

    def test_evaluate_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks = [{"id": "t1"}]
            task_file = Path(tmpdir) / "test.json"
            with open(task_file, "w") as f:
                json.dump(tasks, f)

            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command='python -c "import json; print(json.dumps({\'success\': True, \'trace\': {}, \'tokens\': 100}))"')
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            result = adapter.evaluate("t1", harness)
            assert result["success"] is True
            assert result["tokens"] == 100

    def test_score(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command="echo")
            results = [
                {"success": True, "tokens": 100},
                {"success": False, "tokens": 200},
                {"success": True, "tokens": 150},
            ]
            scores = adapter.score(results)
            assert scores["accuracy"] == 2 / 3
            assert scores["passed"] == 2
            assert scores["total"] == 3
            assert scores["mean_tokens"] == 150.0
