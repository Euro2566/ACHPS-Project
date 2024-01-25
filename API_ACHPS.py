from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import mysql.connector
from Model import User, CROP, Controller, Environment, ParaMeter, login_para


app = FastAPI()
host = "localhost"
user = "root"
password = ""
db = "achps_db"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # สามารถแก้ไขเป็นรายชื่อเซิร์ฟเวอร์ที่ได้รับอนุญาต
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/Read")
def read():
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM environment")
    myresult = mycursor.fetchall()
    return myresult

#ที่ใช้งาน
@app.post("/login")
def login(EandP:login_para):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    if (EandP.email == "" or EandP.Pass == ""):
        return {"error": "password or email is Null"}
    else:
        sql = "SELECT * FROM user WHERE Email = %s AND password = %s"
        val = (EandP.email, EandP.Pass)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if (myresult == []):
            return {"User_id": "Null"}
        else:
            return myresult[0]

@app.post("/register")
def register(userData: User):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM user WHERE Email = %s"
    val = (userData.email,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if(myresult != []):
        return {"status": "non success", "message": "db has Email"}
    else:
        mycursor = mydb.cursor()
        sql = "INSERT INTO user (User_id, name, Email, password, Phone, User_Img) VALUES (NULL, %s, %s, %s, %s, %s)"
        val = (userData.name, userData.email, userData.Pass, userData.phone, userData.user_img)
        mycursor.execute(sql, val)
        mydb.commit()
        return {"status": "success", "message": "User registered successfully"}


@app.get("/myfarm/{userID}")
def myfarm(userID:str):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM crop WHERE User_id = %s"
    val = (userID,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

@app.post("/CreateFarm")
def CreateFarm(crop: CROP):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM crop WHERE CropName = %s AND User_id = %s"
    val = (crop.cropName, crop.user_id)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    if(myresult != []):
        return {"status": "non success", "message": "db has a farm name and user_id"}
    else:
        sql = "SELECT * FROM crop WHERE SN_farm = %s AND User_id = %s"
        val = (crop.SN_farm, crop.user_id)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if(myresult != []):
            return {"status": "non success", "message": "db has a SN_farm in User_id"}    
        else:
            sql = "SELECT * FROM crop WHERE SN_farm = %s"
            val = (crop.SN_farm,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if(myresult != []):
                return {"status": "non success", "message": "db has a SN_farm"}    
            else:
                mycursor = mydb.cursor()
                sql = "INSERT INTO crop (User_id, CropName, StartDate, SN_farm) VALUES (%s, %s, %s, %s)"
                val = (crop.user_id, crop.cropName, crop.startDate, crop.SN_farm)
                mycursor.execute(sql, val)
                mydb.commit()
                
                mycursor = mydb.cursor(dictionary=True)
                sql = "SELECT * FROM crop WHERE CropName = %s AND SN_farm = %s"
                val = (crop.cropName, crop.SN_farm)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                cr_id = myresult[0]["CropID"]

                sql = "INSERT INTO environment (CropID, Intensity, pH, Temperature, Humidity, Growth, EC) VALUES (%s, 100, %s, 35, 60, 0, %s)"
                val = (cr_id, crop.rangePH, crop.rangeEC)
                mycursor.execute(sql, val)
                mydb.commit()
                
                return {"status": "success", "message": "User registered successfully"}
            
@app.put("/EditProfile/{id}")
def EditProfile(userData:User, id:int):    
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor()
    sql="UPDATE user SET name = %s, password = %s, Phone = %s, User_Img = %s WHERE user.User_id = %s"
    val = (userData.name, userData.Pass, userData.phone, userData.user_img, str(id))
    mycursor.execute(sql, val)
    mydb.commit()
    return {"status": "success"}
           
@app.put("/EditValue/{CropID}")
def EditValue(value:Environment, CropID:int):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor()
    sql="UPDATE environment SET Intensity = %s, pH = %s, Temperature = %s, Humidity = %s, EC = %s WHERE environment.CropID = %s"
    val = (value.intensity, value.ph, value.temperature, value.humidity, value.EC, str(CropID))
    mycursor.execute(sql, val)
    mydb.commit()
    return {"status": "success"}

@app.get("/GetValue/{CropID}")
def GetValue(CropID:str):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM parameter WHERE CropID = %s"
    val = (CropID,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    if(myresult == []):
        return {"status": "non success", "message": "No CropID"}
    else:
        return myresult

@app.get("/GetNontification/{CropID}")
def GetNontification(CropID:str):
    pass

@app.post("/AddParameter")
def AddParameter(parameter:ParaMeter):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor()
    sql = "INSERT INTO parameter (CropID, ECvalue, pHvalue, IntensityValue, TempValue, HumiValue, ImageResult) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (parameter.CropID, parameter.ECvalue, parameter.PHvalue, parameter.IntensityValue, parameter.TempValue, parameter.HumiValue, parameter.ImageResult)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"status": "success"}

@app.post("/Controller")
def controller(Con:Controller):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM crop WHERE SN_farm = %s"
    val = (Con.SN_farm,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    if(myresult != []):
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM controller WHERE CropID = %s"
        val = (myresult[0]["CropID"],)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        crop_id = myresult[0]["CropID"]

        if(myresult == []):
            mycursor = mydb.cursor()
            sql = "INSERT INTO controller (CropID, NitricAcid, SunBlock, Fan, Fogging, LED, WaterPump, NutrientPump) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (crop_id, Con.NitricAcid, Con.SunBlock, Con.fan, Con.fogging, Con.led, Con.WaterPump, Con.NutrientPump)
            mycursor.execute(sql, val)
            mydb.commit()
            return {"status": "success", "message": "Add new row"}
        else:
            mycursor = mydb.cursor()
            sql = "UPDATE controller SET NitricAcid = %s, SunBlock = %s, Fan = %s, Fogging = %s, LED = %s , WaterPump = %s, NutrientPump = %s WHERE controller.CropID = %s"
            val = (Con.NitricAcid, Con.SunBlock, Con.fan, Con.fogging, Con.led, Con.WaterPump, Con.NutrientPump, crop_id)
            mycursor.execute(sql, val)
            mydb.commit()
            return {"status": "success", "message": "Table is update"}
    else:
        return {"status": "no success", "message": "Not found a SN_farm"}
    
@app.get("/GetEnvironment/{Sn_farm}")
def GetEnvironment(Sn_farm:str):
    mydb = mysql.connector.connect(host=host, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM crop WHERE SN_farm = %s"
    val = (Sn_farm,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    crop_id = myresult[0]["CropID"]

    if (myresult != []):
        sql = "SELECT * FROM environment WHERE CropID = %s"
        val = (crop_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult
    else:
        return {"status": "no success", "message": "Not found a SN_farm"}
