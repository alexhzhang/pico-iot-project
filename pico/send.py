import urequests

UPLOAD_URL = "http://pico-server.local:5000/upload"

def send_payload(payload):
    try:
        r = urequests.post(UPLOAD_URL, json=payload)
        r.close()
        return True
    except Exception as e:
        print("Send error:", e)
        return False
