import json
from pathlib import Path

from meta_harness.benchmark.terminalbench import TerminalBenchAdapter
from meta_harness.harness.validator import HarnessValidator
from meta_harness.loop.convergence import ConvergenceTracker
from meta_harness.meta_agent.proposer import MetaAgent
from meta_harness.trace.store import TraceStore


class OptimizerLoop:
    def __init__(self, config: dict, baseline_harness: Path | None = None):
        self.config = config
        self.trace_store = TraceStore(config["traces"]["root"])
        self.convergence = ConvergenceTracker(
            patience=config["loop"]["patience"],
            subset_size=config["loop"]["subset_size"],
            max_iterations=config["loop"]["max_iterations"],
        )
        self.validator = HarnessValidator()
        benchmark_config = config.get("benchmark", {})
        self.adapter = TerminalBenchAdapter(
            dataset_name=benchmark_config.get("dataset_name", "terminal-bench-core"),
            version=benchmark_config.get("version", "0.1.1"),
            task_dir=Path(benchmark_config["task_dir"]) if benchmark_config.get("task_dir") else None,
        )
        self.baseline_harness = baseline_harness or Path(__file__).parent.parent / "harness" / "templates" / "baseline"
        self.meta_agent: MetaAgent | None = None

    def set_meta_agent(self, meta_agent: MetaAgent):
        self.meta_agent = meta_agent

    def run(self):
        iter_id = 0
        harness_path = self.baseline_harness

        while iter_id < self.config["loop"]["max_iterations"]:
            # Evaluate
            tasks = self.convergence.get_tasks(self.adapter)
            results = []
            for task in tasks:
                result = self.adapter.evaluate(task["id"], harness_path)
                results.append(result)

            scores = self.adapter.score(results)
            self.trace_store.save(iter_id, harness_path, results, scores)

            # Check convergence
            if self.convergence.should_stop(scores, iter_id):
                break

            if self.meta_agent is None:
                raise RuntimeError("MetaAgent not set. Call set_meta_agent() before running.")

            # Propose new harness
            new_harness = self.meta_agent.propose(self.trace_store, iter_id + 1)

            # Validate
            errors = self.validator.validate(new_harness)
            if errors:
                # Save error trace and continue with old harness
                self.trace_store.save(iter_id + 1, harness_path, [], {
                    "accuracy": scores["accuracy"],
                    "passed": scores["passed"],
                    "total": scores["total"],
                    "mean_tokens": scores["mean_tokens"],
                    "validation_errors": errors,
                })
                iter_id += 1
                continue

            harness_path = new_harness
            iter_id += 1
