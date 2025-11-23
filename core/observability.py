# core/observability.py
import time
from datetime import datetime, timezone


class Metrics:
    """
    Tracks counters and timings for AEGIS observability.
    """

    def __init__(self):
        self.counters = {}
        self.timers = {}

    def count(self, key):
        self.counters[key] = self.counters.get(key, 0) + 1

    def start(self, key):
        self.timers[key] = time.perf_counter()

    def stop(self, key):
        if key in self.timers:
            elapsed = time.perf_counter() - self.timers[key]
            self.timers[key] = elapsed
            return elapsed
        return None

    def export(self):
        return {
            "time": datetime.now(timezone.utc).isoformat(),
            "counters": self.counters,
            "timers": self.timers
        }
