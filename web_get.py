import configparser 
import requests 
import time 
import serial 
import json 
import datetime 
import PIR231.PIR231_api 
from pymongo import MongoClient
# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

registJson = {
    "ip": config["LOCAL_DEVICE"]["IP"],
    "mac": config["LOCAL_DEVICE"]["MAC"]
}
while(True):
    try:
        r = requests.get(config["GCP"]["SERVER_PROTOCOL"] + "://" + config["GCP"]["SERVER_IP"] + ":" + config["GCP"]["SERVER_PORT"] + "/" "query/"  + config["CLOUD_DEVICE"]["MAC"])
        data = r.text
        data = data.replace("[","").replace("]","")
        data = json.loads(r.text)
        sendStatus = {}
        sendStatus["sensorData"] = {}
        sendStatus["sensorData"]["相對濕度"] = data[0]["value"]
        sendStatus["sensorData"]["環境溫度"] = data[1]["value"]
        sendStatus["sensorData"]["露點溫度"] = data[2]["value"]
        sendStatus["sensorData"]["絕對濕度"] = data[3]["value"]
        sendStatus["sensorData"]["人員"] = data[4]["value"]
        sendStatus["sensorData"]["UV燈"] = data[5]["value"]
        sendStatus["sensorData"]["加熱器"] = data[6]["value"]
        sendStatus["sensorData"]["風扇"] = data[7]["value"]
        sendStatus["sensorData"]["風扇停止時間"] = data[8]["value"]
        print(sendStatus["sensorData"])
        r = requests.post(config["DATASTORAGE_SERVER"]["SERVER_PROTOCOL"] + "://" + config["DATASTORAGE_SERVER"]["SERVER_IP"] + ":" + config["DATASTORAGE_SERVER"]["SERVER_PORT"] + "/insert", json=sendStatus)
        time.sleep(3)
    except:
        print("ERROR")
        time.sleep(2)
