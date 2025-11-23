# aegis_main.py
import time, uuid, json, os

from agents.asr_agent import ASRAgent
from agents.tts_agent import TTSAgent
from agents.context_compactor import ContextCompactor
from agents.multi_speciality import MultiSpecialityCoordinator
from agents.severity_estimator import SeverityEstimator

from core.sessions import InMemorySessionService, MemoryBank
from core.observability import Metrics
from core.a2a import A2AMessage, A2ARouter

from oracle.gemini_oracle_stub import GeminiOracle
from tools.openapi_client import HospitalOpenAPIClient


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class AEGIS:
    def __init__(self):
        # Agents
        self.asr = ASRAgent()
        self.tts = TTSAgent()
        self.compactor = ContextCompactor()
        self.specialty = MultiSpecialityCoordinator()
        self.severity = SeverityEstimator()
        self.oracle = GeminiOracle()

        # Memory systems
        self.session = InMemorySessionService()
        self.memory_bank = MemoryBank(os.path.join(PROJECT_ROOT, "memory_bank.json"))

        # Observability
        self.metrics = Metrics()

        # A2A
        self.router = A2ARouter()
        self.hospital_client = HospitalOpenAPIClient("http://127.0.0.1:5001")
        self.router.register("HospitalAI", self.hospital_client)

        # Data buffers
        self.vitals_history = []
        self.last_analysis = None

    # ------------------------------------------------------
    # Vitals ingestion (mock)
    # ------------------------------------------------------
    def ingest_vitals(self):
        """
        Replace with real serial/IoT input.
        """
        import random
        return {
            "hr": random.randint(80, 150),
            "bp_systolic": random.randint(70, 140),
            "spo2": random.randint(85, 99)
        }

    # ------------------------------------------------------
    # Main analysis pipeline
    # ------------------------------------------------------
    def analyze_patient(self, report):
        # Log report
        self.session.add_event("paramedic_report", report)
        self.memory_bank.save("paramedic_report", report)

        # Severity
        current_vitals = self.vitals_history[-1]
        severity = self.severity.estimate(current_vitals)

        # Trend
        trend = self.compactor.summarize(self.vitals_history)

        # Specialists
        specialists = self.specialty.assign_specialists(report, current_vitals)

        # Oracle
        oracle_out = self.oracle.analyze(
            report=report,
            vitals=current_vitals,
            severity_score=severity,
            trend=trend,
            specialists=specialists
        )

        self.last_analysis = oracle_out

        # Save for dashboard
        with open(os.path.join(PROJECT_ROOT, "last_analysis.json"), "w") as f:
            json.dump(oracle_out, f, indent=2)

        # A2A to hospital
        msg = A2AMessage(
            from_agent="AEGIS",
            to_agent="HospitalAI",
            payload=oracle_out,
            trace_id=str(uuid.uuid4())
        )

        response = self.router.send(msg, target_client=self.hospital_client)
        self.memory_bank.save("hospital_response", response)

        # Announce
        self.tts.speak(
            f"Hospital notified. Ward {oracle_out['ward']} confirmed recommendation."
        )

        return oracle_out, response

    # ------------------------------------------------------
    # Main operational loop
    # ------------------------------------------------------
    def run(self, duration=20):
        print("AEGIS system running...")
        start = time.time()

        while time.time() - start < duration:
            vitals = self.ingest_vitals()
            self.vitals_history.append(vitals)

            self.session.add_event("vitals", vitals)
            self.memory_bank.save("vitals", vitals)

            print("Vitals:", vitals)

            time.sleep(1)

        # Trigger analysis after vitals window
        paramedic_input = "Patient fell from a height with suspected chest trauma."
        return self.analyze_patient(paramedic_input)


if __name__ == "__main__":
    aegis = AEGIS()
    final, hospital = aegis.run(10)
    print("FINAL AEGIS ANALYSIS:\n", final)
    print("HOSPITAL RESPONSE:\n", hospital)
