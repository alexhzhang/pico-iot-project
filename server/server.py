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
    """Pico sensor upload endpoint."""
    data = request.get_json()

    log(f"Received JSON: {json.dumps(data, indent=2)}")

    if not data:
        log("ERROR: No JSON provided.")
        return jsonify({"error": "No JSON provided"}), 400

    success = insert_reading(data)

    if success:
        log("Database insert: SUCCESS")
        return jsonify({"status": "ok"}), 200
    else:
        log("Database insert: FAILED")
        return jsonify({"error": "Database insert failed"}), 500


# ================================================================
#  ADDED: /latest route
# ================================================================
from db import get_db  # ensure we can query

@app.route("/latest", methods=["GET"])
def latest():
    """Returns the most recent sensor reading."""
    conn = get_db()
    if conn is None:
        return jsonify({"error": "DB connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT device_id, temp, humidity, pressure, light,
                   raw_json, timestamp
            FROM readings
            ORDER BY id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return jsonify({"error": "No data found"}), 404

        return jsonify(row)

    except Exception as e:
        print("[DB] Latest error:", e)
        return jsonify({"error": "Query failed"}), 500

    finally:
        conn.close()


# ================================================================
#  ADDED: /history route
# ================================================================
@app.route("/history", methods=["GET"])
def history():
    """Returns N most recent readings for charting."""
    limit = int(request.args.get("limit", 100))

    conn = get_db()
    if conn is None:
        return jsonify({"error": "DB connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT device_id, temp, humidity, pressure, light,
                   timestamp
            FROM readings
            ORDER BY id DESC
            LIMIT {limit}
        """)
        rows = cursor.fetchall()
        cursor.close()

        rows.reverse()  # oldest → newest for charts

        return jsonify(rows)

    except Exception as e:
        print("[DB] History error:", e)
        return jsonify({"error": "Query failed"}), 500

    finally:
        conn.close()



@app.after_request
def after_request_logging(response):
    """Log outgoing response status code."""
    log(f"Response: {response.status_code}")
    return response


# ================================================================
#  mDNS BROADCAST SECTION (this is the autodetect magic)
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
