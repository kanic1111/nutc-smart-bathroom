import dl303_api
import time
import requests
import configparser

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('../config.ini')

registJson = {
    "ip": config["DL303_DEVICE"]["IP"],
    "mac": config["DL303_DEVICE"]["MAC"]
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
    dl303_CO = dl303_api.get_Co()
    dl303_CO2 = dl303_api.get_Co2()
    dl303_RH = dl303_api.get_Humidity()
    dl303_TC = dl303_api.get_Temperature()
    dl303_DC = dl303_api.get_DewPoint()
    dl303_Absolute_RH = round(6.112*(2.718*((17.67*float(dl303_TC))/(float(dl303_TC)+243.5))*float(dl303_RH)*2.1674/(273.15+float(dl303_TC))), 2)
    print('co:', float(float(dl303_CO) + 1), 'co2:', dl303_CO2, 'rh:', dl303_RH, 'tc:', dl303_TC, 'dc:', dl303_DC, 'absolute_rh: ', float(dl303_Absolute_RH))
    try:
        sendStatus = {}
        sendStatus["mac"] = config["DL303_DEVICE"]["MAC"]
        sendStatus["sensorData"] = {}
        sendStatus["sensorData"]["一氧化碳"] = float(dl303_CO) + 1
        sendStatus["sensorData"]["二氧化碳"] = float(dl303_CO2)
        sendStatus["sensorData"]["濕度"] = float(dl303_RH)
        sendStatus["sensorData"]["溫度"] = float(dl303_TC)
        sendStatus["sensorData"]["相對溫度"] = float(dl303_DC)
        sendStatus["sensorData"]["絕對溫度"] = float(dl303_Absolute_RH)
        r = requests.post(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/insert", json=sendStatus)
        print(r.text)
    except:
        pass    
    time.sleep(0.5)