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
