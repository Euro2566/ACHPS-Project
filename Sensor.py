import time
import busio
import board
import adafruit_dht
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bh1750
from collections import namedtuple

class Sensor:
    def __init__(self, ads, channel):
        self.ads = ads
        self.channel = channel

    def read_value(self):
        raw_value = self.channel.value
        voltage = (raw_value / 32767.0) * 4.096
        return voltage

class ECSensor(Sensor):
    def __init__(self, ads, channel):
        super().__init__(ads, channel)

    def read_ec_value(self):
        voltage = super().read_value()
        ec_value = voltage * 1000  # แปลงเป็น microsiemens/cm (µS/cm)
        return ec_value

class PHSensor(Sensor):
    def __init__(self, ads, channel):
        super().__init__(ads, channel)

    def read_ph_value(self):
        voltage = super().read_value()
        ph_value = -5.70 * voltage + 21.34
        return ph_value

class IntensitySensor:
    def __init__(self, i2c):
        self.i2c = i2c
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def read_intensity_value(self):
        return self.sensor.lux
    

class TemperatureSensor:
    def __init__(self) -> None:
        self.dht_device = adafruit_dht.DHT11(board.D4)

    def read_temperture(self):
        return self.dht_device.temperature
    
    def read_humidity(self):
        return self.dht_device.humiditys