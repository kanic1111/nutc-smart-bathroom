import configparser
import requests
import time
import serial
import json
import datetime


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

registJson = {
    "ip": config["LOCAL_DEVICE"]["IP"],
    "mac": config["LOCAL_DEVICE"]["MAC"]
}

referenceJson = {"濕度": 0}
# 風扇段數 0 關 / 3 最強
readStatusJson = {"UV燈": 0, "加熱器": 0, "風扇": 0, "人員": 0}
controlJson = {"UV燈": 0, "加熱器": 0, "風扇": 0, "人員": 0}
preStatusJson = {"UV燈": 0, "加熱器": 0, "風扇": 0, "人員": 0}

uvStatusArray = ["開啟", "關閉"]
heatStatusArray = ["開啟", "關閉"]
fanStatusArray = ["關閉", "初速", "中速", "全速"]
humanStatusArray = ["無人", "有人"]

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
        arduino = serial.Serial(config["LOCAL_DEVICE"]["SERIAL"])
        print(str(datetime.datetime.now()) + "\tSerial Open")
        portOpen = not portOpen 
    except:
        print(str(datetime.datetime.now()) + "\tRetry Open Serial")
        time.sleep(3)

startTimeStamp = ""
stopTimeStamp = ""

while(True):
    print(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    r = requests.get(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    print(r.text)
    for x in range(0, len(r.json())):
        # print(r.json()[x].get('name'))
        # print(r.json()[x].get('value'))
        if (r.json()[x].get('name') == "相對濕度"):
            referenceJson["濕度"] = r.json()[x].get('value')
        if (r.json()[x].get('name') == "溫度"):
            referenceJson["溫度"] = r.json()[x].get('value')


    # readStatusJson = arduino.read()
    controlJson = {"UV燈": 0, "加熱器": 0, "人員": 0}

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

    if (preStatusJson["人員"] == 1 and readStatusJson["人員"] == 0):
        mode = 0
    elif (preStatusJson["人員"] == 0 and readStatusJson["人員"] == 0):
        mode = 1
    elif (readStatusJson["人員"] == 1):
        if (referenceJson["濕度"] > 85):
            mode = 2
        elif (referenceJson["濕度"] < 65):
            mode = 3
        preStatusJson["人員"] = 1
    elif (referenceJson["濕度"] >= 85 or referenceJson["溫度"] >= 35):
        mode = 4
    else: mode = 5

    if (mode == 0):
        if (startTimeStamp == ""):
            # 設定時間戳做完參考
            startTimeStamp = datetime.datetime.now()
            stopTimeStamp = datetime.datetime.now() + datetime.timedelta(minutes=15)
        elif (stopTimeStamp + datetime.timedelta(minutes=15) < datetime.datetime.now()):
            # 經過 15 分鐘的半速後進行無人模式
            preStatusJson["人員"] == 0
        elif (stopTimeStamp < datetime.datetime.now())
            # 人走後 10 分鐘降為半速
            # controlMode = 5
        elif (startTimeStamp + datetime.timedelta(minutes=5) < datetime.datetime.now()):
            # 人走後 5 分鐘使用全速
            # controlMode = 6
    elif (mode != 1):
        # 非 模式 0 且非模式 1 時清除時間戳。
        recordTimeStamp = ""

    if (mode == 1):
        # UV 燈啟動 / 風扇啟動 (10min/1hr)
        if (startTimeStamp == ""):
            # 設定時間戳做完參考，開啟 UV 燈及風扇。
            # controlMode = 5
            startTimeStamp = datetime.datetime.now()
            stopTimeStamp = datetime.datetime.now() + datetime.timedelta(minutes=10)
        elif ((startTimeStamp + datetime.timedelta(hours=1)) < datetime.datetime.now()):
            # 刷新每小時的時間戳，啟動目前的風扇狀態。
            startTimeStamp = ""
        elif (stopTimeStamp < datetime.datetime.now())
            # 開啟 10 分鐘風扇後關閉
            # controlMode = 4
    elif (mode != 0): 
        # 非 模式 0 且非模式 1 時清除時間戳。
        recordTimeStamp = ""
        
        
    if (mode == 2):
        # 浴室有人，濕度 85 up
        # controlMode = 8
    if (mode == 3):
        # 浴室有人，濕度 65 down
        # controlMode = 7
    if (mode == 4):
        # 濕度 85 up / 溫度 35 up
        # controlMode = 2

    if (readStatusJson["人員"] == 1):
        preStatusJson["人員"] == 1

    print("controlMode", controlMode)
    time.sleep(0.5)




