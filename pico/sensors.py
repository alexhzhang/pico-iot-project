# sensors.py — handles all Pico sensor readings
from machine import Pin, I2C
from aht20 import AHT20

def init_sensors():
    # I2C0: SDA on GP0, SCL on GP1
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    aht = AHT20(i2c)
    return aht

def read_all(aht):
    """Return a dict of all sensor values."""
    t, h = aht.read()

    return {
        "temp": round(t, 2),
        "humidity": round(h, 2),
        "pressure": None,   # AHT20 has no pressure
        "light": None       # You can add sensors later
    }
