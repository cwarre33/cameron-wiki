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
