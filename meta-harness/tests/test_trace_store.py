import json
import tempfile
from pathlib import Path

import pytest

from meta_harness.trace.store import TraceStore


class TestTraceStore:
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            harness_path = Path(tmpdir) / "fake_harness"
            harness_path.mkdir()
            (harness_path / "agent.py").write_text("# agent")
            traces = [{"task_id": "t1", "success": True, "tokens": 100}]
            scores = {"accuracy": 1.0, "passed": 1, "total": 1, "mean_tokens": 100}

            iter_dir = store.save(iter_id=0, harness_path=harness_path, traces=traces, scores=scores)

            assert iter_dir.exists()
            assert (iter_dir / "scores.json").exists()
            assert (iter_dir / "harness" / "agent.py").exists()
            assert (iter_dir / "traces" / "task_0.json").exists()

    def test_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            harness_path = Path(tmpdir) / "fake_harness"
            harness_path.mkdir()
            (harness_path / "agent.py").write_text("# agent")
            store.save(0, harness_path, [{"task_id": "t1", "success": True, "tokens": 100}], {"accuracy": 1.0, "passed": 1, "total": 1, "mean_tokens": 100})

            loaded = store.load(0)
            assert loaded["scores"]["accuracy"] == 1.0
            assert loaded["harness_path"].exists()

    def test_get_best(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            for i in range(3):
                harness_path = Path(tmpdir) / f"fake_harness_{i}"
                harness_path.mkdir()
                (harness_path / "agent.py").write_text("# agent")
                acc = 0.2 + (i * 0.3)
                store.save(i, harness_path, [], {"accuracy": acc, "passed": int(acc * 10), "total": 10, "mean_tokens": 100})

            best_iter, best_scores = store.get_best()
            assert best_iter == 2
            assert best_scores["accuracy"] == 0.8

    def test_diff_generated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            h1 = Path(tmpdir) / "h1"
            h1.mkdir()
            (h1 / "agent.py").write_text("x = 1")
            store.save(0, h1, [], {"accuracy": 0.0, "passed": 0, "total": 1, "mean_tokens": 0})

            h2 = Path(tmpdir) / "h2"
            h2.mkdir()
            (h2 / "agent.py").write_text("x = 2")
            store.save(1, h2, [], {"accuracy": 0.0, "passed": 0, "total": 1, "mean_tokens": 0})

            diff_path = Path(tmpdir) / "iter_001" / "diff.patch"
            assert diff_path.exists()
            content = diff_path.read_text()
            assert "x = 1" in content or "x = 2" in content
