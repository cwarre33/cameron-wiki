"""
Patch for TerminalBench Windows compatibility.

The issue: TerminalBench uses pathlib.Path for container paths, which on Windows
produces backslash separators (\\tmp instead of /tmp). Docker containers expect
Unix-style forward slashes.
"""

from pathlib import PurePosixPath


def apply_patch():
    """Apply Windows path compatibility patches to TerminalBench."""
    try:
        from terminal_bench.terminal import tmux_session
        from terminal_bench.terminal import docker_compose_manager

        # Patch 1: Fix TmuxSession container path
        tmux_session.TmuxSession._GET_ASCIINEMA_TIMESTAMP_SCRIPT_CONTAINER_PATH = PurePosixPath(
            "/tmp/get-asciinema-timestamp.sh"
        )

        # Patch 2: Fix DockerComposeManager container test dir
        docker_compose_manager.DockerComposeManager.CONTAINER_TEST_DIR = PurePosixPath("/tests")

        return True
    except Exception as e:
        print(f"Warning: Could not apply TerminalBench patch: {e}")
        return False
