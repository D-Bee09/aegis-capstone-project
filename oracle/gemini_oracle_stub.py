# oracle/gemini_oracle_stub.py
class GeminiOracle:
    """
    Stub: In real deployment this calls Gemini model.
    """

    def analyze(self, report, vitals, severity_score, trend, specialists):
        ward = "ICU" if severity_score >= 8 else "HDU"

        return {
            "ward": ward,
            "severity_score": severity_score,
            "trend": trend,
            "specialists_required": specialists,
            "notes": "LLM Oracle Stub Response"
        }
