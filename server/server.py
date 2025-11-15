from flask import Flask, request, jsonify
from db import insert_reading
from datetime import datetime
import json

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


if __name__ == "__main__":
    log("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
