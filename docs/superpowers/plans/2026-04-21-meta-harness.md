# Meta-Harness Optimizer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a closed optimization loop that iteratively rewrites an agent harness to maximize TerminalBench scores, architected for generalization to other benchmarks.

**Architecture:** Four-layer closed loop: TraceStore (filesystem) → BenchmarkAdapter (Harbor wrapper) → Harness (agent code) → MetaAgent (LLM engineer), orchestrated by OptimizerLoop with convergence detection.

**Tech Stack:** Python 3.11+, pytest, PyYAML, `openai` client (for NIM), `ollama` Python package, Docker (for TerminalBench/Harbor), `difflib` (standard library).

---

## File Structure

```
meta-harness/
├── pyproject.toml
├── requirements.txt
├── config.yaml
├── run.py
├── meta_harness/
│   ├── __init__.py
│   ├── loop/
│   │   ├── __init__.py
│   │   ├── optimizer.py          # Orchestrator
│   │   └── convergence.py        # Score tracking, rollback
│   ├── meta_agent/
│   │   ├── __init__.py
│   │   ├── proposer.py           # LLM interface
│   │   └── prompt_builder.py     # Assembles meta-agent context
│   ├── harness/
│   │   ├── __init__.py
│   │   ├── runtime.py            # Loads and runs harness
│   │   ├── validator.py          # Schema + safety checks
│   │   └── templates/
│   │       └── baseline/
│   │           ├── __init__.py
│   │           ├── agent.py
│   │           ├── system_prompt.md
│   │           ├── tools.py
│   │           ├── context_manager.py
│   │           └── stop_conditions.py
│   ├── benchmark/
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract adapter
│   │   └── terminalbench.py      # TerminalBench adapter
│   └── trace/
│       ├── __init__.py
│       ├── store.py              # Filesystem logic
│       └── compressor.py         # Trace serialization
└── tests/
    ├── __init__.py
    ├── conftest.py               # Shared fixtures
    ├── test_trace_store.py
    ├── test_benchmark_adapter.py
    ├── test_harness_validator.py
    ├── test_convergence.py
    └── test_meta_agent.py
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `meta-harness/pyproject.toml`
- Create: `meta-harness/requirements.txt`
- Create: `meta-harness/config.yaml`
- Create: directory structure

- [ ] **Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "meta-harness"
version = "0.1.0"
description = "Closed optimization loop for agent harness engineering"
requires-python = ">=3.11"
dependencies = [
    "pyyaml>=6.0",
    "openai>=1.0",
    "ollama>=0.1.0",
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
]

[project.optional-dependencies]
dev = ["black", "ruff", "mypy"]

[tool.setuptools.packages.find]
where = ["."]
include = ["meta_harness*"]
```

- [ ] **Step 2: Create requirements.txt**

```
pyyaml>=6.0
openai>=1.0
ollama>=0.1.0
pytest>=7.0
pytest-asyncio>=0.21.0
```

- [ ] **Step 3: Create config.yaml**

```yaml
loop:
  max_iterations: 50
  patience: 5
  subset_size: 10

models:
  meta_agent:
    provider: nim
    model: meta/llama-3.1-70b-instruct
    base_url: https://integrate.api.nvidia.com/v1
    api_key_env: NVIDIA_NIM_API_KEY
  harness:
    provider: ollama
    model: llama3.1:8b

benchmark:
  name: terminalbench
  task_dir: ./terminalbench_tasks
  command: "python -m terminalbench.run"

traces:
  root: ./traces
```

- [ ] **Step 4: Create directory structure**

Run:
```bash
mkdir -p meta-harness/meta_harness/{loop,meta_agent,harness/templates/baseline,benchmark,trace}
mkdir -p meta-harness/tests
touch meta-harness/meta_harness/__init__.py
touch meta-harness/meta_harness/loop/__init__.py
touch meta-harness/meta_harness/meta_agent/__init__.py
touch meta-harness/meta_harness/harness/__init__.py
touch meta-harness/meta_harness/harness/templates/baseline/__init__.py
touch meta-harness/meta_harness/benchmark/__init__.py
touch meta-harness/meta_harness/trace/__init__.py
touch meta-harness/tests/__init__.py
touch meta-harness/tests/conftest.py
```

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add .
git commit -m "chore: project scaffolding for meta-harness"
```

---

## Task 2: TraceStore

**Files:**
- Create: `meta-harness/meta_harness/trace/store.py`
- Create: `meta-harness/tests/test_trace_store.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_trace_store.py -v
```

Expected: FAIL with ImportError or NameError for TraceStore.

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_trace_store.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/trace/store.py tests/test_trace_store.py
git commit -m "feat: TraceStore with save, load, get_best, and diff generation"
```

