from pydantic import BaseModel
from typing import Optional

class login_para(BaseModel):
    email:str
    Pass:str

class User(BaseModel):
    name:str
    Pass:str
    phone:str
    email:str
    user_img:str
    #level: Optional[str] = "nermal"

class CROP(BaseModel):
    user_id:str
    SN_farm:str
    cropName:str
    rangeEC:str
    rangePH:str
    startDate:str

class ParaMeter(BaseModel):
    CropID:str
    ECvalue:str
    PHvalue:str
    TempValue:str
    HumiValue:str
    IntensityValue:str
    ImageResult:str

class Environment(BaseModel):
    EC:str
    intensity:str
    ph:str
    temperature:str
    humidity:str
    growth:str

class Controller(BaseModel):
    SN_farm:str
    NitricAcid:str
    SunBlock:str
    fan:str
    fogging:str
    led:str
    WaterPump:str
    NutrientPump:str



