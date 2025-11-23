# hospital_sim.py
from flask import Flask, request, jsonify
import time

app = Flask(__name__)


@app.route("/handoff", methods=["POST"])
def handoff():
    data = request.json or {}

    specialists = data.get("specialists_required", [])
    out = []

    for spec in specialists:
        out.append({
            "specialty": spec,
            "status": "CONFIRMED",
            "eta_minutes": 5 + len(out)
        })

    return jsonify({
        "status": "CONFIRMED",
        "case_id": f"SIM_{int(time.time())}",
        "assigned_ward": data.get("ward", "ICU"),
        "specialists": out
    })


if __name__ == "__main__":
    app.run(port=5001)