---

## Task 3: Harness Validator

**Files:**
- Create: `meta-harness/meta_harness/harness/validator.py`
- Create: `meta-harness/tests/test_harness_validator.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_harness_validator.py -v
```

Expected: FAIL with ImportError for HarnessValidator.

- [ ] **Step 3: Write minimal implementation**

```python
import ast
from pathlib import Path


class HarnessValidator:
    DANGEROUS_CALLS = {"eval", "exec", "compile"}

    def __init__(self, allowed_tools: set[str] | None = None):
        self.allowed_tools = allowed_tools

    def validate(self, harness_path: Path) -> list[str]:
        errors = []
        tools_file = harness_path / "tools.py"
        if not tools_file.exists():
            errors.append("Missing tools.py")
            return errors

        with open(tools_file) as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            errors.append(f"Syntax error in tools.py: {e}")
            return errors

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in self.DANGEROUS_CALLS:
                    errors.append(f"Dangerous function call: {func.id}")
                elif isinstance(func, ast.Attribute) and func.attr in self.DANGEROUS_CALLS:
                    errors.append(f"Dangerous function call: {func.attr}")

        return errors
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_harness_validator.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/harness/validator.py tests/test_harness_validator.py
git commit -m "feat: HarnessValidator with AST safety checks"
```

---

## Task 4: Baseline Harness Templates

**Files:**
- Create: `meta-harness/meta_harness/harness/templates/baseline/system_prompt.md`
- Create: `meta-harness/meta_harness/harness/templates/baseline/tools.py`
- Create: `meta-harness/meta_harness/harness/templates/baseline/context_manager.py`
- Create: `meta-harness/meta_harness/harness/templates/baseline/stop_conditions.py`
- Create: `meta-harness/meta_harness/harness/templates/baseline/agent.py`

- [ ] **Step 1: Create system_prompt.md**

```markdown
You are an expert terminal agent. You have access to tools to interact with the filesystem and execute commands.
Your goal is to complete the given task.
Think step by step. Use tools when needed.
When you believe the task is complete, call the submit tool with your final answer.
```

- [ ] **Step 2: Create tools.py**

```python
import subprocess


def execute_command(command: str) -> str:
    """Execute a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr


def read_file(path: str) -> str:
    """Read the contents of a file."""
    with open(path) as f:
        return f.read()


def submit(answer: str) -> dict:
    """Submit the final answer."""
    return {"action": "submit", "answer": answer}
```

- [ ] **Step 3: Create context_manager.py**

```python
import pathlib


class ContextManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def build_context(self, task: str, history: list[dict]) -> list[dict]:
        messages = [
            {"role": "system", "content": self._load_system_prompt()},
            {"role": "user", "content": task},
        ]
        for entry in history:
            if isinstance(entry, dict) and "content" in entry:
                messages.append({"role": "assistant", "content": entry["content"]})
            else:
                messages.append({"role": "assistant", "content": str(entry)})
        return messages

    def _load_system_prompt(self) -> str:
        path = pathlib.Path(__file__).parent / "system_prompt.md"
        with open(path) as f:
            return f.read()
```

- [ ] **Step 4: Create stop_conditions.py**

```python
class StopConditions:
    def __init__(self, max_steps: int = 20):
        self.max_steps = max_steps

    def should_stop(self, history: list[dict]) -> bool:
        if not history:
            return False
        last = history[-1]
        if isinstance(last, dict) and last.get("action") == "submit":
            return True
        if len(history) >= self.max_steps:
            return True
        return False
```

- [ ] **Step 5: Create agent.py**

```python
from .context_manager import ContextManager
from .stop_conditions import StopConditions
from .tools import execute_command, read_file, submit


class Agent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.tools = {
            "execute_command": execute_command,
            "read_file": read_file,
            "submit": submit,
        }
        self.context_manager = ContextManager()
        self.stop_conditions = StopConditions()

    def run(self, task: str) -> dict:
        history = []
        while not self.stop_conditions.should_stop(history):
            context = self.context_manager.build_context(task, history)
            response = self.llm_client.complete(context, tools=self.tools)
            history.append(response)
        return {"history": history, "answer": self._extract_answer(history)}

    def _extract_answer(self, history: list[dict]) -> str:
        for entry in reversed(history):
            if isinstance(entry, dict) and entry.get("action") == "submit":
                return entry.get("answer", "")
        return ""
```

