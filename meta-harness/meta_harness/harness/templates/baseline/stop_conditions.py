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
