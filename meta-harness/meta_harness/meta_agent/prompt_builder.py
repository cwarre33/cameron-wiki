import json
from pathlib import Path

from meta_harness.trace.store import TraceStore


class PromptBuilder:
    def build(self, trace_store: TraceStore, current_iter: int) -> str:
        prev_iter = current_iter - 1
        current = trace_store.load(prev_iter)
        best_iter, best_scores = trace_store.get_best()

        sections = [
            self._section_intro(),
            self._section_rules(),
            self._section_harness(current),
            self._section_scores(prev_iter, current["scores"], best_iter, best_scores),
            self._section_failures(current),
            self._section_output_format(),
        ]
        return "\n\n".join(sections)

    def _section_intro(self) -> str:
        return (
            "You are an expert AI researcher and agent engineer. "
            "Your task is to analyze the execution traces of an agent harness and rewrite it to improve performance."
        )

    def _section_rules(self) -> str:
        return (
            "Rules:\n"
            "1. You may rewrite system_prompt.md, tools.py, context_manager.py, stop_conditions.py, and agent.py.\n"
            "2. Do NOT use eval(), exec(), or compile().\n"
            "3. The harness must expose an Agent class with a run(task: str) -> dict method.\n"
            "4. Keep changes focused. One major improvement per rewrite is better than many small changes.\n"
            "5. If a prior change had no effect, try a different approach."
        )

    def _section_harness(self, current: dict) -> str:
        harness_path = current["harness_path"]
        lines = ["Current Harness Code:"]
        for file_path in sorted(harness_path.rglob("*")):
            if file_path.is_file():
                rel = file_path.relative_to(harness_path)
                lines.append(f"\n### FILE: {rel}\n")
                lines.append(file_path.read_text())
        return "\n".join(lines)

    def _section_scores(self, iter_id: int, scores: dict, best_iter: int, best_scores: dict) -> str:
        return (
            f"Iteration {iter_id} Scores:\n"
            f"{json.dumps(scores, indent=2)}\n\n"
            f"Best Scores (iteration {best_iter}):\n"
            f"{json.dumps(best_scores, indent=2)}"
        )

    def _section_failures(self, current: dict) -> str:
        failures = [t for t in current.get("traces", []) if not t.get("success")]
        if not failures:
            return "No failures in this iteration.\n"
        lines = ["Failure Traces (first 5):"]
        for trace in failures[:5]:
            lines.append(json.dumps(trace, indent=2))
        return "\n".join(lines)

    def _section_output_format(self) -> str:
        return (
            "Output the new harness files in this exact format:\n\n"
            "### FILE: <filename>\n"
            "<file content>\n\n"
            "Example:\n"
            "### FILE: agent.py\n"
            "class Agent:\n"
            "    def run(self, task: str):\n"
            "        return {'answer': '42'}\n"
        )