- [ ] **Step 6: Commit**

```bash
cd meta-harness
git add meta_harness/harness/templates/baseline/
git commit -m "feat: baseline harness templates with agent, tools, context manager, and stop conditions"
```

---

## Task 5: Harness Runtime

**Files:**
- Create: `meta-harness/meta_harness/harness/runtime.py`
- Create: `meta-harness/tests/test_harness_runtime.py`

- [ ] **Step 1: Write the failing test**

```python
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.harness.runtime import HarnessRuntime


class TestHarnessRuntime:
    def test_run_loads_and_executes_agent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            (harness / "__init__.py").write_text("")
            (harness / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    def run(self, task: str):
        return {"answer": "42", "history": [{"content": "done"}]}
''')
            (harness / "system_prompt.md").write_text("You are an agent.")
            (harness / "tools.py").write_text("def execute_command(cmd): pass\n")
            (harness / "context_manager.py").write_text("class ContextManager: pass\n")
            (harness / "stop_conditions.py").write_text("class StopConditions: pass\n")

            runtime = HarnessRuntime(harness)
            mock_llm = MagicMock()
            result = runtime.run("What is 6*7?", mock_llm)

            assert result["answer"] == "42"
            assert len(result["history"]) == 1
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_harness_runtime.py -v
```

Expected: FAIL with ImportError for HarnessRuntime.

- [ ] **Step 3: Write minimal implementation**

```python
import importlib.util
import sys
from pathlib import Path


class HarnessRuntime:
    def __init__(self, harness_path: str | Path):
        self.harness_path = Path(harness_path)

    def run(self, task: str, llm_client) -> dict:
        agent_path = self.harness_path / "agent.py"
        if not agent_path.exists():
            raise FileNotFoundError(f"agent.py not found in {self.harness_path}")

        module_name = f"meta_harness_dynamic_agent_{self.harness_path.name}"
        spec = importlib.util.spec_from_file_location(module_name, agent_path)
        module = importlib.util.module_from_spec(spec)

        # Temporarily add harness path for imports
        sys.path.insert(0, str(self.harness_path))
        try:
            spec.loader.exec_module(module)
            agent = module.Agent(llm_client)
            return agent.run(task)
        finally:
            sys.path.pop(0)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_harness_runtime.py -v
```

Expected: Test PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/harness/runtime.py tests/test_harness_runtime.py
git commit -m "feat: HarnessRuntime dynamic loading and execution"
```

---

## Task 6: Benchmark Adapter Base + TerminalBench Adapter

**Files:**
- Create: `meta-harness/meta_harness/benchmark/base.py`
- Create: `meta-harness/meta_harness/benchmark/terminalbench.py`
- Create: `meta-harness/tests/test_benchmark_adapter.py`

- [ ] **Step 1: Write the failing test for base adapter**

```python
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from meta_harness.benchmark.terminalbench import TerminalBenchAdapter


