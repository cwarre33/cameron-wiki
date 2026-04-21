import random
from meta_harness.benchmark.base import BenchmarkAdapter


class ConvergenceTracker:
    def __init__(self, patience: int = 5, subset_size: int = 10, max_iterations: int = 50):
        self.patience = patience
        self.subset_size = subset_size
        self.max_iterations = max_iterations
        self.best_score = 0.0
        self.iterations_without_improvement = 0
        self.history = []

    def get_tasks(self, adapter: BenchmarkAdapter) -> list[dict]:
        all_tasks = adapter.load_tasks()
        random.seed(42)
        return random.sample(all_tasks, min(self.subset_size, len(all_tasks)))

    def should_stop(self, scores: dict, iter_id: int) -> bool:
        accuracy = scores.get("accuracy", 0.0)
        self.history.append((iter_id, accuracy))

        if accuracy > self.best_score:
            self.best_score = accuracy
            self.iterations_without_improvement = 0
        else:
            self.iterations_without_improvement += 1

        if self.iterations_without_improvement >= self.patience:
            return True
        if iter_id >= self.max_iterations - 1:
            return True
        return False
