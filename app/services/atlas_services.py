from flask import current_app
import requests
from requests.auth import HTTPBasicAuth

ATLAS_USERNAME = current_app.config.get("ATLAS_USERNAME")
ATLAS_PASSWORD = current_app.config.get("ATLAS_PASSWORD")

ATLAS_BASE_URL = current_app.config.get("ATLAS_BASE_URL")

def mask_aadhaar(aadhaar_file):
    ATLAS_AADHAAR_MASK_URL = f"{ATLAS_BASE_URL}/aadhaar/mask"

    auth = HTTPBasicAuth(username=ATLAS_USERNAME, password=ATLAS_PASSWORD)

    response = requests.post(
        ATLAS_AADHAAR_MASK_URL, 
        auth=auth, 
        data= {
            "file": aadhaar_file,
            "mask_qr": True
        })
    
    return response