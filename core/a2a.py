# core/a2a.py
import json, os
from dataclasses import dataclass
from datetime import datetime, timezone

A2A_LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'a2a_logs.json'))


@dataclass
class A2AMessage:
    from_agent: str
    to_agent: str
    payload: dict
    trace_id: str

    def to_dict(self):
        return {
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "trace_id": self.trace_id,
            "payload": self.payload,
            "ts": datetime.now(timezone.utc).isoformat()
        }


class A2ARouter:
    def __init__(self):
        self.routes = {}

    def register(self, name, client):
        self.routes[name] = client

    def _log_message(self, message: A2AMessage, result):
        entry = message.to_dict()
        entry["result"] = result

        try:
            if not os.path.exists(A2A_LOG_PATH):
                with open(A2A_LOG_PATH, "w") as f:
                    json.dump([], f)

            with open(A2A_LOG_PATH, "r") as f:
                data = json.load(f)
        except Exception:
            data = []

        data.append(entry)

        try:
            with open(A2A_LOG_PATH, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def send(self, message: A2AMessage, target_client=None):
        client = target_client or self.routes.get(message.to_agent)

        if client:
            try:
                result = client.handoff(message.payload)
                self._log_message(message, result)
                return result
            except Exception as e:
                err = {"error": str(e)}
                self._log_message(message, err)
                return err

        err = {"error": "no target client"}
        self._log_message(message, err)
        return err
