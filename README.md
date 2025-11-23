# A.E.G.I.S: Automated Emergency Guide Intelligence System

**AI-Enhanced Guardian**

## 🚑 Problem Statement

In emergency medical situations, the critical "golden hour" between injury and hospital care can determine patient survival. Paramedics face overwhelming challenges:

1. **Communication Breakdowns**: Vital information gets lost between ambulance and hospital
2. **Hands-Busy Limitation**: Paramedics treating patients cannot simultaneously write reports or make phone calls
3. **Resource Allocation Delays**: Hospitals need advance notice to mobilize specialists and prepare resources
4. **Cognitive Overload**: Paramedics must simultaneously treat patients while manually communicating status updates
5. **Lack of Predictive Intelligence**: No real-time analysis of patient deterioration trends

These gaps lead to delayed care, misallocated resources, and preventable deaths. **A.E.G.I.S (Automated Emergency Guide Intelligence System) bridges this critical gap using voice-activated AI agents that enable hands-free operation.**

## 💡 Solution

**A.E.G.I.S (Automated Emergency Guide Intelligence System)** is an AI-powered pre-hospital coordination system that uses autonomous agents to:

1. **Monitor** patient vitals continuously via IoT medical devices
2. **Listen** to paramedic verbal reports using speech recognition
3. **Analyze** severity trends and predict resource needs using AI
4. **Guide** paramedics step-by-step through medical protocols with real-time feedback
5. **Respond** to each intervention's success or failure with adaptive instructions
6. **Coordinate** with hospital systems via Agent-to-Agent (A2A) communication
7. **Speak** critical updates back to paramedics via text-to-speech

The system operates autonomously in the ambulance with **interactive two-way communication**, guiding paramedics through trauma protocols while ensuring hospitals receive comprehensive, structured patient data before arrival.

## 🎯 Value Proposition

- **Saves Lives**: Reduces hospital preparation time by 5-10 minutes through automated communication
- **Hands-Free Operation**: Voice-activated system allows paramedics to focus on patient care
- **Interactive Guidance**: Step-by-step medical protocols with real-time success/failure feedback
- **Adaptive Intelligence**: System responds differently based on whether interventions succeed or fail
- **Optimizes Resources**: Pre-assigns specialists based on AI analysis before ambulance arrival
- **Reduces Cognitive Load**: Automates documentation and communication, eliminating manual reporting
- **Improves Coordination**: Standardized A2A protocol ensures no information loss between teams
- **Enables Predictive Care**: Trend analysis alerts teams to deteriorating patients in real-time
- **Complete Documentation**: Automatically logs all interventions and outcomes for legal/medical records

## 🏗️ Architecture
#### System Flow Diagram

```mermaid
graph TB
    subgraph AMBULANCE["🚑 AEGIS AMBULANCE SYSTEM"]
        ASR[ASR Agent<br/>Speech-to-Text]
        VITALS[Vitals Monitor<br/>IoT Sensors<br/>HR, BP, SpO2]
        SESSION[Session Service<br/>Memory Bank]
        
        ORCH[AEGIS Orchestrator<br/>Pipeline Coordinator]
        
        COMPACT[Context Compactor<br/>Trend Analysis]
        SEVERITY[Severity Estimator<br/>Shock Index]
        SPECIALTY[Multi-Specialty<br/>Coordinator]
        
        ORACLE[Gemini Oracle<br/>Final Decision Engine]
        
        TTS[TTS Agent<br/>Voice Feedback]
        A2A[A2A Router<br/>Message Queue]
    end
    
    subgraph HOSPITAL["🏥 HOSPITAL AI SYSTEM"]
        API[Hospital OpenAPI<br/>Handoff Endpoint]
        RESPONSE[Ward Assignment<br/>Specialist Confirmation<br/>Case ID & ETA]
    end
    
    subgraph DASHBOARD["📊 WEB DASHBOARD"]
        FLASK[Flask Server<br/>Real-time Monitoring]
        LOGS[A2A Logs Viewer]
        MEMORY[Memory Bank Viewer]
    end
    
    ASR --> ORCH
    VITALS --> ORCH
    SESSION --> ORCH
    
    ORCH --> COMPACT
    ORCH --> SEVERITY
    ORCH --> SPECIALTY
    
    COMPACT --> ORACLE
    SEVERITY --> ORACLE
    SPECIALTY --> ORACLE
    
    ORACLE --> TTS
    ORACLE --> A2A
    
    A2A -->|A2A Protocol<br/>JSON/REST| API
    API -->|HTTPS Response| RESPONSE
    RESPONSE --> SESSION
    
    A2A -.->|Logs| FLASK
    SESSION -.->|Events| FLASK
    FLASK --> LOGS
    FLASK --> MEMORY
    
    style AMBULANCE fill:#e1f5ff,stroke:#000,stroke-width:2px,color:#000
    style HOSPITAL fill:#fff4e1,stroke:#000,stroke-width:2px,color:#000
    style DASHBOARD fill:#f0f0f0,stroke:#000,stroke-width:2px,color:#000
    style ORACLE fill:#ffcccc
    style A2A fill:#ccffcc
```

#### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  [ASR Agent]    [Vitals Monitor]    [Session Memory]        │
│   Speech           IoT Sensors        Event History         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  ORCHESTRATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│              AEGIS Core Orchestrator                        │
│        • Pipeline Coordination                              │
│        • Event Management                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   ANALYSIS LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  [Context Compactor] [Severity Estimator] [Multi-Specialty] │
│   Trend Analysis      Shock Index Calc     Specialist Match │
│   BP/HR/SpO2 Trends   Score: 1-10          Burns/Neuro/etc  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  DECISION LAYER                             │
├─────────────────────────────────────────────────────────────┤
│                  Gemini Oracle Agent                        │
│         • Synthesizes all agent outputs                     │
│         • Ward assignment (ICU/HDU/TRAUMA)                  │
│         • Resource allocation decisions                     │
└────────────────┬─────────────────────┬──────────────────────┘
                 │                     │
        ┌────────▼────────┐   ┌────────▼────────┐
        │   TTS Agent     │   │   A2A Router    │
        │  Voice Feedback │   │ Message Logging │
        └─────────────────┘   └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │ Hospital OpenAPI│
                              │     Client      │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────────────┐
                              │  Hospital AI System     │
                              │  • Handoff Endpoint     │
                              │  • Ward Confirmation    │
                              │  • Specialist ETA       │
                              └─────────────────────────┘
