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
