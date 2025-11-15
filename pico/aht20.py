# aht20.py — MicroPython driver for AHT20
import time

class AHT20:
    def __init__(self, i2c, address=0x38):
        self.i2c = i2c
        self.address = address
        self._init()

    def _init(self):
        # Soft reset
        try:
            self.i2c.writeto(self.address, b'\xBA')
            time.sleep_ms(20)
        except:
            pass

        # Calibrate
        self.i2c.writeto(self.address, b'\xBE\x08\x00')
        time.sleep_ms(10)

    def read(self):
        """Returns (temperature_C, humidity_percent)"""
        self.i2c.writeto(self.address, b'\xAC\x33\x00')
        time.sleep_ms(80)

        data = self.i2c.readfrom(self.address, 6)

        h_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        t_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = (h_raw / 1048576) * 100
        temperature = (t_raw / 1048576) * 200 - 50

        return temperature, humidity
