from flask import Flask, request, jsonify
from db import insert_reading
from datetime import datetime
import json
from zeroconf import ServiceInfo, Zeroconf
import socket

app = Flask(__name__)

def log(msg):
    """Simple timestamped logger."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[SERVER {timestamp}] {msg}")


@app.before_request
def before_request_logging():
    """Log every incoming request."""
    log(f"Incoming {request.method} {request.path} from {request.remote_addr}")


@app.route("/upload", methods=["POST"])
def upload():
    # Parse JSON
    data = request.get_json()

    # Log raw JSON body
    log(f"Received JSON: {json.dumps(data, indent=2)}")

    if not data:
        log("ERROR: No JSON provided.")
        return jsonify({"error": "No JSON provided"}), 400

    # Insert into database
    success = insert_reading(data)

    if success:
        log("Database insert: SUCCESS")
        return jsonify({"status": "ok"}), 200
    else:
        log("Database insert: FAILED")
        return jsonify({"error": "Database insert failed"}), 500


@app.after_request
def after_request_logging(response):
    """Log outgoing response status code."""
    log(f"Response: {response.status_code}")
    return response


# ================================================================
# 🔥 mDNS BROADCAST SECTION (this is the autodetect magic)
# ================================================================
def start_mdns_service():
    try:
        hostname = "pico-server.local."
        local_ip = socket.gethostbyname(socket.gethostname())

        info = ServiceInfo(
            "_http._tcp.local.",
            "pico-server._http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=5000,
            properties={},
            server=hostname,
        )

        zeroconf = Zeroconf()
        zeroconf.register_service(info)

        log(f"[mDNS] Advertised on network as http://pico-server.local:5000")
        log(f"[mDNS] Local IP: {local_ip}")

    except Exception as e:
        log(f"[mDNS] Error starting Zeroconf: {e}")


# ================================================================
# MAIN ENTRY POINT
# ================================================================
if __name__ == "__main__":
    log("Starting Flask server...")

    # Start autodiscovery service BEFORE Flask run()
    start_mdns_service()

    # Start Flask
    app.run(debug=True, use_reloader=False)
