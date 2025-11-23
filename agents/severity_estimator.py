# agents/severity_estimator.py
class SeverityEstimator:
    """
    A simple ML stub scoring trauma severity.
    """

    def estimate(self, vitals):
        hr = vitals.get("hr", 90)
        bp = vitals.get("bp_systolic", 120)
        spo2 = vitals.get("spo2", 98)

        shock_index = hr / max(bp, 1)

        score = 3

        if shock_index > 1.0:
            score = 5
        if shock_index > 1.3:
            score = 7
        if bp < 90 or spo2 < 92 or shock_index > 1.5:
            score = 9

        return score
