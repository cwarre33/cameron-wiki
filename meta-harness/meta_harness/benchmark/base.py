from abc import ABC, abstractmethod
from pathlib import Path


class BenchmarkAdapter(ABC):
    @abstractmethod
    def load_tasks(self, split: str = "test") -> list[dict]:
        pass

    @abstractmethod
    def evaluate(self, task_id: str, harness_path: Path) -> dict:
        pass

    def score(self, results: list[dict]) -> dict:
        total = len(results)
        passed = sum(1 for r in results if r.get("success"))
        tokens = [r.get("tokens", 0) for r in results]
        return {
            "accuracy": passed / total if total > 0 else 0.0,
            "passed": passed,
            "total": total,
            "mean_tokens": sum(tokens) / total if total > 0 else 0.0,
        }
