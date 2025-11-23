# web/dashboard.py
from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path

app = Flask(__name__, template_folder="templates", static_folder="static")
BASE = Path(__file__).resolve().parents[1]

A2A_LOG = BASE / "a2a_logs.json"
MEMORY_BANK = BASE / "memory_bank.json"
LAST_ANALYSIS = BASE / "last_analysis.json"


def _load_json(path: Path):
    try:
        if path.exists():
            return json.loads(path.read_text())
        return []
    except:
        return []


@app.route("/")
def index():
    a2a = _load_json(A2A_LOG)
    memory = _load_json(MEMORY_BANK)
    last = _load_json(LAST_ANALYSIS) if LAST_ANALYSIS.exists() else None
    return render_template(
        "index.html",
        a2a_logs=a2a[::-1],
        memory=memory[::-1],
        last_analysis=last
    )


@app.route("/api/a2a")
def api_a2a():
    return jsonify(_load_json(A2A_LOG)[::-1])


@app.route("/api/last")
def api_last():
    return jsonify(_load_json(LAST_ANALYSIS))


@app.route("/api/memory")
def api_memory():
    return jsonify(_load_json(MEMORY_BANK)[::-1])


@app.route("/api/replay", methods=["POST"])
def api_replay():
    data = request.get_json() or {}
    return jsonify({"status": "ok", "replayed": data})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
