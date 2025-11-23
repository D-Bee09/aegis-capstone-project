# core/sessions.py
import json
import os
from datetime import datetime, timezone


class InMemorySessionService:
    """
    Stores session messages and events for the duration of the run.
    """

    def __init__(self):
        self.session = []

    def add_event(self, event_type, payload):
        entry = {
            "type": event_type,
            "payload": payload,
            "ts": datetime.now(timezone.utc).isoformat()
        }
        self.session.append(entry)
        return entry

    def get_history(self):
        return self.session[:]


class MemoryBank:
    """
    Persists important events to memory_bank.json.
    """

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def save(self, event_type, payload):
        entry = {
            "type": event_type,
            "payload": payload,
            "ts": datetime.now(timezone.utc).isoformat()
        }

        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

        return entry