class TestBenchmarkAdapter:
    def test_load_tasks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks = [{"id": "t1"}, {"id": "t2"}]
            task_file = Path(tmpdir) / "test.json"
            with open(task_file, "w") as f:
                json.dump(tasks, f)

            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command="echo '{}' ")
            loaded = adapter.load_tasks(split="test")
            assert len(loaded) == 2
            assert loaded[0]["id"] == "t1"

    def test_evaluate_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tasks = [{"id": "t1"}]
            task_file = Path(tmpdir) / "test.json"
            with open(task_file, "w") as f:
                json.dump(tasks, f)

            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command="echo '{\"success\": true, \"trace\": {}, \"tokens\": 100}'")
            harness = Path(tmpdir) / "harness"
            harness.mkdir()
            result = adapter.evaluate("t1", harness)
            assert result["success"] is True
            assert result["tokens"] == 100

    def test_score(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adapter = TerminalBenchAdapter(task_dir=Path(tmpdir), command="echo")
            results = [
                {"success": True, "tokens": 100},
                {"success": False, "tokens": 200},
                {"success": True, "tokens": 150},
            ]
            scores = adapter.score(results)
            assert scores["accuracy"] == 2 / 3
            assert scores["passed"] == 2
            assert scores["total"] == 3
            assert scores["mean_tokens"] == 150.0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_benchmark_adapter.py -v
```

Expected: FAIL with ImportError.

- [ ] **Step 3: Implement base adapter and TerminalBench adapter**

```python
# meta_harness/benchmark/base.py
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
```

```python
# meta_harness/benchmark/terminalbench.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_benchmark_adapter.py -v
```

Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/benchmark/base.py meta_harness/benchmark/terminalbench.py tests/test_benchmark_adapter.py
git commit -m "feat: BenchmarkAdapter base and TerminalBench adapter"
```

---

## Task 7: Convergence Tracker

**Files:**
- Create: `meta-harness/meta_harness/loop/convergence.py`
- Create: `meta-harness/tests/test_convergence.py`

- [ ] **Step 1: Write the failing test**

```python
import random
from unittest.mock import MagicMock

import pytest

from meta_harness.loop.convergence import ConvergenceTracker


class TestConvergenceTracker:
    def test_should_stop_after_patience(self):
        tracker = ConvergenceTracker(patience=3, subset_size=5)
        tracker.should_stop({"accuracy": 0.5}, 0)
        tracker.should_stop({"accuracy": 0.5}, 1)
        tracker.should_stop({"accuracy": 0.5}, 2)
        assert tracker.should_stop({"accuracy": 0.5}, 3) is True

    def test_should_not_stop_if_improving(self):
        tracker = ConvergenceTracker(patience=3, subset_size=5)
        tracker.should_stop({"accuracy": 0.5}, 0)
        tracker.should_stop({"accuracy": 0.6}, 1)
        tracker.should_stop({"accuracy": 0.7}, 2)
        assert tracker.should_stop({"accuracy": 0.7}, 3) is False

    def test_should_stop_at_max_iterations(self):
        tracker = ConvergenceTracker(patience=10, subset_size=5, max_iterations=5)
        tracker.should_stop({"accuracy": 0.5}, 0)
        tracker.should_stop({"accuracy": 0.5}, 1)
        tracker.should_stop({"accuracy": 0.5}, 2)
        tracker.should_stop({"accuracy": 0.5}, 3)
        assert tracker.should_stop({"accuracy": 0.5}, 4) is True

    def test_get_tasks_returns_subset(self):
        tracker = ConvergenceTracker(patience=3, subset_size=2)
        mock_adapter = MagicMock()
        mock_adapter.load_tasks.return_value = [{"id": f"t{i}"} for i in range(10)]
        tasks = tracker.get_tasks(mock_adapter)
        assert len(tasks) == 2
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_convergence.py -v
```

Expected: FAIL with ImportError.

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_convergence.py -v
```

Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/loop/convergence.py tests/test_convergence.py
git commit -m "feat: ConvergenceTracker with patience and max_iterations"
```

---

## Task 8: MetaAgent Prompt Builder

**Files:**
- Create: `meta-harness/meta_harness/meta_agent/prompt_builder.py`
- Create: `meta-harness/tests/test_meta_agent.py`

- [ ] **Step 1: Write the failing test**

```python
import json
import tempfile
from pathlib import Path

import pytest

from meta_harness.meta_agent.prompt_builder import PromptBuilder
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_meta_agent.py -v
```

Expected: FAIL with ImportError.

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_meta_agent.py::TestPromptBuilder -v
```

Expected: Both tests PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/meta_agent/prompt_builder.py tests/test_meta_agent.py
git commit -m "feat: MetaAgent PromptBuilder with harness code and failure traces"
```

---

## Task 9: MetaAgent Proposer

**Files:**
- Create: `meta-harness/meta_harness/meta_agent/proposer.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_meta_agent.py`:

```python
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.meta_agent.proposer import MetaAgent
from meta_harness.meta_agent.prompt_builder import PromptBuilder
from meta_harness.trace.store import TraceStore


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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_meta_agent.py::TestMetaAgent -v
```

Expected: FAIL with ImportError for MetaAgent.

- [ ] **Step 3: Write minimal implementation**

```python
import re
import tempfile
from pathlib import Path

from meta_harness.meta_agent.prompt_builder import PromptBuilder
from meta_harness.trace.store import TraceStore


class MetaAgent:
    def __init__(self, llm_client, prompt_builder: PromptBuilder | None = None):
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder or PromptBuilder()

    def propose(self, trace_store: TraceStore, current_iter: int) -> Path:
        prompt = self.prompt_builder.build(trace_store, current_iter)
        response = self.llm_client.complete([{"role": "user", "content": prompt}])
        content = response.get("content", "")
        files = self._parse_files(content)

        # Write to temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix=f"meta_harness_{current_iter}_"))
        for filename, file_content in files.items():
            file_path = temp_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(file_content)
        return temp_dir

    def _parse_files(self, content: str) -> dict[str, str]:
        files = {}
        pattern = r"###\s*FILE:\s*(.+?)\n(.*?)(?=###\s*FILE:|\Z)"
        matches = re.findall(pattern, content, re.DOTALL)
        for filename, file_content in matches:
            files[filename.strip()] = file_content.strip()
        return files
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_meta_agent.py::TestMetaAgent -v
```

Expected: Test PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/meta_agent/proposer.py tests/test_meta_agent.py
git commit -m "feat: MetaAgent proposer with file parsing and temp harness generation"
```

---

## Task 10: OptimizerLoop

**Files:**
- Create: `meta-harness/meta_harness/loop/optimizer.py`
- Create: `meta-harness/tests/test_optimizer.py`

- [ ] **Step 1: Write the failing test**

```python
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from meta_harness.loop.optimizer import OptimizerLoop


class TestOptimizerLoop:
    def test_single_iteration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "traces": {"root": str(Path(tmpdir) / "traces")},
                "loop": {"max_iterations": 1, "patience": 5, "subset_size": 2},
                "benchmark": {"name": "dummy", "task_dir": str(tmpdir), "command": "echo"},
            }

            # Create fake tasks file
            import json
            with open(Path(tmpdir) / "test.json", "w") as f:
                json.dump([{"id": "t1"}, {"id": "t2"}], f)

            # Create fake baseline harness
            baseline = Path(tmpdir) / "baseline"
            baseline.mkdir()
            (baseline / "__init__.py").write_text("")
            (baseline / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client): pass
    def run(self, task: str):
        return {"answer": "done", "history": []}
