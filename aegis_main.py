"""
A.E.G.I.S. Main System
Complete Integration: Context Compactor, Oracle Engine, A2A Protocol
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import deque

# Import from other modules
# from oracle_engine import OracleEngine
# from a2a_protocol import A2AClient, TOWERCommand


class ContextCompactor:
    """
    Agent 1: Compacts streaming sensor data into trend summaries.
    Processes 5-minute windows of vital signs into actionable trends.
    """
    
    def __init__(self, window_minutes: int = 5):
        """
        Initialize Context Compactor.
        
        Args:
            window_minutes: Size of the rolling window for trend analysis
        """
        self.window_minutes = window_minutes
        self.vital_buffer = {
            'bp_systolic': deque(maxlen=300),   # 5 min @ 1/sec
            'bp_diastolic': deque(maxlen=300),
            'hr': deque(maxlen=300),
            'spo2': deque(maxlen=300),
            'rr': deque(maxlen=60)  # 5 min @ 1/5sec
        }
        self.timestamps = deque(maxlen=300)
    
    def add_reading(self, vitals: Dict) -> None:
        """
        Add a new vital signs reading to the buffer.
        
        Args:
            vitals: Dictionary of current vital signs
        """
        self.timestamps.append(datetime.now())
        
        for key in self.vital_buffer.keys():
            if key in vitals:
                self.vital_buffer[key].append(vitals[key])
    
    def get_trend_summary(self) -> str:
        """
        Generate human-readable trend summary from buffered data.
        
        Returns:
            Concise trend description for Oracle Engine
        """
        if not self.timestamps:
            return "No data available"
        
        # Calculate trends for each vital
        trends = {}
        for vital, readings in self.vital_buffer.items():
            if readings:
                trend = self._calculate_trend(list(readings))
                trends[vital] = trend
        
        # Build narrative summary
        summary_parts = []
        
        # Blood pressure trend
        if 'bp_systolic' in trends:
            bp_trend = trends['bp_systolic']
            bp_current = self.vital_buffer['bp_systolic'][-1] if self.vital_buffer['bp_systolic'] else 0
            bp_start = self.vital_buffer['bp_systolic'][0] if self.vital_buffer['bp_systolic'] else 0
            
            if bp_trend['direction'] == 'declining':
                summary_parts.append(
                    f"BP declining from {bp_start}/{self.vital_buffer['bp_diastolic'][0]} "
                    f"to {bp_current}/{self.vital_buffer['bp_diastolic'][-1]} "
                    f"(Δ{bp_trend['change']:.1f} mmHg)"
                )
            elif bp_trend['direction'] == 'rising':
                summary_parts.append(f"BP rising (Δ+{bp_trend['change']:.1f} mmHg)")
            else:
                summary_parts.append(f"BP stable at {bp_current}/{self.vital_buffer['bp_diastolic'][-1]}")
        
        # Heart rate trend
        if 'hr' in trends:
            hr_trend = trends['hr']
            hr_current = self.vital_buffer['hr'][-1] if self.vital_buffer['hr'] else 0
            hr_start = self.vital_buffer['hr'][0] if self.vital_buffer['hr'] else 0
            
            if hr_trend['direction'] == 'rising':
                summary_parts.append(f"HR increasing from {hr_start} to {hr_current} bpm")
            elif hr_trend['direction'] == 'declining':
                summary_parts.append(f"HR decreasing from {hr_start} to {hr_current} bpm")
            else:
                summary_parts.append(f"HR stable at {hr_current} bpm")
        
        # SpO2 trend
        if 'spo2' in trends:
            spo2_current = self.vital_buffer['spo2'][-1] if self.vital_buffer['spo2'] else 0
            spo2_trend = trends['spo2']
            
            if spo2_trend['direction'] == 'declining':
                summary_parts.append(f"SpO2 declining to {spo2_current}% ⚠️")
            else:
                summary_parts.append(f"SpO2 stable at {spo2_current}%")
        
        # Stability assessment
        volatility = self._assess_volatility()
        if volatility == 'high':
            summary_parts.append("⚠️ HIGH VOLATILITY - Patient unstable")
        
        return ". ".join(summary_parts) + "."
    
    def _calculate_trend(self, readings: List[float]) -> Dict:
        """
        Calculate trend direction and magnitude.
        
        Args:
            readings: List of vital sign readings
        
        Returns:
            Dictionary with direction and change magnitude
        """
        if len(readings) < 2:
            return {'direction': 'stable', 'change': 0}
        
        start_avg = sum(readings[:5]) / min(5, len(readings[:5]))
        end_avg = sum(readings[-5:]) / min(5, len(readings[-5:]))
        change = end_avg - start_avg
        
        # Determine direction with threshold
        threshold = 5  # Minimum change to be considered a trend
        if abs(change) < threshold:
            direction = 'stable'
        elif change > 0:
            direction = 'rising'
        else:
            direction = 'declining'
        
        return {
            'direction': direction,
            'change': abs(change),
            'start_avg': start_avg,
            'end_avg': end_avg
        }
    
    def _assess_volatility(self) -> str:
        """Assess overall patient stability based on vital sign volatility."""
        if not self.vital_buffer['hr']:
            return 'unknown'
        
        # Calculate standard deviation of heart rate (proxy for stability)
        hr_readings = list(self.vital_buffer['hr'])
        mean_hr = sum(hr_readings) / len(hr_readings)
        variance = sum((x - mean_hr) ** 2 for x in hr_readings) / len(hr_readings)
        std_dev = variance ** 0.5
        
        if std_dev > 20:
            return 'high'
        elif std_dev > 10:
            return 'moderate'
        else:
            return 'low'
    
    def get_current_vitals(self) -> Dict:
        """Get most recent vital signs."""
        return {
            'bp_systolic': self.vital_buffer['bp_systolic'][-1] if self.vital_buffer['bp_systolic'] else None,
            'bp_diastolic': self.vital_buffer['bp_diastolic'][-1] if self.vital_buffer['bp_diastolic'] else None,
            'hr': self.vital_buffer['hr'][-1] if self.vital_buffer['hr'] else None,
            'spo2': self.vital_buffer['spo2'][-1] if self.vital_buffer['spo2'] else None,
            'rr': self.vital_buffer['rr'][-1] if self.vital_buffer['rr'] else None,
            'timestamp': self.timestamps[-1].isoformat() if self.timestamps else None
        }


class AEGISSystem:
    """
    Main A.E.G.I.S. Orchestrator
    Coordinates all agents and manages the complete workflow.
    """
    
    def __init__(self, ambulance_id: str, gemini_api_key: str, hospital_endpoint: str):
        """
        Initialize complete A.E.G.I.S. system.
        
        Args:
            ambulance_id: Unique ambulance identifier
            gemini_api_key: API key for Gemini
            hospital_endpoint: Hospital TOWER endpoint
        """
        self.ambulance_id = ambulance_id
        
        # Initialize all agents
        self.context_compactor = ContextCompactor(window_minutes=5)
        # self.oracle_engine = OracleEngine(api_key=gemini_api_key)  # Uncomment in production
        # self.a2a_client = A2AClient(ambulance_id, hospital_endpoint)  # Uncomment in production
        
        # System state
        self.patient_active = False
        self.hospital_notified = False
        self.last_analysis = None
    
    async def start_patient_monitoring(self, initial_report: str) -> None:
        """
        Begin monitoring a new patient.
        
        Args:
            initial_report: Paramedic's initial voice report
        """
        print(f"\n🚨 A.E.G.I.S. ACTIVATED - {self.ambulance_id}")
        print(f"📋 Initial Report: {initial_report}")
        
        self.patient_active = True
        self.initial_report = initial_report
        
        # Start sensor monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    async def _monitoring_loop(self) -> None:
        """
        Main monitoring loop that processes vitals and triggers analysis.
        Runs every second during patient transport.
        """
        while self.patient_active:
            # Simulate vital signs (in production, read from sensors)
            vitals = self._simulate_vitals()
            
            # Add to context compactor
            self.context_compactor.add_reading(vitals)
            
            # Check if we have enough data and haven't notified hospital yet
            if not self.hospital_notified and len(self.context_compactor.timestamps) >= 60:
                await self._trigger_analysis()
            
            await asyncio.sleep(1)  # 1 Hz monitoring
    
    def _simulate_vitals(self) -> Dict:
        """
        Simulate deteriorating patient vitals.
        In production, this would read from actual sensors.
        """
        import random
        
        # Simulate declining BP and rising HR (hemorrhagic shock)
        base_time = len(self.context_compactor.timestamps)
        
        return {
            'bp_systolic': max(70, 110 - (base_time * 0.1) + random.randint(-3, 3)),
            'bp_diastolic': max(40, 70 - (base_time * 0.05) + random.randint(-2, 2)),
            'hr': min(140, 90 + (base_time * 0.15) + random.randint(-2, 2)),
            'spo2': max(88, 96 - (base_time * 0.02) + random.randint(-1, 1)),
            'rr': min(28, 16 + (base_time * 0.05)),
            'gcs': 12
        }
    
    async def _trigger_analysis(self) -> None:
        """
        Trigger complete analysis chain:
        Context Compactor → Oracle Engine → A2A Protocol
        """
        print("\n" + "=" * 60)
        print("🔄 TRIGGERING COMPLETE A.E.G.I.S. ANALYSIS CHAIN")
        print("=" * 60)
        
        # Step 1: Get trend summary from Context Compactor
        print("\n📊 AGENT 1 (Context Compactor): Generating trend summary...")
        trend_summary = self.context_compactor.get_trend_summary()
        current_vitals = self.context_compactor.get_current_vitals()
        print(f"Trend: {trend_summary}")
        
        # Step 2: Oracle Engine analysis (simulated)
        print("\n🔮 AGENT 2 (Oracle Engine): Analyzing with Gemini...")
        # In production: analysis = await self.oracle_engine.analyze_patient(...)
        analysis = self._simulate_oracle_analysis(current_vitals, trend_summary)
        self.last_analysis = analysis
        print(json.dumps(analysis, indent=2))
        
        # Step 3: Send A2A request to hospital
        print("\n📡 AGENT 3 (A2A Client): Sending resource request to hospital...")
        # In production: confirmation = await self.a2a_client.send_resource_request(analysis)
        confirmation = self._simulate_hospital_response()
        print(json.dumps(confirmation, indent=2))
        
        self.hospital_notified = True
        print("\n✅ Hospital resources confirmed and ready!")
    
    def _simulate_oracle_analysis(self, vitals: Dict, trend: str) -> Dict:
        """Simulate Oracle Engine output for demo purposes."""
        return {
            'diagnosis': {
                'primary': 'Severe Head Trauma with Skull Fracture',
                'secondary': ['Hemothorax', 'Pelvic Fracture'],
                'polytrauma': True,
                'hemorrhage_risk': 'severe',
                'categories': ['skull_fracture', 'chest_trauma']
            },
            'specialists_required': [
                'Neurosurgeon',
                'ENT',
                'Trauma Surgeon',
                'Cardiothoracic',
                'Intensivist'
            ],
            'blood_requirements': {
                'prbc_units': 6,
                'ffp_units': 4,
                'platelet_units': 1,
                'total_units': 11,
                'protocol': 'MTP_FULL',
                'urgency': 'IMMEDIATE'
            },
            'bed_type': 'ICU',
            'severity_score': 9,
            'eta_minutes': 12
        }
    
    def _simulate_hospital_response(self) -> Dict:
        """Simulate hospital TOWER response."""
        return {
            'status': 'CONFIRMED',
            'case_id': 'CASE_20250512_001',
            'resources': {
                'specialists': {
                    'allocated': [
                        {'specialty': 'Neurosurgeon', 'status': 'AVAILABLE', 'eta': '5 min'},
                        {'specialty': 'ENT', 'status': 'AVAILABLE', 'eta': '5 min'},
                        {'specialty': 'Trauma Surgeon', 'status': 'AVAILABLE', 'eta': '3 min'},
                        {'specialty': 'Cardiothoracic', 'status': 'ON_CALL', 'eta': '15 min'},
                        {'specialty': 'Intensivist', 'status': 'AVAILABLE', 'eta': '3 min'}
                    ]
                },
                'bed': {
                    'bed_type': 'ICU',
                    'status': 'RESERVED',
                    'location': 'ICU_BAY_3'
                },
                'blood': {
                    'status': 'READY',
                    'blood_type': 'O_NEG',
                    'units': {'prbc': 6, 'ffp': 4, 'platelets': 1},
                    'location': 'TRAUMA_BAY_WARMER'
                }
            },
            'ready_time': 10  # minutes
        }
    
    def get_dashboard_data(self) -> Dict:
        """
        Get current dashboard data for UI display.
        
        Returns:
            Complete system state for dashboard
        """
        return {
            'ambulance_id': self.ambulance_id,
            'patient_active': self.patient_active,
            'current_vitals': self.context_compactor.get_current_vitals(),
            'trend_summary': self.context_compactor.get_trend_summary() if self.patient_active else None,
            'last_analysis': self.last_analysis,
            'hospital_notified': self.hospital_notified,
            'timestamp': datetime.now().isoformat()
        }


# Demo function to show complete system
async def demo_complete_system():
    """
    Demonstrate complete A.E.G.I.S. system workflow.
    This simulates a 2-minute patient transport with real-time monitoring.
    """
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "A.E.G.I.S. SYSTEM DEMONSTRATION" + " " * 17 + "║")
    print("║" + " " * 4 + "Automated Emergency Guidance & Intelligence System" + " " * 4 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Initialize system
    aegis = AEGISSystem(
        ambulance_id="RESCUE_7",
        gemini_api_key="demo_key",
        hospital_endpoint="hospital.example.com/tower"
    )
    
    # Start patient monitoring with initial report
    initial_report = """
    52-year-old male, fall from 20 feet.
    Patient unconscious on arrival, GCS 8.
    Obvious skull deformity right side with CSF rhinorrhea.
    Decreased breath sounds right chest.
    Pelvis unstable to palpation.
    Currently GCS 12 after intubation and fluids.
    """
    
    await aegis.start_patient_monitoring(initial_report)
    
    # Run for 2 minutes to collect data and trigger analysis
    print("\n⏱️  Monitoring for 120 seconds...")
    await asyncio.sleep(120)
    
    # Show final dashboard
    print("\n" + "=" * 60)
    print("📊 FINAL DASHBOARD STATE")
    print("=" * 60)
    dashboard = aegis.get_dashboard_data()
    print(json.dumps(dashboard, indent=2))
    
    # Stop monitoring
    aegis.patient_active = False
    print("\n✅ Demo complete - Patient handoff ready")


if __name__ == "__main__":
    # Run complete system demonstration
    asyncio.run(demo_complete_system())
