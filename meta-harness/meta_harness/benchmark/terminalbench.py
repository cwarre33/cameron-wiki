import json
import os
import subprocess
from pathlib import Path

from meta_harness.benchmark.base import BenchmarkAdapter


class TerminalBenchAdapter(BenchmarkAdapter):
    def __init__(self, dataset_name: str = "terminal-bench-core", version: str = "0.1.1", task_dir: Path | None = None):
        self.dataset_name = dataset_name
        self.version = version
        self.task_dir = task_dir
        self._tasks = None

    def _get_dataset(self):
        from terminal_bench.dataset.dataset import Dataset
        return Dataset(name=self.dataset_name, version=self.version)

    def load_tasks(self, split: str = "test") -> list[dict]:
        dataset = self._get_dataset()
        tasks = []
        for task_path in dataset.tasks:
            task_yaml = task_path / "task.yaml"
            if task_yaml.exists():
                import yaml
                with open(task_yaml) as f:
                    task_data = yaml.safe_load(f)
                task_data["id"] = task_path.name
                task_data["path"] = str(task_path)
                tasks.append(task_data)
        return tasks

    def evaluate(self, task_id: str, harness_path: Path) -> dict:
        # Run TerminalBench harness via CLI
        output_dir = Path("runs") / f"meta_harness_{task_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "python", "-m", "terminal_bench.cli.tb.main", "run",
            "-d", f"{self.dataset_name}=={self.version}",
            "-t", task_id,
            "-a", "oracle",  # Use oracle agent for now, will be replaced with harness agent
            "--no-cleanup",
            "--output-path", str(output_dir),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )

            # Find the results JSON
            result_files = list(output_dir.glob("*/results.json"))
            if not result_files:
                return {
                    "task_id": task_id,
                    "success": False,
                    "trace": {"stdout": result.stdout, "stderr": result.stderr},
                    "tokens": 0,
                }

            with open(result_files[0]) as f:
                data = json.load(f)

            # Find the specific task result
            task_result = None
            for r in data.get("results", []):
                if r.get("task_id") == task_id:
                    task_result = r
                    break

            if task_result:
                is_resolved = task_result.get("is_resolved")
                return {
                    "task_id": task_id,
                    "success": is_resolved if is_resolved is not None else False,
                    "trace": task_result,
                    "tokens": (task_result.get("total_input_tokens") or 0) + (task_result.get("total_output_tokens") or 0),
                }
            else:
                return {
                    "task_id": task_id,
                    "success": False,
                    "trace": data,
                    "tokens": 0,
                }

        except subprocess.TimeoutExpired:
            return {
                "task_id": task_id,
                "success": False,
                "trace": {"error": "timeout"},
                "tokens": 0,
            }
        except Exception as e:
            return {
                "task_id": task_id,
                "success": False,
                "trace": {"error": str(e)},
                "tokens": 0,
            }
