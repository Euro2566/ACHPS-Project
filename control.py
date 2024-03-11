import requests
import datetime
import subprocess

from hist2 import *
from Maincontroller import *


url = "https://92f1-171-103-193-214.ngrok-free.app"
sn_farm = "r1"

def test():
    url_crop = "/parameter"
    response = requests.get(url + url_crop)
    data = response.json()
    for i in data:
        print(i)

def check_wifi_connection():
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        output = result.stdout
        if "ESSID" in output:
            return "Connected to WiFi"
        else:
            return "Not connected to WiFi"
    except Exception as e:
        return "Error:", e

def getEnvaronment(sn_farm):
    url_crop = "/myfarm"
    url_enveronment = "/environment/"
    #parameter_return = None
    
    response = requests.get(url + url_crop)
    if response.status_code == 200:
        
        data = response.json()
        for sn_f in data:
            if sn_f["SN_farm"] == sn_farm:
            
                CropID = str(sn_f["CropID"])
                response = requests.get(url + url_enveronment + CropID)
                parameter_data = response.json()
                return parameter_data[0]
                
                '''
                for parameter_data_use in parameter_data:
                    if parameter_data_use['CropID'] == CropID:
                        parameter_return = parameter_data_use
                        return parameter_return          
                '''
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return "Failed connect"
                        
                

def updateParameter(sn_farm, ECvalue, pHvalue, IntensityValue, Temperature, Humidity, ImageResult):
    url_crop = "/myfarm"
    url_put_parameter = "/editparameter"
    
    response = requests.get(url + url_crop)

    if response.status_code == 200:

        data = response.json()
        
        for sn_f in data:
            if sn_f["SN_farm"] == sn_farm:
                CropID = sn_f["CropID"]
                data_to_send = {
                    'ECvalue': ECvalue,
                    'pHvalue': pHvalue,
                    'CropID':CropID,
                    'IntensityValue': IntensityValue,
                    'TempValue':Temperature,
                    'HumiValue':Humidity,
                    'ImageResult': ImageResult
                }

                #HTTP PUT request
                response = requests.post(url + url_put_parameter, json=data_to_send)

                if response.status_code == 200:
                    print("Data successfully updated.")
                    break
                else:
                    print("Failed to update data. Status code:", response.status_code)
                    break
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        


#processing_img()
#print(getEnvaronment(sn_farm))
#updateParameter(sn_farm, 1, 6, 150, 28, 40, 80)
#test()


oldHour = None
imgresult = None
state_mixer = True
state_read = True
state_error = False

status_controller_error = True
while status_controller_error:
    try:
        controller = MainControl()
        status_controller_error = False
    except:
        status_controller_error = True

while 1:
    status = check_wifi_connection()

    if status == "Connected to WiFi" and state_error == False:
        try:
            print("1")
            parameter_use = getEnvaronment(sn_farm)
            state_read = True
            
            if type(parameter_use) == str:
                print("2")
                if parameter_use == "Failed connect":
                    state_error = True
                    
            else:
                state_error = False
                
        except:
            state_read = False
            state_error = True
            
        while status == "Connected to WiFi" and state_read and state_error == False:
            try:
                status = check_wifi_connection()
                
                current_time = datetime.datetime.now()
                hour = current_time.hour
                minute = current_time.minute
                
                if (hour == 6 and minute <= 30):
                    parameter_use = getEnvaronment(sn_farm)
                    
                    command = "sudo fswebcam -r --no-banner /home/pi/testimage/test.jpg"
                    subprocess.run(command, shell=True)
                    imgresult = processing_img()
                    state_mixer = True
                    

                if (hour == 18 and minute <= 30) and state_mixer:
                    if imgresult == "linear phase":
                        controller.Mixfertilizer((parameter_use["EC"]/100)*80,parameter_use["pH"])
                    
                    else:
                        controller.Mixfertilizer(parameter_use["EC"],parameter_use["pH"])
                elif (hour >= 18 and minute > 30) and state_mixer:
                    controller.Clear_output()
                    state_mixer = False

                controller.ControlTemperature(parameter_use["Temperature"],parameter_use["Humidity"])
                controller.Dimming(parameter_use["Intensity"])

                if (hour != oldHour):
                    oldHour = hour
                    post_parameter = controller.Return_value()
                    print(post_parameter)
                    
                    if imgresult == None:
                        command = "sudo fswebcam -r --no-banner /home/pi/testimage/test.jpg"
                        subprocess.run(command, shell=True)
                        imgresult = processing_img()
                        updateParameter(sn_farm, post_parameter["ec"], post_parameter["ph"], post_parameter["intensity"], int(post_parameter["temp"]), int(post_parameter["humi"]),'stady state phase')
                    else:
                        updateParameter(sn_farm, post_parameter["ec"], post_parameter["ph"], post_parameter["intensity"], int(post_parameter["temp"]), int(post_parameter["humi"]), 'stady state phase')
            except:
                controller.Clear_output()
                print("error")
                break
    else:
        controller.ControlTemperature(27, 70)
        controller.Dimming(2000)
        state_error = False

                
            