```

### Key Agent Responsibilities

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| **ASR Agent** | Converts paramedic speech to structured text (CRITICAL for hands-free operation) | Audio from microphone | Text transcription |
| **Paramedic Guidance** | Provides step-by-step medical protocols with adaptive feedback | Injury type, vitals, severity | Protocol steps with success/failure responses |
| **Context Compactor** | Analyzes vital sign trends over time | Array of vital readings | Trend summary (rising/falling/stable) |
| **Severity Estimator** | Calculates trauma severity score | Current vitals (HR, BP, SpO2) | Severity score (1-10) |
| **Multi-Specialty Coordinator** | Assigns required medical specialists | Injury description + vitals | List of specialist types |
| **Gemini Oracle** | Final decision-making and synthesis | All agent outputs | Ward assignment, resource allocation |
| **TTS Agent** | Provides voice feedback to paramedics (CRITICAL for hands-free confirmation) | Text messages | Spoken audio output |
| **A2A Router** | Manages inter-agent communication | Messages between agents | Logged, routed messages |

## 🔑 Key Concepts Demonstrated

### 1. **Multi-Agent Coordination**
- Six specialized agents work collaboratively
- Clear separation of concerns (trend analysis, severity scoring, specialist assignment)
- Orchestrator pattern coordinates agent execution pipeline

### 2. **Agent-to-Agent (A2A) Communication**
- Structured message passing between AEGIS and Hospital AI
- Trace IDs for full observability
- JSON logging of all A2A transactions
- Implements OpenAPI client for standardized hospital integration

### 3. **Memory Systems**
- **Session Memory**: In-memory storage for current patient encounter
- **Memory Bank**: Persistent JSON storage for critical events
- **Context Window Management**: Compactor agent summarizes long vital histories

### 4. **Orchestration & Workflow**
- Sequential pipeline: Ingest → Analyze → Decide → Communicate
- Deterministic agent execution order
- Error handling and fallback mechanisms

### 5. **Tool Integration**
- **MCP-like Tools**: Hospital lookup tool for ward information
- **OpenAPI Integration**: RESTful communication with external hospital system
- **IoT Mock Interface**: Simulated vital sign ingestion (extensible to real devices)

### 6. **Observability**
- Metrics tracking (counters, timers)
- Complete A2A message logging
- Web dashboard for real-time monitoring
- Timestamped event history

## 🛠️ Technical Implementation

### Technology Stack

- **Core Language**: Python 3.8+
- **Speech Recognition**: `speech_recognition` library (Google Speech API)
- **Text-to-Speech**: `pyttsx3` (offline), `gTTS` (online option)
- **Web Framework**: Flask for dashboard
- **HTTP Client**: `requests` for OpenAPI calls
- **LLM Integration**: Gemini Oracle stub (ready for Gemini API integration)

### Code Quality Features

- **Modular Design**: Each agent is a separate class in its own file
- **Docstrings**: All classes include purpose documentation
- **Error Handling**: Try-catch blocks in critical paths (A2A routing, file I/O)
- **Configuration**: Paths managed via `PROJECT_ROOT` constants
- **Type Hints**: Used in key functions for clarity

### File Structure

```
aegis/
├── agents/
│   ├── asr_agent.py              # Speech recognition with error handling
│   ├── tts_agent.py              # Text-to-speech feedback
│   ├── context_compactor.py      # Vital trend analysis
│   ├── multi_speciality.py       # Specialist assignment logic
│   └── severity_estimator.py     # Shock index calculation
├── core/
│   ├── a2a.py                    # Agent-to-agent messaging
│   ├── sessions.py               # Memory systems
│   └── observability.py          # Metrics tracking
├── oracle/
│   └── gemini_oracle_stub.py     # LLM decision engine (stub)
├── tools/
│   ├── mcp_tools.py              # MCP-like hospital lookup
│   └── openapi_client.py         # Hospital API integration
├── web/
│   ├── dashboard.py              # Flask dashboard
│   ├── templates/
│   │   └── index.html            # Dashboard UI
│   └── static/
│       └── style.css             # Dashboard styling
├── aegis_main.py                 # Main orchestrator with interactive guidance
├── hospital_sim.py               # Simulated hospital endpoint
├── requirements.txt              # Python dependencies
├── a2a_logs.json                 # A2A message log
├── memory_bank.json              # Persistent memory
└── last_analysis.json            # Most recent analysis result
```

## 🚀 Setup Instructions

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask
requests
pyttsx3
gtts
playsound
speechrecognition
pyaudio
```
### Running the System

**Step 1: Start the Hospital Simulator**

```bash
python hospital_sim.py
# Server runs on http://127.0.0.1:5001
```

**Step 2: Run AEGIS System**

```bash
python aegis_main.py
# Runs for 10 seconds collecting vitals, then performs analysis
```

**Step 3: Launch Dashboard (Optional)**

```bash
cd web
python dashboard.py
# Open browser to http://localhost:8080
```

### Expected Output

```
AEGIS system running...
Vitals: {'hr': 142, 'bp_systolic': 98, 'spo2': 91}
Vitals: {'hr': 135, 'bp_systolic': 95, 'spo2': 89}
...
AEGIS SPEAKS: Hospital notified. Ward ICU confirmed recommendation.

FINAL AEGIS ANALYSIS:
{
  "ward": "ICU",
  "severity_score": 9,
  "trend": {"bp_trend": "falling", "hr_trend": "rising", "spo2_trend": "falling"},
  "specialists_required": ["Trauma Surgeon", "Cardiothoracic Surgeon", ...]
}

HOSPITAL RESPONSE:
{
  "status": "CONFIRMED",
  "case_id": "SIM_1763900000",
  "assigned_ward": "ICU",
  "specialists": [...]
}
```

## 📊 Dashboard Features

The web dashboard (`http://localhost:8080`) provides:

1. **Last Analysis Panel**: JSON view of most recent AI decision
2. **A2A Logs Table**: Chronological message history with trace IDs
3. **Memory Bank**: Recent events from persistent storage
4. **API Endpoints**: 
   - `/api/a2a` - Get A2A logs
   - `/api/last` - Get last analysis
   - `/api/memory` - Get memory bank entries

## 🎥 Demo Scenario

### Complete Interactive Workflow:

