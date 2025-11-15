# main.py — main loop for real Pico sensor → server uploads
import time
import network
from sensors import init_sensors, read_all
from send import send_payload

DEVICE_ID = "pico-wh-001"
INTERVAL_SEC = 5

def wait_for_network():
    wlan = network.WLAN(network.STA_IF)
    while not wlan.isconnected():
        print("Waiting for Wi-Fi...")
        time.sleep(1)
    print("Wi-Fi OK:", wlan.ifconfig()[0])

def main():
    wait_for_network()

    aht = init_sensors()
    print("AHT20 sensor initialized ✓")

    while True:
        reading = read_all(aht)
        reading["device_id"] = DEVICE_ID

        print("Reading:", reading)

        ok = send_payload(reading)
        if ok:
            print("Upload OK ✓")
        else:
            print("Upload FAILED ✗")

        print("-" * 40)
        time.sleep(INTERVAL_SEC)

main()
