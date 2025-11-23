# hospital_sim.py
from flask import Flask, request, jsonify
import time
import json
import os

app = Flask(__name__)
LOG_FILE = "hospital_logs.json"

def log_entry(entry):
    """Append hospital response logs for session history"""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def pick_ward(severity_score, injury_description=""):
    """Basic triage logic"""
    if "burn" in injury_description.lower():
        return "BURN WARD"
    if severity_score >= 8:
        return "ICU"
    if 5 <= severity_score < 8:
        return "HDU"
    return "TRAUMA WARD"

@app.route("/handoff", methods=["POST"])
def handoff():
    data = request.json or {}
    timestamp = int(time.time())
    
    injury_description = data.get("injury_description", "")
    severity_score = data.get("severity_score", 7)
    
    # Use specialists sent by AEGIS
    specialists_from_aegis = data.get("specialists_required", [])
    
    assigned_ward = pick_ward(severity_score, injury_description)
    
    # Format specialists with mobilization status
    specialists_out = []
    for idx, spec in enumerate(specialists_from_aegis):
        specialists_out.append({
            "specialty": spec,
            "status": "MOBILIZED",
            "eta_minutes": 3 + idx
        })
    
    response = {
        "status": "CONFIRMED",
        "timestamp": timestamp,
        "case_id": f"SIM_{timestamp}",
        "assigned_ward": assigned_ward,
        "injury_description": injury_description,
        "specialists": specialists_out,
        "notes": "Hospital team mobilized per AEGIS recommendations."
    }
    
    log_entry(response)
    return jsonify(response), 200

if __name__ == "__main__":
    print("🏥 Hospital Simulation Server Running at http://127.0.0.1:5001/handoff")
    app.run(port=5001)