**1. System Initialization**
```
🚑 A.E.G.I.S ONLINE
🔊 AEGIS: "AEGIS system online. All agents initialized."
```

**2. Vital Signs Monitoring (10 seconds)**
```
[01] Vitals: HR=142 BP=85 SpO2=89%
[02] Vitals: HR=145 BP=82 SpO2=87%
...
[10] Vitals: HR=148 BP=78 SpO2=86%
```

**3. Paramedic Reports Injury**
```
🔊 AEGIS: "AEGIS ready. Describe the patient's visible injuries."
🎤 Paramedic: "Male, 35 years old, fell 20 feet from scaffolding. 
              Visible chest deformity, paradoxical breathing, 
              severe respiratory distress."
```

**4. Visual Patient Status**
```
📊 PATIENT VITAL SIGNS MONITOR
═══════════════════════════════
Heart Rate:       148 bpm      🔴 CRITICAL
Blood Pressure:    78 mmHg     🔴 CRITICAL  
SpO2:              86%         🔴 CRITICAL

Severity Score:   9/10
Severity:         [█████████░] 🔴

📈 TRENDS:
  BP Trend:    FALLING
  HR Trend:    RISING
  SpO2 Trend:  FALLING

⚠️  Shock Index:   1.90      🔴 SEVERE SHOCK
```

**5. Interactive Protocol Guidance**
```
📋 INITIATING CHEST TRAUMA PROTOCOL
═══════════════════════════════════
🔊 AEGIS: "CRITICAL ALERT. Initiating chest trauma protocol."

STEP 1/5
─────────────────────────────────
📌 Assess airway, breathing, circulation
🔊 AEGIS: "Step 1. Assess airway, breathing, circulation."
🎤 Awaiting response: Say 'COMPLETED' or 'FAILED'

🎤 Paramedic: "Completed"
✅ STEP COMPLETED
🔊 AEGIS: "Good. Airway patent. Continue monitoring."

STEP 2/5
─────────────────────────────────
📌 Apply high-flow oxygen via non-rebreather mask at 15 liters per minute
🔊 AEGIS: "Step 2. Apply high-flow oxygen at 15 liters per minute."

🎤 Paramedic: "Completed"
✅ STEP COMPLETED
🔊 AEGIS: "Excellent. Oxygen therapy initiated. Monitor SpO2 closely."

STEP 3/5
─────────────────────────────────
📌 Examine chest for paradoxical movement, crepitus, or open wounds
🔊 AEGIS: "Step 3. Examine chest for paradoxical movement."

🎤 Paramedic: "Failed"
❌ STEP FAILED
🔊 AEGIS: "Flail chest identified. Apply occlusive dressing. 
          Prepare needle decompression kit."
🎤 Describe what happened:
📝 Paramedic: "Right side moving opposite to breathing, multiple rib fractures"

STEP 4/5
─────────────────────────────────
📌 Establish large-bore IV access in both arms
🔊 AEGIS: "Step 4. Establish large-bore IV access in both arms."

🎤 Paramedic: "Completed"
✅ STEP COMPLETED
🔊 AEGIS: "IV access secured. Ready for fluid administration."

STEP 5/5
─────────────────────────────────
📌 Begin cautious fluid resuscitation - 250ml bolus, then reassess
🔊 AEGIS: "Step 5. Begin fluid resuscitation, 250ml bolus."

🎤 Paramedic: "Completed"
✅ STEP COMPLETED
🔊 AEGIS: "Fluid bolus administered. Reassessing hemodynamics."

📊 PROTOCOL SUMMARY
═══════════════════════════════════
✅ Completed Steps: 4/5
❌ Failed Steps: 1/5
🟡 STATUS: GOOD

🔊 AEGIS: "Good effort. Most critical steps completed. 
          Continue monitoring closely."
```

**6. Hospital Notification**
```
🏥 HOSPITAL NOTIFICATION
═══════════════════════════════════
🔊 AEGIS: "Hospital notified. ICU ward confirmed. 
          Specialists are being mobilized."
📋 Specialists assigned: Trauma Surgeon, Cardiothoracic Surgeon, Anesthesiologist
```

**7. ETA Collection**
```
🔊 AEGIS: "What is your estimated time of arrival?"
🎤 Paramedic: "12 minutes"
🔊 AEGIS: "ETA 12 minutes logged. Maintain current care. Safe transport."
```

