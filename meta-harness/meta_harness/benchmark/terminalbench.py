import json
import os
import subprocess
from pathlib import Path

from meta_harness.benchmark.base import BenchmarkAdapter


class TerminalBenchAdapter(BenchmarkAdapter):
    def __init__(self, task_dir: Path, command: str | None = None):
        self.task_dir = Path(task_dir)
        self.command = command or "python -m terminalbench.run"

    def load_tasks(self, split: str = "test") -> list[dict]:
        task_file = self.task_dir / f"{split}.json"
        with open(task_file) as f:
            return json.load(f)

    def evaluate(self, task_id: str, harness_path: Path) -> dict:
        env = os.environ.copy()
        env["HARNESS_PATH"] = str(harness_path)
        env["TASK_ID"] = task_id

        result = subprocess.run(
            self.command,
            shell=True,
            capture_output=True,
            text=True,
            env=env,
            timeout=300,
        )

        try:
            data = json.loads(result.stdout)
            return {
                "task_id": task_id,
                "success": data.get("success", False),
                "trace": data.get("trace", {}),
                "tokens": data.get("tokens", 0),
            }
        except json.JSONDecodeError:
            return {
                "task_id": task_id,
                "success": False,
                "trace": {"stdout": result.stdout, "stderr": result.stderr},
                "tokens": 0,
            }
