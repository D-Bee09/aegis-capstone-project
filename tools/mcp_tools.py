# tools/mcp_tools.py
class HospitalLookupTool:
    """
    MCP-like tool:
    Returns info about hospital wards/resources.
    """

    def lookup(self, ward_name):
        data = {
            "ICU": "Critical care with ventilators",
            "HDU": "High dependency unit",
            "TRAUMA": "Trauma resuscitation bay",
            "BURN": "Acute burns management center"
        }
        return {"ward": ward_name, "info": data.get(ward_name.upper(), "Unknown ward")}
