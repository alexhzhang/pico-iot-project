# send_sim.py
import requests
from datetime import datetime

# Adjust if your Flask server is bound differently
UPLOAD_URL = "http://127.0.0.1:5000/upload"
TIMEOUT_SEC = 5


def send_reading(payload: dict):
    """
    Send one JSON payload to the Flask /upload endpoint.
    Returns (success: bool, status_code: int | None, text: str | None)
    """
    try:
        resp = requests.post(UPLOAD_URL, json=payload, timeout=TIMEOUT_SEC)
        return True, resp.status_code, resp.text
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [SIM] Error sending data:", e)
        return False, None, None
