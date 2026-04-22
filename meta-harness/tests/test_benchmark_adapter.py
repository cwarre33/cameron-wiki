import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from meta_harness.benchmark.base import BenchmarkAdapter
from meta_harness.benchmark.terminalbench import TerminalBenchAdapter


class TestBenchmarkAdapter:
    def test_load_tasks(self):
        # Test with a mock adapter that doesn't need TerminalBench dataset
        adapter = MockAdapter()
        loaded = adapter.load_tasks()
        assert len(loaded) == 2
        assert loaded[0]["id"] == "t1"

    def test_evaluate_success(self):
        adapter = MockAdapter()
        harness = Path(tempfile.mkdtemp()) / "harness"
        harness.mkdir()
        result = adapter.evaluate("t1", harness)
        assert result["success"] is True
        assert result["tokens"] == 100

    def test_score(self):
        adapter = MockAdapter()
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


class MockAdapter(BenchmarkAdapter):
    def load_tasks(self, split: str = "test") -> list[dict]:
        return [{"id": "t1"}, {"id": "t2"}]

    def evaluate(self, task_id: str, harness_path: Path) -> dict:
        return {"task_id": task_id, "success": True, "trace": {}, "tokens": 100}
