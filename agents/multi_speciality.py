# agents/multi_specialty.py
class MultiSpecialityCoordinator:
    """
    Assigns medical specialists based on injury description + vitals.
    """

    def assign_specialists(self, report: str, vitals: dict):
        report = report.lower()
        specialists = []

        if "burn" in report:
            specialists.append("Burns Specialist")

        if "head" in report or "skull" in report:
            specialists.append("Neurosurgeon")

        if "chest" in report or "rib" in report:
            specialists.append("Cardiothoracic Surgeon")

        if "leg" in report or "fracture" in report:
            specialists.append("Orthopedic Surgeon")

        if "trauma" in report or "fall" in report:
            specialists.append("Trauma Surgeon")

        specialists.append("Emergency Physician")
        specialists.append("Anesthesiologist")

        # Remove duplicates
        return list(dict.fromkeys(specialists))
