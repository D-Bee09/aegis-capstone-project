# aegis_main.py
import time, uuid, json, os

from agents.asr_agent import ASRAgent
from agents.tts_agent import TTSAgent
from agents.context_compactor import ContextCompactor
from agents.multi_speciality import MultiSpecialityCoordinator
from agents.severity_estimator import SeverityEstimator
from agents.paramedic_guidance_agent import ParamedicGuidanceAgent

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
        self.tts = TTSAgent(mode="offline")
        self.compactor = ContextCompactor()
        self.specialty = MultiSpecialityCoordinator()
        self.severity = SeverityEstimator()
        self.oracle = GeminiOracle()
        self.guidance = ParamedicGuidanceAgent()

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

    def ingest_vitals(self):
        """Mock vitals - replace with real IoT."""
        import random
        return {
            "hr": random.randint(130, 160),
            "bp_systolic": random.randint(70, 95),
            "spo2": random.randint(84, 92)
        }

    def display_visual_status(self, vitals, severity_score, trend):
        """Display visual patient status."""
        hr = vitals.get("hr", 0)
        bp = vitals.get("bp_systolic", 0)
        spo2 = vitals.get("spo2", 0)
        shock_index = hr / max(bp, 1)
        
        print("\n" + "="*50)
        print("📊 PATIENT VITAL SIGNS MONITOR")
        print("="*50)
        print(f"Heart Rate:      {hr} bpm      {'🔴 CRITICAL' if hr > 120 else '🟡 ELEVATED' if hr > 100 else '🟢 NORMAL'}")
        print(f"Blood Pressure:  {bp} mmHg     {'🔴 CRITICAL' if bp < 90 else '🟡 LOW' if bp < 100 else '🟢 NORMAL'}")
        print(f"SpO2:            {spo2}%         {'🔴 CRITICAL' if spo2 < 90 else '🟡 LOW' if spo2 < 94 else '🟢 NORMAL'}")
        print(f"Severity Score:  {severity_score}/10")
        
        # Visual severity bar
        filled = "█" * severity_score
        empty = "░" * (10 - severity_score)
        color = "🔴" if severity_score >= 8 else "🟡" if severity_score >= 5 else "🟢"
        print(f"Severity:        [{filled}{empty}] {color}")
        
        print("\n📈 TRENDS:")
        print(f"   BP Trend:     {trend['bp_trend'].upper()} {'⬇️' if trend['bp_trend'] == 'falling' else '⬆️' if trend['bp_trend'] == 'rising' else '➡️'}")
        print(f"   HR Trend:     {trend['hr_trend'].upper()} {'⬆️' if trend['hr_trend'] == 'rising' else '⬇️' if trend['hr_trend'] == 'falling' else '➡️'}")
        print(f"   SpO2 Trend:   {trend['spo2_trend'].upper()} {'⬇️' if trend['spo2_trend'] == 'falling' else '⬆️' if trend['spo2_trend'] == 'rising' else '➡️'}")
        
        print(f"\n⚠️ Shock Index: {shock_index:.2f} {'🔴 SEVERE SHOCK' if shock_index > 1.5 else '🟡 SHOCK' if shock_index > 1.0 else '🟢 STABLE'}")
        print("="*50 + "\n")

    def execute_protocol(self, protocol_name, injury_description):
        """Interactive protocol execution with paramedic."""
        protocol = self.guidance.get_protocol(protocol_name)
        
        print("\n" + "="*50)
        print(f"📋 INITIATING {protocol['name']}")
        print("="*50)
        
        self.tts.speak(f"CRITICAL ALERT. Initiating {protocol['name'].lower()}.")
        
        completed_steps = 0
        failed_steps = 0
        step_logs = []
        
        for step in protocol["steps"]:
            print(f"\nSTEP {step['id']}/{len(protocol['steps'])}")
            print("-" * 50)
            print(f"📌 {step['instruction']}")
            
            self.tts.speak(f"Step {step['id']}. {step['instruction']}")
            
            # Get paramedic response
            print("🎤 Awaiting response: Say 'COMPLETED' or 'FAILED'")
            response = self.asr.listen(timeout=10, phrase_time_limit=5)
            
            if not response:
                print("⚠️ No response received. Assuming step in progress...")
                continue
            
            response_lower = response.lower()
            success = "complete" in response_lower or "done" in response_lower or "yes" in response_lower
            
            if success:
                print("✅ STEP COMPLETED")
                feedback = self.guidance.get_step_feedback(protocol_name, step['id'], True)
                self.tts.speak(feedback)
                completed_steps += 1
                step_logs.append({"step": step['id'], "status": "completed", "instruction": step['instruction']})
            else:
                print("❌ STEP FAILED")
                feedback = self.guidance.get_step_feedback(protocol_name, step['id'], False)
                self.tts.speak(feedback)
                
                # Ask for details
                print("🎤 Describe what happened:")
                self.tts.speak("Describe what happened.")
                details = self.asr.listen(timeout=15, phrase_time_limit=15)
                print(f"📝 Paramedic describes: {details}")
                
                failed_steps += 1
                step_logs.append({
                    "step": step['id'], 
                    "status": "failed", 
                    "instruction": step['instruction'],
                    "details": details
                })
            
            time.sleep(1)
        
        # Protocol summary
        total_steps = len(protocol['steps'])
        success_rate = (completed_steps / total_steps) * 100
        
        print("\n" + "="*50)
        print("📊 PROTOCOL SUMMARY")
        print("="*50)
        print(f"✅ Completed Steps: {completed_steps}/{total_steps}")
        print(f"❌ Failed Steps: {failed_steps}/{total_steps}")
        
        status = "🟢 EXCELLENT" if success_rate >= 80 else "🟡 GOOD" if success_rate >= 60 else "🔴 CRITICAL"
        print(f"{status} STATUS: {success_rate:.0f}% success rate")
        
        feedback_msg = "Excellent work. All critical interventions completed." if success_rate >= 80 else \
                      "Good effort. Most critical steps completed. Continue monitoring closely." if success_rate >= 60 else \
                      "Multiple interventions failed. Request ALS backup and expedite transport."
        
        self.tts.speak(feedback_msg)
        print("="*50 + "\n")
        
        return {
            "protocol": protocol['name'],
            "completed": completed_steps,
            "failed": failed_steps,
            "success_rate": success_rate,
            "steps": step_logs
        }

    def collect_eta(self):
        """Collect ETA from paramedic."""
        print("\n" + "="*50)
        self.tts.speak("What is your estimated time of arrival?")
        print("🎤 Please state ETA in minutes:")
        
        eta_response = self.asr.listen(timeout=10, phrase_time_limit=5)
        
        # Extract number from response
        import re
        numbers = re.findall(r'\d+', eta_response)
        eta_minutes = int(numbers[0]) if numbers else 15
        
        print(f"⏱️ ETA: {eta_minutes} minutes")
        self.tts.speak(f"ETA {eta_minutes} minutes logged. Maintain current care. Safe transport.")
        print("="*50 + "\n")
        
        return eta_minutes

    def analyze_patient(self, report):
        """Main analysis pipeline."""
        self.session.add_event("paramedic_report", report)
        self.memory_bank.save("paramedic_report", report)

        current_vitals = self.vitals_history[-1]
        severity = self.severity.estimate(current_vitals)
        trend = self.compactor.summarize(self.vitals_history)
        specialists = self.specialty.assign_specialists(report, current_vitals)

        # Display visual status
        self.display_visual_status(current_vitals, severity, trend)

        # Execute protocol
        protocol_name = self.guidance.select_protocol(report)
        protocol_result = self.execute_protocol(protocol_name, report)

        # Oracle decision
        oracle_out = self.oracle.analyze(
            report=report,
            vitals=current_vitals,
            severity_score=severity,
            trend=trend,
            specialists=specialists
        )
        oracle_out["protocol_execution"] = protocol_result

        self.last_analysis = oracle_out

        # Save for dashboard
        with open(os.path.join(PROJECT_ROOT, "last_analysis.json"), "w") as f:
            json.dump(oracle_out, f, indent=2)

        # Hospital notification
        print("\n" + "="*50)
        print("🏥 HOSPITAL NOTIFICATION")
        print("="*50)
        
        msg = A2AMessage(
            from_agent="AEGIS",
            to_agent="HospitalAI",
            payload={
                **oracle_out,
                "injury_description": report
            },
            trace_id=str(uuid.uuid4())
        )

        response = self.router.send(msg, target_client=self.hospital_client)
        self.memory_bank.save("hospital_response", response)

        self.tts.speak(f"Hospital notified. {oracle_out['ward']} ward confirmed. Specialists are being mobilized.")
        
        if response.get("specialists"):
            print(f"📋 Specialists assigned: {', '.join([s['specialty'] for s in response['specialists']])}")
        
        print("="*50 + "\n")

        # Collect ETA
        eta = self.collect_eta()
        oracle_out["eta_minutes"] = eta

        return oracle_out, response

    def run(self):
        """Main operational loop."""
        print("\n" + "="*60)
        print("🛡️ A.E.G.I.S ONLINE")
        print("="*60)
        self.tts.speak("AEGIS system online. All agents initialized.")
        print("="*60 + "\n")

        # Collect vitals for 10 seconds
        print("📊 Collecting vital signs for 10 seconds...\n")
        start = time.time()
        count = 1

        while time.time() - start < 10:
            vitals = self.ingest_vitals()
            self.vitals_history.append(vitals)
            self.session.add_event("vitals", vitals)
            self.memory_bank.save("vitals", vitals)
            print(f"[{count:02d}] Vitals: HR={vitals['hr']} BP={vitals['bp_systolic']} SpO2={vitals['spo2']}%")
            count += 1
            time.sleep(1)

        print("\n✅ Vitals collection complete.\n")

        # Get injury report
        self.tts.speak("AEGIS ready. Describe the patient's visible injuries.")
        print("🎤 Listening for injury description...")
        
        paramedic_report = self.asr.listen(timeout=20, phrase_time_limit=20)
        
        if not paramedic_report:
            print("⚠️ No report received. Using default scenario.")
            paramedic_report = "Male, 35 years old, fell 20 feet from scaffolding. Visible chest deformity, paradoxical breathing, severe respiratory distress."
        
        print(f"📝 Report: {paramedic_report}\n")

        # Analyze
        return self.analyze_patient(paramedic_report)


if __name__ == "__main__":
    aegis = AEGIS()
    final, hospital = aegis.run()
    
    print("\n" + "="*60)
    print("✅ SESSION COMPLETED")
    print("="*60)
    print(f"• {len(aegis.vitals_history)} vital sign readings logged")
    print(f"• {final['protocol_execution']['protocol']} executed ({final['protocol_execution']['success_rate']:.0f}% success rate)")
    print(f"• Hospital {final['ward']} confirmed with {len(hospital.get('specialists', []))} specialists mobilized")
    print(f"• Complete A2A message logs saved")
    print(f"• ETA: {final.get('eta_minutes', 'N/A')} minutes")
    print("="*60 + "\n")
