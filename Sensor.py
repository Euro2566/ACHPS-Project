import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_bh1750
from pigpio_dht import DHT11, DHT22
from collections import namedtuple
from microcontroller import pin


_kvalue = 1.0
_kvalueLow = 1.0
_kvalueHigh = 1.0
_voltage = 0.0
_temperature = 25.0

class Sensor:
    def __init__(self, ads, channel):
        global _kvalueLow
        global _kvalueHigh
        self.ads = ads
        self.channel = channel

    def read_voltage(self):
        raw_value = self.channel.value
        voltage = (raw_value / 32767.0) * 4.096
        return voltage
    
    def read_value(self):
        raw_value = self.channel.value
        return raw_value
        

class ECSensor(Sensor):
    def __init__(self, ads, channel):

        super().__init__(ads, channel)
#1000 microsiemens/centimeter = 550 TDS, parts per million, 550 scale = 0.55
# ec_value*0.55 = tds(ppm)       
    def read_ec_value(self):
        global _kvalueLow
        global _kvalueHigh
        global _kvalue
        temperature = 25
        voltage = super().read_voltage()
        #averageVoltage=voltage*5000/1024
        #ec_value = voltage*1000  # แปลงเป็น microsiemens/cm (µS/cm)
        ec_value = 1000*voltage/820.0/200.0
        valueTemp =ec_value * _kvalue
        if(valueTemp > 2.5):
            _kvalue = _kvalueHigh
        elif(valueTemp < 2.0):
            _kvalue = _kvalueLow
        value = ec_value * _kvalue
        value = value / (1.0+0.0185*(temperature-25.0))
       
        return round(voltage, 2)
    
    def KvalueTempCalculation(self, compECsolution, voltage):
        return 820.0*200.0*compECsolution/1000.0/voltage
    
    def calibration(self, temperature):
        voltage = super().read_value()
        rawEC = 1000*voltage/820.0/200.0
        print(">>>current rawEC is: %.3f" % rawEC)
        if (rawEC > 0.8 and rawEC < 2.1):  # automated 1.413 buffer solution dection
            compECsolution = 1.413*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:1.413us/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'kvalueLow=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:1.413us/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1413,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        elif (rawEC > 2 and rawEC < 3.5):  # automated 2.76 buffer solution dection
            compECsolution = 2.76*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:2.76ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'kvalueHigh=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:2.76ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 276,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        elif (rawEC > 9 and rawEC < 16.8):  # automated 12.88 buffer solution dection
            compECsolution = 12.88*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            print(">>>Buffer Solution:12.88ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'kvalueHigh=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:12.88ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1288,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        else:
            status_msg = ">>>Buffer Solution Error, EC raw: %.3f, Try Again<<<" % rawEC
            print(status_msg)
            cal_res = {'status': 9999, 'status_message': status_msg}
            return cal_res

class PHSensor(Sensor):
    def __init__(self, ads, channel):
        super().__init__(ads, channel)

    def read_ph_value(self):
        voltage = super().read_value()
        rawvoltage = (voltage/ 32767.0) * 4.096
        #newvoltage = rawvoltage               6.86 new else
        
        if rawvoltage > 2.4 and rawvoltage <= 2.69: # 4 newvotage 1
            #print("newvoltage")
            newvoltage = rawvoltage - 1.2525
            
            voltage = (14 * newvoltage)/5
            voltage = voltage
        elif rawvoltage > 2.7: #6.86 new else
            #print("new")
            newvoltage = rawvoltage - 0.9525
            
            voltage = (14 * newvoltage)/5
            voltage = voltage+0.7
        
        else:
            #print("old")
            newvoltage = rawvoltage
            voltage = (14 * newvoltage)/5
            voltage = voltage-0.535
        #print(newvoltage)
        #if pH > 6.5-7
        #voltage = voltage * 0.0004039
        #Formula --- pH = 7 - mV/ 57.14 .
        if newvoltage < 1.63 :
            #voltage = voltage * 0.0007598
            #print ("1")
            voltage = voltage
        else:
            #print("else")
            voltage = voltage+1.3
        _acidVoltage      = 2032.44
        _neutralVoltage   = 1500.0
        #(voltage-1500.0)/3.0
        #ph_value = -5.70 * voltage + 21.34
        """slope     = (7.0-4.0)/((_neutralVoltage-1500.0)/3.0 - (_acidVoltage-1500.0)/3.0)
        intercept = 7.0 - slope*(_neutralVoltage-1500.0)/3.0
        ph_value  = slope*(voltage-1500.0)/3.0+intercept
        ph_value = (voltage-1500.0)/3.0"""
        return round(voltage, 2)

class IntensitySensor:
    def __init__(self, i2c):
        self.i2c = i2c
        self.sensor = adafruit_bh1750.BH1750(i2c)

    def read_intensity_value(self):
        return round(self.sensor.lux, 2)
    

class TemperatureSensor:
    def __init__(self) -> None:
        #self.humidity, self.temperature = Adafruit_DHT.read_retry(11, 4)
        #self.dht_device = adafruit_dht.DHT11(pin.D4,use_pulseio=False)
        self.dht_device = DHT11(4)
        print("read dht")
        self.dht = self.dht_device.read()
        self.temp = 0
        tem = 0
        hum = 0
        self.humi = 0

    def read_temperature(self):
        try:
            self.dht = self.dht_device.read()
            if(self.dht['valid']==True):
                self.temp = self.dht['temp_c']
                tem = self.temp
            else:
                self.temp = tem
            return round(self.temp, 2)
        
        except:
            return round(self.temp, 2)
                
        
    
    def read_humidity(self):
        
        try:
            self.dht = self.dht_device.read()
            if(self.dht['valid']==True):
                self.humi = self.dht['humidity']
                hum = self.humi
            else:
                self.humi = hum
            return round(self.humi, 2)
     
        except:
            return round(self.humi, 2)
        