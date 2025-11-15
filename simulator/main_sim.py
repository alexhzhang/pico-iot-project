# main_sim.py
import time
from datetime import datetime

from sensors_sim import read_all_sensors
from send_sim import send_reading

DEVICE_ID = "pico-sim-001"
LOOP_INTERVAL_SEC = 5  # how often to send readings


def main():
    print("========================================")
    print("  Pico Simulator Started")
    print(f"  Device ID: {DEVICE_ID}")
    print(f"  Interval: {LOOP_INTERVAL_SEC} seconds")
    print("  Target:   /upload on http://127.0.0.1:5000")
    print("========================================")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get fake sensor readings
            reading = read_all_sensors()
            reading["device_id"] = DEVICE_ID

            print(f"[{timestamp}] [SIM] Reading:", reading)

            success, status_code, text = send_reading(reading)

            if success:
                print(f"[{timestamp}] [SIM] Sent -> status {status_code}")
            else:
                print(f"[{timestamp}] [SIM] FAILED to send reading.")

            print("-" * 40)
            time.sleep(LOOP_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n[SIM] Stopped by user.")


if __name__ == "__main__":
    main()
