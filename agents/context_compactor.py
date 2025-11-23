# agents/context_compactor.py
class ContextCompactor:
    """
    Analyzes vitals & compresses long history into a trend summary.
    """

    def summarize(self, vitals_list):
        if not vitals_list:
            return "No vitals yet."

        bp_values = [v["bp_systolic"] for v in vitals_list if "bp_systolic" in v]
        hr_values = [v["hr"] for v in vitals_list if "hr" in v]
        spo2_values = [v["spo2"] for v in vitals_list if "spo2" in v]

        def trend(values):
            if len(values) < 2:
                return "stable"
            if values[-1] > values[0]:
                return "rising"
            if values[-1] < values[0]:
                return "falling"
            return "stable"

        return {
            "bp_trend": trend(bp_values),
            "hr_trend": trend(hr_values),
            "spo2_trend": trend(spo2_values)
        }
