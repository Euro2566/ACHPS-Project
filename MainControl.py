import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bh1750
from collections import namedtuple

from Sensor import *

class MainControl:
    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.ads_ec = ADS.ADS1115(self.i2c)
        self.chan_ec = AnalogIn(self.ads_ec, ADS.P0)
        self.ec_sensor = ECSensor(self.ads_ec, self.chan_ec)

        self.ads_ph = ADS.ADS1115(self.i2c, address=0x49)
        self.chan_ph = AnalogIn(self.ads_ph, ADS.P1)
        self.ph_sensor = PHSensor(self.ads_ph, self.chan_ph)

        self.ads_intensity = ADS.ADS1115(self.i2c, address=0x4A)
        self.chan_intensity = AnalogIn(self.ads_intensity, ADS.P2)
        self.intensity_sensor = IntensitySensor(self.i2c)
    
