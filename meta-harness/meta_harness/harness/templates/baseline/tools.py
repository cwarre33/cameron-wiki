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
