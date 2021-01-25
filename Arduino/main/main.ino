#include <ArduinoJson.h>

const int fanControlPin = 6;
const int uvControlPin = 7;
const int heatControlPin = 8;
int fanPreStatus = 0;
int uvPreStatus = 1;
int heatPreStatus = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(fanControlPin, OUTPUT);
  pinMode(uvControlPin, OUTPUT);
  pinMode(heatControlPin, OUTPUT); 
  analogWrite(fanControlPin, 0);
  digitalWrite(uvControlPin, 0);
  digitalWrite(heatControlPin, 0);
}

void loop() {
  String data;
  int count = 0;

  StaticJsonDocument<200> sendJson;

  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    data = Serial.readString();
    count = data.length();
    char json[count+1];
    data.toCharArray(json, count+1);
    Serial.println(json);
    StaticJsonDocument<200> jsonBuffer;
    //  char json[] = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";
    DeserializationError error = deserializeJson(jsonBuffer, json);
    Serial.println(); 
    // Test if parsing succeeds.
    if (error) {
//      Serial.print(F("deserializeJson() failed: "));
//      Serial.println(error.c_str());
      return;
    }
    if (jsonBuffer["fan"].is<int>() and (jsonBuffer["fan"] >= 0 or jsonBuffer["fan"] <= 3)) {
        Serial.print("fan-receiveStatus:");
        Serial.println(int(jsonBuffer["fan"]));
        if (fanPreStatus != jsonBuffer["fan"]){
          fanPreStatus = jsonBuffer["fan"];
          analogWrite(fanControlPin, int(jsonBuffer["fan"])*85);
        }
    }
    
    if (jsonBuffer["uv"].is<int>() and (jsonBuffer["uv"] == 0 or jsonBuffer["uv"] == 1)) {
        Serial.print("uv-receiveStatus:");
        Serial.println(int(jsonBuffer["uv"]));
        if (uvPreStatus != jsonBuffer["uv"]){
          uvPreStatus = jsonBuffer["uv"];
          digitalWrite(uvControlPin, !int(jsonBuffer["uv"]));
        }
    }
    
    if (jsonBuffer["heat"].is<int>() and (jsonBuffer["heat"] == 0 or jsonBuffer["heat"] == 1)) {
        Serial.print("heat-receiveStatus:");
        Serial.println(int(jsonBuffer["heat"]));
        if (heatPreStatus != jsonBuffer["heat"]){
          heatPreStatus = jsonBuffer["heat"];
          digitalWrite(heatControlPin, !int(jsonBuffer["heat"]));
        }
    }
  }
}
