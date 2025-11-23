# tools/openapi_client.py
import requests

class HospitalOpenAPIClient:
    """
    Sends patient data & requests resources from hospital AI.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def handoff(self, payload):
        try:
            r = requests.post(self.base_url + "/handoff", json=payload, timeout=5)
            return r.json()
        except Exception as e:
            return {"error": str(e)}
