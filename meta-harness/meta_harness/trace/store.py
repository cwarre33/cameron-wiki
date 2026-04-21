import json
import shutil
from pathlib import Path


class TraceStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        iter_id: int,
        harness_path: Path,
        traces: list[dict],
        scores: dict,
    ) -> Path:
        iter_dir = self.root / f"iter_{iter_id:03d}"
        iter_dir.mkdir(exist_ok=True)

        harness_dest = iter_dir / "harness"
        if harness_dest.exists():
            shutil.rmtree(harness_dest)
        shutil.copytree(harness_path, harness_dest)

        traces_dir = iter_dir / "traces"
        traces_dir.mkdir(exist_ok=True)
        for i, trace in enumerate(traces):
            with open(traces_dir / f"task_{i}.json", "w") as f:
                json.dump(trace, f, indent=2)

        with open(iter_dir / "scores.json", "w") as f:
            json.dump(scores, f, indent=2)

        if iter_id > 0:
            prev_harness = self.root / f"iter_{iter_id - 1:03d}" / "harness"
            diff = self._generate_diff(prev_harness, harness_dest)
            with open(iter_dir / "diff.patch", "w") as f:
                f.write(diff)

        return iter_dir

    def load(self, iter_id: int) -> dict:
        iter_dir = self.root / f"iter_{iter_id:03d}"
        with open(iter_dir / "scores.json") as f:
            scores = json.load(f)
        traces_dir = iter_dir / "traces"
        traces = []
        if traces_dir.exists():
            for trace_file in sorted(traces_dir.glob("*.json")):
                with open(trace_file) as f:
                    traces.append(json.load(f))
        return {
            "harness_path": iter_dir / "harness",
            "scores": scores,
            "traces": traces,
        }

    def get_best(self) -> tuple[int, dict]:
        best_iter = -1
        best_score = -1.0
        best_scores = {}
        for iter_dir in sorted(self.root.glob("iter_*")):
            iter_num = int(iter_dir.name.split("_")[1])
            with open(iter_dir / "scores.json") as f:
                scores = json.load(f)
            accuracy = scores.get("accuracy", 0.0)
            if accuracy > best_score:
                best_score = accuracy
                best_iter = iter_num
                best_scores = scores
        return best_iter, best_scores

    def _generate_diff(self, prev: Path, curr: Path) -> str:
        import difflib

        diff_lines = []
        for prev_file in prev.rglob("*"):
            if prev_file.is_file():
                rel = prev_file.relative_to(prev)
                curr_file = curr / rel
                if curr_file.exists():
                    with open(prev_file) as f1, open(curr_file) as f2:
                        lines1 = f1.readlines()
                        lines2 = f2.readlines()
                    file_diff = difflib.unified_diff(
                        lines1, lines2, fromfile=str(rel), tofile=str(rel)
                    )
                    diff_lines.extend(file_diff)
                else:
                    diff_lines.append(f"--- {rel}\n+++ deleted\n")
        return "".join(diff_lines)
