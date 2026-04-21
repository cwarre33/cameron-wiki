import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.meta_agent.prompt_builder import PromptBuilder
from meta_harness.meta_agent.proposer import MetaAgent
from meta_harness.trace.store import TraceStore


class TestPromptBuilder:
    def test_build_includes_harness_code(self):
        builder = PromptBuilder()
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "agent.py").write_text("x = 1")
            (harness / "tools.py").write_text("def foo(): pass")
            store.save(0, harness, [], {"accuracy": 0.5, "passed": 5, "total": 10, "mean_tokens": 100})

            prompt = builder.build(store, current_iter=1)
            assert "agent.py" in prompt
            assert "x = 1" in prompt
            assert "tools.py" in prompt

    def test_build_includes_scores(self):
        builder = PromptBuilder()
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "agent.py").write_text("x = 1")
            store.save(0, harness, [], {"accuracy": 0.5, "passed": 5, "total": 10, "mean_tokens": 100})

            prompt = builder.build(store, current_iter=1)
            assert "0.5" in prompt or "accuracy" in prompt


class TestMetaAgent:
    def test_propose_parses_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TraceStore(tmpdir)
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "agent.py").write_text("x = 1")
            store.save(0, harness, [], {"accuracy": 0.5, "passed": 5, "total": 10, "mean_tokens": 100})

            mock_llm = MagicMock()
            mock_llm.complete.return_value = {
                "content": (
                    "### FILE: agent.py\n"
                    "x = 2\n"
                )
            }

            proposer = MetaAgent(llm_client=mock_llm, prompt_builder=PromptBuilder())
            new_harness = proposer.propose(store, current_iter=1)

            assert new_harness.exists()
            assert (new_harness / "agent.py").read_text().strip() == "x = 2"
