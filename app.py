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


referenceJson = {}
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

while(True):
    print(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    r = requests.get(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/query/" + config["CLOUD_DEVICE"]["MAC"])
    print(r.text)
    for x in range(0, len(r.json())):
        print(r.json()[x].get('name'))
        print(r.json()[x].get('value'))
        # if (r.json()[x].get('name') == "light"):
        #     referenceData = int(r.json()[x].get('value'))
    
    
    
    print("controlJson", controlJson)
    # if (preStatusJson["fan"] != controlJson["fan"]):
    #     try:
    #         print("serial open")
    #         arduino = serial.Serial(config["LOCAL_DEVICE"]["SERIAL"])
    #         time.sleep(3)
    #         arduino.write(str(json.dumps(controlJson) + "\\n").encode('utf-8'))
    #         arduino.close()
    #         preStatusJson = {}
    #         preStatusJson["fan"] = controlJson["fan"]
    #         time.sleep(10)
    #     except:
    #         pass
    # try:
    #     sendStatus = {}
    #     sendStatus["mac"] = config["LOCAL_DEVICE"]["MAC"]
    #     sendStatus["sensorData"] = {}
    #     if preStatusJson["fan"] == 1: sendStatus["sensorData"]["fan"] = "進風"
    #     if preStatusJson["fan"] == 0: sendStatus["sensorData"]["fan"] = "關閉"
    #     if preStatusJson["fan"] == -1: sendStatus["sensorData"]["fan"] = "排風"
    #     print(json.dumps(sendStatus))
    #     r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/insert", json=sendStatus)
    #     print(r.text)
    # except:
    #     pass
        
    time.sleep(0.5)




