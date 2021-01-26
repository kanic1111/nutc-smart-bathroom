# -*- coding: utf-8 -*-

import configparser
import requests
import time
import serial
import json
import datetime
import PIR231.PIR231_api

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

registJson = {
    "ip": config["LOCAL_DEVICE"]["IP"],
    "mac": config["LOCAL_DEVICE"]["MAC"]
}
mode = 5
referenceJson = {"humid": 0 ,"person":0}
# 風扇段數 0 關 / 3 最強
readStatusJson = {'uv':0, 'heat': 0, 'fan':0}
controlJson = {'uv':0, 'heat': 0, 'fan':0}
preStatusJson = {"UV": 0, "heat": 0, "fan": 0, "person": 0}

# uvStatusArray = ["開啟", "關閉"]
# heatStatusArray = ["開啟", "關閉"]
# fanStatusArray = ["關閉", "初速", "中速", "全速"]
# humanStatusArray = ["無人", "有人"]

gcpRegist = 0
while(not gcpRegist):
    try:
        # print(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/devices")
        r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/devices", json=registJson)
        print(str(datetime.datetime.now()) + "\tGCP Device Regist Status:", r.json()["status"])
        gcpRegist = 1
    except:
        print(str(datetime.datetime.now()) + "\tGCP Device Regist Error")
        time.sleep(3)

portOpen = 0

while (not portOpen):
    try:
        print(str(datetime.datetime.now()) + "\tSerial try Open")
        arduino = serial.Serial(config["LOCAL_DEVICE"]["SERIAL"],9600)
        print(str(datetime.datetime.now()) + "\tSerial Open")
        portOpen = not portOpen 
    except:
        print(str(datetime.datetime.now()) + "\tRetry Open Serial")
        time.sleep(3)

