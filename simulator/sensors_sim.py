# sensors_sim.py
import random
import time
import math

def read_temp():
    """
    Simulate temperature (°C).
    Around 22–28°C with small noise and slow variation.
    """
    base = 25
    # slow drift + random noise
    drift = 2 * math.sin(time.time() / 300.0)  # 10-minute-ish cycle
    noise = random.uniform(-0.5, 0.5)
    return round(base + drift + noise, 2)


def read_humidity():
    """
    Simulate humidity (%).
    Around 40–60% with noise.
    """
    base = 50
    drift = 5 * math.sin(time.time() / 600.0)
    noise = random.uniform(-2, 2)
    return round(base + drift + noise, 1)


def read_pressure():
    """
    Simulate pressure (hPa).
    Around 1005–1020 hPa.
    """
    base = 1013
    noise = random.uniform(-5, 5)
    return round(base + noise, 1)


def read_light():
    """
    Simulate light level (arbitrary units).
    0–1000 range with quick noise.
    """
    return round(random.uniform(100, 900), 0)


def read_all_sensors():
    """
    Return a dict matching your DB schema / Flask JSON payload.
    """
    return {
        "temp": read_temp(),
        "humidity": read_humidity(),
        "pressure": read_pressure(),
        "light": read_light(),
    }
