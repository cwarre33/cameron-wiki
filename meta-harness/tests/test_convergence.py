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