''')
            (baseline / "system_prompt.md").write_text("You are an agent.")
            (baseline / "tools.py").write_text("def execute_command(cmd): pass\n")
            (baseline / "context_manager.py").write_text("class ContextManager: pass\n")
            (baseline / "stop_conditions.py").write_text("class StopConditions: pass\n")

            loop = OptimizerLoop(config, baseline_harness=baseline)

            # Mock the adapter to return success
            loop.adapter.evaluate = MagicMock(return_value={"success": True, "trace": {}, "tokens": 50})

            loop.run()

            assert loop.trace_store.root.exists()
            assert (loop.trace_store.root / "iter_000" / "scores.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd meta-harness
pytest tests/test_optimizer.py -v
```

Expected: FAIL with ImportError.

- [ ] **Step 3: Write minimal implementation**

```python
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
        self.adapter = TerminalBenchAdapter(
            task_dir=Path(config["benchmark"]["task_dir"]),
            command=config["benchmark"].get("command"),
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd meta-harness
pytest tests/test_optimizer.py -v
```

Expected: Test PASS.

- [ ] **Step 5: Commit**

```bash
cd meta-harness
git add meta_harness/loop/optimizer.py tests/test_optimizer.py
git commit -m "feat: OptimizerLoop orchestrating evaluate-save-propose cycle"
```

---

## Task 11: Entry Point (run.py)

**Files:**
- Create: `meta-harness/run.py`

- [ ] **Step 1: Create run.py**

```python
#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import yaml

from meta_harness.loop.optimizer import OptimizerLoop
from meta_harness.meta_agent.proposer import MetaAgent


def create_llm_client(provider: str, model: str, config: dict):
    if provider == "nim":
        from openai import OpenAI
        api_key = os.environ.get(config.get("api_key_env", "NVIDIA_NIM_API_KEY"))
        return OpenAI(api_key=api_key, base_url=config.get("base_url"))
    elif provider == "ollama":
        import ollama
        return ollama
    else:
        raise ValueError(f"Unknown provider: {provider}")


def main():
    parser = argparse.ArgumentParser(description="Meta-Harness Optimizer")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--baseline", default=None, help="Path to baseline harness")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    baseline = Path(args.baseline) if args.baseline else None
    loop = OptimizerLoop(config, baseline_harness=baseline)

    meta_config = config["models"]["meta_agent"]
    llm_client = create_llm_client(
        meta_config["provider"],
        meta_config["model"],
        meta_config,
    )
    meta_agent = MetaAgent(llm_client=llm_client)
    loop.set_meta_agent(meta_agent)

    loop.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
cd meta-harness
git add run.py
git commit -m "feat: entry point script with config loading and LLM client factory"
```

---

## Task 12: Integration Smoke Test

**Files:**
- Create: `meta-harness/tests/test_integration.py`

- [ ] **Step 1: Write integration smoke test**

```python
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from meta_harness.loop.optimizer import OptimizerLoop
from meta_harness.meta_agent.proposer import MetaAgent


class TestIntegration:
    def test_full_loop_with_mock_llm(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup tasks
            with open(Path(tmpdir) / "test.json", "w") as f:
                json.dump([{"id": "t1"}], f)

            # Setup baseline harness
            baseline = Path(tmpdir) / "baseline"
            baseline.mkdir()
            (baseline / "__init__.py").write_text("")
            (baseline / "agent.py").write_text('''
