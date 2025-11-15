# send.py — sends JSON to your Flask API
import urequests
import json

UPLOAD_URL = "http://YOUR_PC_IP:5000/upload"
# Replace YOUR_PC_IP with actual IP of PC hosting Flask server

def send_payload(payload):
    try:
        r = urequests.post(UPLOAD_URL, json=payload)
        r.close()
        return True
    except Exception as e:
        print("Send error:", e)
        return False
