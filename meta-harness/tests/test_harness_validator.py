import tempfile
from pathlib import Path

import pytest

from meta_harness.harness.validator import HarnessValidator


class TestHarnessValidator:
    def test_valid_harness_passes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "tools.py").write_text("def execute_command(cmd): pass\ndef read_file(path): pass\n")
            validator = HarnessValidator()
            errors = validator.validate(harness)
            assert errors == []

    def test_missing_tools_py(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            validator = HarnessValidator()
            errors = validator.validate(harness)
            assert any("Missing tools.py" in e for e in errors)

    def test_dangerous_eval(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "tools.py").write_text("def run(code): eval(code)\n")
            validator = HarnessValidator()
            errors = validator.validate(harness)
            assert any("eval" in e for e in errors)

    def test_dangerous_exec(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "tools.py").write_text("def run(code): exec(code)\n")
            validator = HarnessValidator()
            errors = validator.validate(harness)
            assert any("exec" in e for e in errors)
