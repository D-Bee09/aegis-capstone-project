from flask import Flask, request, jsonify
import time
import random
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


def assign_specialists(injury_description=""):
     # Add anesthesiologist for severe cases
    def needs_anesthesiologist(severity_score, vitals, injury_description):

    # Condition 1: Severe trauma
    if severity_score >= 8:
        return True

    # Condition 2: Respiratory compromise
    desc = injury_description.lower()
    if ("paradoxical" in desc or 
        "respiratory distress" in desc or 
        "flail chest" in desc or 
        "collapsed lung" in desc):
        return True

    # Condition 3: Vitals-based
    if vitals:
        bp = vitals.get("bp", 100)
        hr = vitals.get("hr", 100)
        shock_index = hr / max(bp, 1)
        if bp < 90 and hr > 120:
            return True
        if shock_index >= 1.0:
            return True

    # Condition 4: Surgery likely
    surg_keywords = ["fracture", "open wound", "penetrating", "thoracic", "severe bleeding"]
    if any(kw in desc for kw in surg_keywords):
        return True

    return False

    """Choose specialists based on injury type"""
    specialists = []

    desc = injury_description.lower()

    if "chest" in desc or "thorax" in desc:
        specialists.append("Cardiothoracic Surgeon")

    if "head" in desc or "brain" in desc:
        specialists.append("Neurosurgeon")

    if "fracture" in desc or "limb" in desc:
        specialists.append("Orthopedic Surgeon")

    if "burn" in desc:
        specialists.append("Burn Specialist")

    # Always activate trauma surgeon
    specialists.append("Trauma Surgeon")
    if needs_anesthesiologist(severity_score, vitals, injury_description):
        specialists.append("Anasthesiologist")


    return specialists


@app.route("/handoff", methods=["POST"])
def handoff():
    data = request.json or {}
    timestamp = int(time.time())

    injury_description = data.get("injury_description", "")
    severity_score = data.get("severity_score", 7)

    # Pick ward based on logic
    assigned_ward = pick_ward(severity_score, injury_description)

    # Assign specialists
    specialists_needed = assign_specialists(injury_description)

    specialists_out = []
    for idx, spec in enumerate(specialists_needed):
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
        "notes": "Hospital ICU/HDU/Trauma team mobilized."
    }

    # Log for history
    log_entry(response)

    return jsonify(response), 200


if __name__ == "__main__":
    print("🏥 Hospital Simulation Server Running at http://127.0.0.1:5001/handoff")
    app.run(port=5001)
