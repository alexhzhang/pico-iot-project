# boot.py — Wi-Fi + WebREPL autostart for Raspberry Pi Pico W (MicroPython)
# 1) Fill in WIFI_* and WEBREPL_PASSWORD below.
# 2) Save this file to the Pico as "boot.py".
# 3) Reboot the Pico, then open https://micropython.org/webrepl and connect.

import network, time
import machine

# ====== CONFIGURE THESE ======
WIFI_SSID = "Pixel_6698"
WIFI_PASSWORD = "whipnaenae"

# WebREPL password must be 4–9 chars (MicroPython requirement)
WEBREPL_PASSWORD = "pico1234"
# =============================

# Basic sanity check for WebREPL password length
if not (4 <= len(WEBREPL_PASSWORD) <= 9):
    raise ValueError("WEBREPL_PASSWORD must be 4–9 characters.")

def connect_wifi(ssid, password, timeout_s=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi SSID:", ssid)
        wlan.connect(ssid, password)

        t0 = time.ticks_ms()
        while (not wlan.isconnected()
               and time.ticks_diff(time.ticks_ms(), t0) < timeout_s * 1000):
            time.sleep(0.25)

    if wlan.isconnected():
        ip, mask, gw, dns = wlan.ifconfig()
        print("Wi-Fi connected ✓")
        print("IP:", ip, " Mask:", mask, " GW:", gw, " DNS:", dns)
        return wlan
    else:
        print("Wi-Fi connection FAILED (timeout).")
        return None

def start_webrepl(password):
    import webrepl
    try:
        webrepl.start(password=password)
        print("WebREPL started ✓  (use https://micropython.org/webrepl)")
        print("Password:", "*" * len(password))
    except Exception as e:
        print("Failed to start WebREPL:", e)

def main():
    time.sleep(0.5)  # Serial stabilization

    wlan = connect_wifi(WIFI_SSID, WIFI_PASSWORD, timeout_s=25)

    if wlan and wlan.isconnected():
        # Optional friendly hostname (supported in recent MicroPython builds)
        try:
            network.hostname("pico-w")
        except Exception:
            pass

        start_webrepl(WEBREPL_PASSWORD)

        print("\nNext steps:")
        print("  1) Open https://micropython.org/webrepl")
        print("  2) Enter the IP shown above")
        print("  3) Connect and enter the password")
    else:
        print("Staying on USB/serial REPL. Fix Wi-Fi config in boot.py and reboot.")

# Run
try:
    main()
except Exception as e:
    print("boot.py error:", e)
    try:
        import webrepl
        webrepl.start(password=WEBREPL_PASSWORD)
        print("WebREPL started anyway for recovery.")
    except Exception:
        pass



#remember: MicroPython automatically executes main.py after boot.py finishes.