#!/usr/bin/env python3
"""Wrapper script that applies Windows path patch before running TerminalBench."""

import sys

# Apply Windows compatibility patch BEFORE importing TerminalBench
from meta_harness.benchmark.terminalbench_patch import apply_patch
apply_patch()

# Now import and run TerminalBench CLI
from terminal_bench.cli.tb.main import app
from typer.main import get_command

if __name__ == "__main__":
    # Get the Click command from Typer app and invoke it
    command = get_command(app)
    sys.exit(command())