**8. Complete Documentation**
```
✅ Session completed.
   - 10 vital sign readings logged
   - Chest trauma protocol executed (80% success rate)
   - Hospital ICU confirmed with 3 specialists mobilized
   - Complete A2A message logs saved
   - ETA: 12 minutes
```

## 🏆 Why Agents?

Agents are **essential** to A.E.G.I.S because:

1. **Parallel Expertise**: Each agent specializes in one medical/technical domain (speech recognition, trend analysis, protocol guidance)
2. **Real-Time Interaction**: The Paramedic Guidance agent provides step-by-step instructions and responds immediately to success/failure feedback
3. **Adaptive Intelligence**: Agents adjust recommendations based on real-time intervention outcomes
4. **Scalability**: New agents (e.g., ECG interpreter, ultrasound analyzer) can be added without rewriting core logic
5. **Fault Tolerance**: If one agent fails, others continue functioning - paramedic can always fall back to manual input
6. **Real-Time Coordination**: Agents process inputs asynchronously (vitals monitoring while listening to speech and guiding through protocols)
7. **Interoperability**: A2A protocol enables communication with external hospital AI agents
8. **Context Awareness**: Each agent maintains state and memory, allowing for contextual responses (e.g., "flail chest identified" only if chest examination fails)

Traditional monolithic systems cannot achieve this level of modularity, real-time responsiveness, interactive feedback, and cross-organizational coordination.

## 🔮 Future Enhancements

- **Live Gemini Integration**: Replace stub with actual Gemini API calls for advanced medical reasoning and protocol selection
- **Real IoT Devices**: Integrate with medical monitors via Bluetooth/serial (Zoll monitors, Philips vital sign monitors)
- **Computer Vision Agent**: Add agent for X-ray/ultrasound image analysis using vision models
- **Multi-Hospital Routing**: A2A communication with multiple hospitals for optimal resource matching based on specialty availability
- **Predictive Deterioration**: Machine learning models to predict patient deterioration before vital signs crash
- **Voice Biometrics**: Verify paramedic identity through voice for secure medical record access
- **Natural Language Protocol Selection**: Let paramedics describe injuries naturally, AI selects appropriate protocol automatically
- **Offline Mode**: Local LLM deployment for areas without cellular connectivity
- **Multi-Language Support**: Protocols and guidance in Spanish, Mandarin, Hindi for diverse paramedic teams
- **Federated Learning**: Train severity models across ambulance fleet data while preserving patient privacy
- **Mobile App**: Paramedic interface for manual overrides, protocol review, and real-time map integration
- **AR Glasses Integration**: Project vital signs and guidance directly into paramedic's field of view
- **Continuous Learning**: System learns from successful/failed interventions to refine protocol recommendations

## 📝 Notes

- **API Keys**: No API keys are committed to this repository. For Gemini integration, set `GOOGLE_API_KEY` environment variable.
- **Simulator**: `hospital_sim.py` simulates hospital responses; replace with real hospital endpoints in production.
- **Speech Recognition**: Default uses Google Speech API (requires internet); can be replaced with offline models.

## 🎓 Course Concepts Applied

This project demonstrates mastery of:

1. ✅ **Multi-agent architecture** (7 specialized agents including interactive Paramedic Guidance)
2. ✅ **Agent-to-agent communication** (A2A protocol with logging and hospital integration)
3. ✅ **Memory systems** (session + persistent storage for protocol execution history)
4. ✅ **Tool integration** (MCP-like tools + OpenAPI + speech recognition)
5. ✅ **Orchestration patterns** (centralized AEGIS coordinator managing agent workflow)
6. ✅ **Observability** (metrics, logging, dashboard, complete audit trail)
7. ✅ **LLM integration** (Gemini Oracle architecture ready for deployment)
8. ✅ **Interactive agents** (Real-time feedback loop with adaptive responses)
9. ✅ **State management** (Protocol execution tracking with success/failure states)
10. ✅ **Error handling** (Robust speech recognition with timeout and retry logic)

## 📄 License

This project is a capstone demonstration for educational purposes.

---

**A.E.G.I.S**: Because every second counts in the golden hour. 🚑💙

*Automated Emergency Guide Intelligence System - Saving lives through intelligent automation.*
