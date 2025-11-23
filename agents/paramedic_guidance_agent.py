# agents/paramedic_guidance_agent.py
class ParamedicGuidanceAgent:
    """
    Provides step-by-step medical protocol guidance with adaptive feedback.
    """
    
    PROTOCOLS = {
        "chest_trauma": {
            "name": "CHEST TRAUMA PROTOCOL",
            "steps": [
                {
                    "id": 1,
                    "instruction": "Assess airway, breathing, circulation",
                    "success_response": "Good. Airway patent. Continue monitoring.",
                    "failure_response": "Airway compromise detected. Prepare intubation kit immediately."
                },
                {
                    "id": 2,
                    "instruction": "Apply high-flow oxygen via non-rebreather mask at 15 liters per minute",
                    "success_response": "Excellent. Oxygen therapy initiated. Monitor SpO2 closely.",
                    "failure_response": "Unable to maintain oxygen saturation. Consider bag-valve-mask ventilation."
                },
                {
                    "id": 3,
                    "instruction": "Examine chest for paradoxical movement, crepitus, or open wounds",
                    "success_response": "Chest examination complete. No immediate life threats identified.",
                    "failure_response": "Flail chest identified. Apply occlusive dressing. Prepare needle decompression kit."
                },
                {
                    "id": 4,
                    "instruction": "Establish large-bore IV access in both arms",
                    "success_response": "IV access secured. Ready for fluid administration.",
                    "failure_response": "IV access failed. Attempt intraosseous access immediately."
                },
                {
                    "id": 5,
                    "instruction": "Begin cautious fluid resuscitation - 250ml bolus, then reassess",
                    "success_response": "Fluid bolus administered. Reassessing hemodynamics.",
                    "failure_response": "Patient not responding to fluids. Suspect internal hemorrhage. Expedite transport."
                }
            ]
        },
        "head_trauma": {
            "name": "HEAD TRAUMA PROTOCOL",
            "steps": [
                {
                    "id": 1,
                    "instruction": "Assess level of consciousness using GCS",
                    "success_response": "GCS documented. Continue neurological monitoring.",
                    "failure_response": "Decreased level of consciousness. Protect airway immediately."
                },
                {
                    "id": 2,
                    "instruction": "Immobilize cervical spine with collar",
                    "success_response": "C-spine immobilized. Maintain neutral alignment.",
                    "failure_response": "Unable to apply collar. Maintain manual inline stabilization."
                },
                {
                    "id": 3,
                    "instruction": "Check pupils - size, equality, reactivity",
                    "success_response": "Pupils equal and reactive. Document baseline.",
                    "failure_response": "Pupil abnormality detected. Possible increased ICP. Elevate head 30 degrees."
                },
                {
                    "id": 4,
                    "instruction": "Establish IV access and prepare mannitol if available",
                    "success_response": "IV established. Mannitol ready if needed.",
                    "failure_response": "No IV access. Continue attempts during transport."
                },
                {
                    "id": 5,
                    "instruction": "Maintain SpO2 above 90% and avoid hypotension",
                    "success_response": "Vital parameters optimized. Continue monitoring.",
                    "failure_response": "Unable to maintain parameters. Increase respiratory support."
                }
            ]
        },
        "burn": {
            "name": "BURN TRAUMA PROTOCOL",
            "steps": [
                {
                    "id": 1,
                    "instruction": "Ensure scene safety and remove patient from heat source",
                    "success_response": "Patient removed from danger. Scene secure.",
                    "failure_response": "Scene unsafe. Call for additional resources before approaching."
                },
                {
                    "id": 2,
                    "instruction": "Assess total body surface area burned using rule of nines",
                    "success_response": "TBSA calculated. Documented for fluid resuscitation.",
                    "failure_response": "Unable to assess full extent. Estimate conservatively high."
                },
                {
                    "id": 3,
                    "instruction": "Cover burns with sterile dressing - do not apply ice",
                    "success_response": "Burns covered appropriately. Temperature preserved.",
                    "failure_response": "Insufficient sterile dressings. Use clean dry sheets."
                },
                {
                    "id": 4,
                    "instruction": "Establish two large-bore IVs for fluid resuscitation",
                    "success_response": "Dual IV access secured. Begin Parkland formula fluids.",
                    "failure_response": "Unable to obtain IV access. Attempt IO route."
                },
                {
                    "id": 5,
                    "instruction": "Administer pain management per protocol",
                    "success_response": "Analgesia administered. Monitor pain levels.",
                    "failure_response": "Unable to give medications. Reassure patient and expedite transport."
                }
            ]
        },
        "general_trauma": {
            "name": "GENERAL TRAUMA PROTOCOL",
            "steps": [
                {
                    "id": 1,
                    "instruction": "Primary survey - ABCDE approach",
                    "success_response": "Primary survey complete. All systems assessed.",
                    "failure_response": "Critical finding in primary survey. Address immediately before proceeding."
                },
                {
                    "id": 2,
                    "instruction": "Control any visible external bleeding",
                    "success_response": "Bleeding controlled. Dressings secure.",
                    "failure_response": "Unable to control bleeding. Apply tourniquet or hemostatic agent."
                },
                {
                    "id": 3,
                    "instruction": "Establish vascular access",
                    "success_response": "Vascular access obtained. Ready for medications.",
                    "failure_response": "Access attempts unsuccessful. Consider alternative routes."
                },
                {
                    "id": 4,
                    "instruction": "Perform secondary survey - head to toe assessment",
                    "success_response": "Secondary survey complete. All injuries documented.",
                    "failure_response": "Patient too unstable for full secondary survey. Load and go."
                },
                {
                    "id": 5,
                    "instruction": "Package patient for transport with full spinal precautions",
                    "success_response": "Patient packaged. Ready for transport.",
                    "failure_response": "Packaging incomplete due to time constraints. Secure during transport."
                }
            ]
        }
    }
    
    def select_protocol(self, injury_description):
        """
        Select appropriate protocol based on injury keywords.
        """
        desc = injury_description.lower()
        
        if any(word in desc for word in ["chest", "rib", "thorax", "breathing", "respiratory"]):
            return "chest_trauma"
        elif any(word in desc for word in ["head", "skull", "brain", "consciousness"]):
            return "head_trauma"
        elif "burn" in desc:
            return "burn"
        else:
            return "general_trauma"
    
    def get_protocol(self, protocol_name):
        """
        Returns the full protocol steps.
        """
        return self.PROTOCOLS.get(protocol_name, self.PROTOCOLS["general_trauma"])
    
    def get_step_feedback(self, protocol_name, step_id, success):
        """
        Returns appropriate feedback based on step outcome.
        """
        protocol = self.PROTOCOLS.get(protocol_name)
        if not protocol:
            return "Protocol not found."
        
        for step in protocol["steps"]:
            if step["id"] == step_id:
                return step["success_response"] if success else step["failure_response"]
        
        return "Step feedback not available."
