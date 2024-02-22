import time
import board
import busio
import datetime
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bh1750
from collections import namedtuple
import RPi.GPIO as GPIO
from Sensor import *
#ec,pH = I2C [SDA SCL set 1]

"""

lib DHT 11 must delay at least 1 sec

"""
class MainControl:
    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        print("main")
        self.ads_ec = ADS.ADS1115(self.i2c)
        self.chan_ec = AnalogIn(self.ads_ec, ADS.P0)
        self.ec_sensor = ECSensor(self.ads_ec, self.chan_ec)
        
        
        self.ads_ph = ADS.ADS1115(self.i2c)
        self.chan_ph = AnalogIn(self.ads_ph, ADS.P1)
        self.ph_sensor = PHSensor(self.ads_ph, self.chan_ph)
        
        
        self.intensity_sensor = IntensitySensor(self.i2c)
        self.temp_and_humidity = TemperatureSensor() #
        
        self.EC_before = 0
        self.pH_before = 0
        self.delay = 0
        self.state = 1
        
        self.state_dimming = True
        
    def Mixfertilizer(self,ECvalue,pHvalue):
        pH_pump = 27
        EC_pump_A = 17
        EC_pump_B = 22
        wather_pump = 26
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pH_pump, GPIO.OUT)
        GPIO.setup(EC_pump_A, GPIO.OUT)
        GPIO.setup(EC_pump_B, GPIO.OUT)
        GPIO.setup(wather_pump, GPIO.OUT)
        
        if self.ph_sensor.read_ph_value() < 4.05:
            self.state = 1
            
        if self.state == 1: 
            if self.pH_before == 0:
                self.pH_before = self.ph_sensor.read_ph_value()
            elif self.ph_sensor.read_ph_value() <= self.pH_before + 0.5:
                self.delay += 0.5
            
             
            if 5.5 < self.ph_sensor.read_ph_value() < pHvalue:
                print("pH pump is woking")
                GPIO.output(pH_pump, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(pH_pump, GPIO.HIGH)
            else:
                print("pH pump is stop")
                GPIO.output(pH_pump, GPIO.HIGH)
                self.delay = 1
                self.state = 2

            
        if self.state == 2:
            if self.EC_before == 0:
                self.EC_before = self.ec_sensor.read_ec_value()
            elif self.ec_sensor.read_ec_value() <= self.EC_before + 0.5:
                self.delay += 0.5
                print(self.delay)
            
            if self.ec_sensor.read_ec_value() <= ECvalue:
                
                print("pump A and B is woking")
                GPIO.output(EC_pump_A, GPIO.LOW)
                GPIO.output(EC_pump_B, GPIO.LOW)
                time.sleep(self.delay)
                GPIO.output(EC_pump_A, GPIO.HIGH)
                GPIO.output(EC_pump_B, GPIO.HIGH)
                
            elif self.ec_sensor.read_ec_value() >= ECvalue + 0.2:
                
                print("water pump is woking")
                GPIO.output(wather_pump, GPIO.LOW)
                time.sleep(self.delay)
                
            else:
                GPIO.output(EC_pump_A, GPIO.HIGH)
                GPIO.output(EC_pump_B, GPIO.HIGH)
                GPIO.output(wather_pump, GPIO.HIGH)
                self.delay = 1
                print("stop all pump")
                
                
        GPIO.cleanup()

    def Dimming(self,IntensityValue):
        Intensity_pin_ON = 5
        Intensity_pin_OFF = 6
        LED = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Intensity_pin_ON, GPIO.OUT)
        GPIO.setup(Intensity_pin_OFF, GPIO.OUT)
        print("Dimming")
        if self.intensity_sensor.read_intensity_value() < IntensityValue  and self.state_dimming:
            GPIO.output(Intensity_pin_ON, GPIO.HIGH)
            GPIO.output(Intensity_pin_OFF, GPIO.LOW)
            time.sleep(4)
            
            GPIO.output(Intensity_pin_ON, GPIO.LOW)
            GPIO.output(Intensity_pin_OFF, GPIO.LOW)
            GPIO.cleanup()
            self.state_dimming = False
        elif self.intensity_sensor.read_intensity_value() > IntensityValue  and self.state_dimming == False:
            GPIO.output(Intensity_pin_ON, GPIO.LOW)
            GPIO.output(Intensity_pin_OFF, GPIO.HIGH)
            time.sleep(3.6)
            
            GPIO.output(Intensity_pin_ON, GPIO.LOW)
            GPIO.output(Intensity_pin_OFF, GPIO.LOW)
            GPIO.cleanup()
            self.state_dimming = True
            
        current_time = datetime.datetime.now()
        hour = current_time.hour
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED, GPIO.OUT)
        if  10 <= hour <= 16:
            intensity_low = (IntensityValue / 100) * 40
            if self.intensity_sensor.read_intensity_value() < intensity_low:
                GPIO.output(LED, GPIO.LOW)
            else:
                GPIO.output(LED, GPIO.HIGH)
                GPIO.cleanup()
                
    
    def ControlTemperature(self,Temp,Humi):
        Fan_pin = 19
        flogging_pin = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Fan_pin, GPIO.OUT)
        
        if self.temp_and_humidity.read_temperature() > 0.0 and self.temp_and_humidity.read_humidity() > 0.0 :

            if  self.temp_and_humidity.read_temperature() > float(Temp):
                GPIO.output(Fan_pin, GPIO.LOW)
                print("fan on")

            elif self.temp_and_humidity.read_temperature() < float(Temp):
                GPIO.output(Fan_pin, GPIO.HIGH)
                print("fan off")
                GPIO.cleanup()

            if self.temp_and_humidity.read_humidity() < float(Humi):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(flogging_pin, GPIO.OUT)
                GPIO.output(flogging_pin, GPIO.LOW)
                time.sleep(10)
                GPIO.output(flogging_pin, GPIO.HIGH)

                GPIO.cleanup()
    
    def Clear_output(self):
        pH_pump = 27
        EC_pump_A = 17
        EC_pump_B = 22
        wather_pump = 26
        
        Intensity_pin_ON = 5
        Intensity_pin_OFF = 6
        LED = 13
        
        Fan_pin = 19
        flogging_pin = 0
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(pH_pump, GPIO.OUT)
        GPIO.setup(EC_pump_A, GPIO.OUT)
        GPIO.setup(EC_pump_B, GPIO.OUT)
        GPIO.setup(wather_pump, GPIO.OUT)
        GPIO.setup(Intensity_pin_ON, GPIO.OUT)
        GPIO.setup(Intensity_pin_OFF, GPIO.OUT)
        GPIO.setup(LED, GPIO.OUT)
        GPIO.setup(Fan_pin, GPIO.OUT)
        GPIO.setup(flogging_pin, GPIO.OUT)
        
        GPIO.output(pH_pump, GPIO.HIGH)
        GPIO.output(EC_pump_A, GPIO.HIGH)
        GPIO.output(EC_pump_B, GPIO.HIGH)
        GPIO.output(wather_pump, GPIO.HIGH)
        
        GPIO.output(Intensity_pin_ON, GPIO.LOW)
        GPIO.output(Intensity_pin_OFF, GPIO.LOW)
        GPIO.output(LED, GPIO.HIGH)
        GPIO.output(flogging_pin, GPIO.HIGH)
        GPIO.output(Fan_pin, GPIO.HIGH)
        
        GPIO.cleanup()
        
        
            
    def Test(self):
        print("EC:{:0.2f}".format(self.ec_sensor.read_ec_value()))
        #print("caribrate ec:{:0.2f}".format(self.ec_sensor.calibration(25)))
        #print(self.chan_ph.voltage)
        print("pH:{:0.2f}".format(self.ph_sensor.read_ph_value()))
        print("Intensity:{:0.2f}".format(self.intensity_sensor.read_intensity_value()))
        
        print("Temp:{:0.2f}".format(self.temp_and_humidity.read_temperature()))
        print("Humi:{:0.2f}".format(self.temp_and_humidity.read_humidity()))
    
    def Return_value(self):
        ec = self.ec_sensor.read_ec_value()
        ph = self.ph_sensor.read_ph_value()
        intensity = self.intensity_sensor.read_intensity_value()
        
        temp = 0
        Humi = 0
        while temp == 0 and Humi == 0:
            temp = self.temp_and_humidity.read_temperature()
            Humi = self.temp_and_humidity.read_humidity()
        return {'ec': ec,'ph': ph,'intensity': intensity,'temp': temp,'humi': Humi}
        #return {'ec':round(ec, 2),'ph':round(ph, 2),'intensity':round(intensity, 2),'temp':round(temp, 2),'humi':round(Humi, 2)}
        
        
        
def turn_on():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
def turn_off():
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)

if __name__ == "__main__":
    
    
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(0, GPIO.OUT)
    #GPIO.setup(6, GPIO.OUT)
    #turn_on()
    GPIO.output(0, GPIO.LOW)
    #GPIO.output(22, GPIO.LOW)
    time.sleep(5)
    GPIO.output(0, GPIO.HIGH)
    #GPIO.output(22, GPIO.HIGH)
    #turn_on()
    #time.sleep(3.6)

    #GPIO.cleanup()

        # Clean up GPIO settings
    '''
    a = MainControl()
    a.Clear_output()
    '''
    while True:

        
        a.Test()
        #a.Mixfertilizer(2.6,6.2)
        #a.ControlTemperature(27,40)
        #a.Dimming(65)
        print(a.Return_value())
        time.sleep(1)
        print()
    '''
    
    
    
    
    
    
    
    