minstartTimeStamp = ""
minstopTimeStamp = ""
hourstartTimeStamp = ""
hourstopTimeStamp = datetime.datetime.now()
while(True):
    print(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    r = requests.get(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    # print(r.text)
    # re = requests.post('http://127.0.0.1:30001/insert', data = r)
    mac = { "mac" : config["LOCAL_DEVICE"]["MAC"]}
    # print("汶萊資料查看",r.json())
    # for x in range(0, len(r.json())):
        # print(r.json()[x].get('name'))
        # print(r.json()[x].get('value'))
        #    
    # if (r.json()[x].get('name') == "相對濕度"):
    referenceJson["humid"] = float(PIR231.PIR231_api.get_Humidity())
    # print("濕度",referenceJson["濕度"])
    # if (r.json()[x].get('name') == "環境溫度"):
    referenceJson["temp"] = float(PIR231.PIR231_api.get_Temperature())
    # print("溫度",referenceJson["溫度"])
    # if (r.json()[x].get('name') == "人員"):
    preStatusJson["person"] = referenceJson["person"]
    referenceJson["person"] = int(PIR231.PIR231_api.get_PIR())
    # print("人員",referenceJson["人員"])
    referenceJson["absolute_humid"] = round(6.112*(2.718*((17.67*float(referenceJson["temp"]))/(float(referenceJson["temp"])+243.5))*float(referenceJson["humid"])*2.1674/(273.15+float(referenceJson["temp"]))), 2)
    referenceJson["Dew_temp"] = float(PIR231.PIR231_api.get_DewPoint())
        # print(type(referenceJson["人員"]))
    # print(referenceJson)
    # time.sleep(3)

    # define controlMode
    # 純風扇
    # 0 = {'uv':0, 'heat': 0, 'fan':0}
    # 1 = {'uv':0, 'heat': 0, 'fan':1}
    # 2 = {'uv':0, 'heat': 0, 'fan':2}
    # 3 = {'uv':0, 'heat': 0, 'fan':3}
    # UV 燈開
    # 4 = {'uv':1, 'heat': 0, 'fan':0}
    # 5 = {'uv':1, 'heat': 0, 'fan':2}
    # 6 = {'uv':1, 'heat': 0, 'fan':3}
    # 加熱器開
    # 7 = {'uv':0, 'heat': 1, 'fan':0}
    # 8 = {'uv':0, 'heat': 1, 'fan':2}

    if (referenceJson["humid"] <= 65 and referenceJson["temp"] <= 30):
        # 溫度或濕度低於 30 或 65  風扇關 UV關
        if(minstartTimeStamp == ""):
            controlJson["fan"] = 0
    elif(referenceJson["humid"] >= 85 or referenceJson["temp"] >= 35):
            # 如果沒人 風扇都開
        
        controlJson["fan"] = 1 
        # mode = 4
        if(preStatusJson["person"] == 1 and referenceJson["person"] == 0 ):
            #人剛走 而且 溫濕度達標 計時五分鐘全速 十分鐘後 半速 
            mode = 0
    else:
        pass
        #如果上面都沒符合 ex: 濕度介於 65 ~ 85 或 溫度 介於 30 ~ 35  維持原來狀態 底下判斷有沒有人在裡面

    
    if(referenceJson["person"] == 1):
        # 計時全清 有人UV燈關
        mode = 2
        minstartTimeStamp = ""
        minstopTimeStamp = ""  
        controlJson["uv"] = 0 
        if (referenceJson["humid"]>=85):
            # 有人 濕度大於85 加熱器開 UV關
            hourstartTimeStamp = ""
            hourstopTimeStamp = "" 
            controlJson["heat"] = 1  
        if (referenceJson["humid"]<=65):
            # 加熱關
            controlJson["heat"] = 0
    elif(referenceJson["person"] == 0):
        #沒人 UV一律開啟 判斷濕度
        controlJson["uv"] = 1
        controlJson["heat"] = 0 
        # if(referenceJson["濕度"]>=85):
        #     controlJson["fan"] = 1  
            # 沒人 濕度大於85 UV開 加熱關 風扇開
    # print("mode",mode)

    if(minstartTimeStamp == "" and controlJson["fan"] == 0):
        if (hourstartTimeStamp == ""):
            # 設定時間戳做完參考，開啟 UV 燈及風扇。
            # controlMode = 5
            # arduino.write(ControlMode(5).encode())
            # print("controlmode = 5")
            hourstartTimeStamp = datetime.datetime.now()
        if ((hourstartTimeStamp + datetime.timedelta(hours=1)) > datetime.datetime.now()):
            # 刷新每小時的時間戳，啟動目前的風扇狀態。
            controlJson["fan"] = 0 
            hourstopTimeStamp = datetime.datetime.now() + datetime.timedelta(minutes=10)
            print("風扇停止一小時")
        elif (hourstopTimeStamp > datetime.datetime.now()):
            controlJson["fan"] = 1
            print("風扇停止一小時開十分鐘")
            # 開啟 10 分鐘風扇後關閉
            # controlMode = 4
            # arduino.write(ControlMode(4).encode())
        else:
            controlJson["fan"] = 0
            hourstartTimeStamp = ""
            hourstopTimeStamp = ""

    if (mode == 0):
        if (minstartTimeStamp == ""):
            # 設定時間戳做完參考
            minstartTimeStamp = datetime.datetime.now()
            # stopTimeStamp = datetime.datetime.now() + datetime.timedelta(minutes=15)
            minstopTimeStamp = datetime.datetime.now() + datetime.timedelta(minutes=3)
            print("starttime",minstartTimeStamp)
            print("stoptime",minstopTimeStamp)
        elif (datetime.datetime.now() > minstopTimeStamp ):
            #經過15分鐘 將風扇轉速條到1 回去前面判斷溫濕度
            print("經過15分鐘")
            controlJson["fan"] = 1
            minstartTimeStamp = ""
            minstopTimeStamp = ""
            mode = 2

        elif (datetime.datetime.now() > minstartTimeStamp + datetime.timedelta(seconds=10)):
            print("人走後經過5分鐘")
            controlJson["fan"] = 2
            # 人走後 5 分鐘使用全速

    if(controlJson["fan"] >= 1 and hourstopTimeStamp == ""):
        #如果風扇打開 將關閉每小時開十分鐘的計時歸零
        hourstartTimeStamp = ""
        hourstopTimeStamp = ""
    #readStatusJson = {"UV燈": 0, "加熱器": 0, "風扇": 0, "人員": 0}
    referenceJson["UV"] ="ON" if controlJson["uv"] else "OFF"
    referenceJson["heat"] = "ON" if controlJson["heat"] else "OFF"
    if controlJson["fan"] == 1:
        referenceJson["fan"] = "half_speed"
    elif controlJson["fan"] == 2:
        referenceJson["fan"] = "full_speed"
    else:
        referenceJson["fan"] = "closed"
    print("人員上一次狀態",(preStatusJson["person"]))
    # print("人走後時間",minstartTimeStamp)
    # print("每一小時計算時間",hourstartTimeStamp)
    print(referenceJson)
    arduino_data = json.dumps(controlJson)
    arduino.write(arduino_data.encode())
    try:
        sendStatus = {}
        sendStatus["mac"] = config["PIR231_DEVICE"]["MAC"]
        sendStatus["sensorData"] = {}
        # sendStatus["sensorData"]["一氧化碳"] = float(PIR231_CO) + 1
        # sendStatus["sensorData"]["二氧化碳"] = float(PIR231_CO2)
        sendStatus["sensorData"]["相對濕度"] = referenceJson["humid"]
        sendStatus["sensorData"]["環境溫度"] = referenceJson["temp"]
        sendStatus["sensorData"]["露點溫度"] = referenceJson["Dew_temp"]
        sendStatus["sensorData"]["絕對濕度"] = referenceJson["absolute_humid"]
        sendStatus["sensorData"]["人員"] = referenceJson["person"]
        sendStatus["sensorData"]["UV燈"] = referenceJson["UV"]
        sendStatus["sensorData"]["加熱器"] = referenceJson["heat"]
        sendStatus["sensorData"]["風扇"] = referenceJson["fan"]
        r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/insert", json=sendStatus)
        print(r.text)
    except:
        print("Error")
        pass
    print("人員上一次狀態",(preStatusJson["person"]))
    # print("人走後時間",minstartTimeStamp)
    # print("每一小時計算時間",hourstartTimeStamp)
    print("現在狀態",controlJson)
    print("讀取狀態",readStatusJson)
    if(controlJson != readStatusJson):
        readStatusJson = controlJson.copy()
        print("控制寫入arduino")
        arduino_data = json.dumps(controlJson)
        # print(arduino_data)
        arduino.write(arduino_data.encode())
    time.sleep(3)


