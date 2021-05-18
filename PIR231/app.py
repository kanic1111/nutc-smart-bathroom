# -*- coding: utf-8 -*-
import PIR231_api
import time
import requests
import configparser

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('/home/pi/nutc-smart-bathroom/config.ini')

registJson = {
    "ip": config["PIR231_DEVICE"]["IP"],
    "mac": config["PIR231_DEVICE"]["MAC"]
}

gcpRegist = 0

while(gcpRegist == 0):
    try:
        # print(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/devices")
        r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/devices", json=registJson)
        print("GCP Device Regist Status:", r.json()["status"])
        gcpRegist = 1
    except:
        print("GCP Device Regist Error")
    time.sleep(5)

while(True):
    try:
    	# PIR231_CO = PIR231_api.get_Co()
    	# PIR231_CO2 = PIR231_api.get_Co2()
        PIR231_RH = PIR231_api.get_Humidity()
        PIR231_TC = PIR231_api.get_Temperature()
        PIR231_DC = PIR231_api.get_DewPoint()
        PIR231_Absolute_RH = round(6.112*(2.718*((17.67*float(PIR231_TC))/(float(PIR231_TC)+243.5))*float(PIR231_RH)*2.1674/(273.15+float(PIR231_TC))), 2)
        PIR231_PIR = PIR231_api.get_PIR()
        # print(PIR231_PIR)
        print('rh:', PIR231_RH, 'tc:', PIR231_TC, 'dc:', PIR231_DC, 'absolute_rh: ', float(PIR231_Absolute_RH),'人員',PIR231_PIR)
        try:
            sendStatus = {}
            sendStatus["mac"] = config["PIR231_DEVICE"]["MAC"]
            sendStatus["sensorData"] = {}
        # sendStatus["sensorData"]["一氧化碳"] = float(PIR231_CO) + 1
        # sendStatus["sensorData"]["二氧化碳"] = float(PIR231_CO2)
            sendStatus["sensorData"]["相對濕度"] = float(PIR231_RH)
            sendStatus["sensorData"]["環境溫度"] = float(PIR231_TC)
            sendStatus["sensorData"]["露點溫度"] = float(PIR231_DC)
            sendStatus["sensorData"]["絕對濕度"] = float(PIR231_Absolute_RH)
            sendStatus["sensorData"]["人員"] = PIR231_PIR
            r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/insert", json=sendStatus)
            print(r.text)
        except:
            print("Error")
            pass
    except:    
        time.sleep(0.5)