class Agent:
    def __init__(self, llm_client): pass
    def run(self, task: str):
        return {"answer": "42", "history": []}
''')
            (baseline / "system_prompt.md").write_text("You are an agent.")
            (baseline / "tools.py").write_text("def execute_command(cmd): pass\n")
            (baseline / "context_manager.py").write_text("class ContextManager: pass\n")
            (baseline / "stop_conditions.py").write_text("class StopConditions: pass\n")

            config = {
                "traces": {"root": str(Path(tmpdir) / "traces")},
                "loop": {"max_iterations": 2, "patience": 5, "subset_size": 1},
                "benchmark": {"name": "dummy", "task_dir": str(tmpdir), "command": "echo"},
            }

            loop = OptimizerLoop(config, baseline_harness=baseline)
            loop.adapter.evaluate = MagicMock(return_value={"success": True, "trace": {}, "tokens": 50})

            mock_llm = MagicMock()
            mock_llm.complete.return_value = {
                "content": (
                    "### FILE: agent.py\n"
                    "class Agent:\n"
                    "    def __init__(self, llm_client): pass\n"
                    "    def run(self, task: str):\n"
                    "        return {'answer': '42', 'history': []}\n"
                )
            }

            meta_agent = MetaAgent(llm_client=mock_llm)
            loop.set_meta_agent(meta_agent)

            loop.run()

            # Verify traces were saved
            assert (loop.trace_store.root / "iter_000" / "scores.json").exists()
            assert (loop.trace_store.root / "iter_001" / "scores.json").exists()
```

- [ ] **Step 2: Run integration test**

```bash
cd meta-harness
pytest tests/test_integration.py -v
```

Expected: Test PASS.

- [ ] **Step 3: Commit**

```bash
cd meta-harness
git add tests/test_integration.py
git commit -m "test: integration smoke test for full optimization loop"
```

---

## Spec Coverage Check

| Spec Section | Task(s) | Notes |
|---|---|---|
| TraceStore (save, load, get_best, diff) | Task 2 | Fully covered |
| BenchmarkAdapter (load_tasks, evaluate, score) | Task 6 | Fully covered |
| Harness (templates, runtime, validator) | Tasks 3, 4, 5 | Fully covered |
| MetaAgent (proposer, prompt_builder) | Tasks 8, 9 | Fully covered |
| OptimizerLoop (orchestrator) | Task 10 | Fully covered |
| Convergence (patience, subset) | Task 7 | Fully covered |
| Config + Entry Point | Task 1, 11 | Fully covered |
| Testing strategy | All tasks + Task 12 | TDD for each component + integration smoke test |

## Placeholder Scan

- No "TBD", "TODO", or "implement later" found.
- All code blocks contain complete, runnable code.
- All tests include assertions.
- All file paths are exact.
- All commands have expected outputs specified.

## Type Consistency Check

- `TraceStore.save()` signature matches usage in `OptimizerLoop` and tests.
- `BenchmarkAdapter.evaluate()` signature matches usage in `TerminalBenchAdapter` and tests.
- `HarnessRuntime.run()` signature matches usage in tests.
- `MetaAgent.propose()` returns `Path`, consistent with `HarnessValidator.validate()` input.
- `ConvergenceTracker.should_stop()` accepts `dict` scores, consistent with `BenchmarkAdapter.score()` output.

All types consistent across tasks.

---

**Plan complete and saved to `docs/superpowers/plans/2026-04-21-meta-harness.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using `executing-plans`, batch execution with checkpoints for review.

Which approach do you want?
