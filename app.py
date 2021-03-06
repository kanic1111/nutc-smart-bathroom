#include <ArduinoJson.h>
int heat_autopin = 5;
int heat_onpin = 4;
int heat_offpin = 3;
int heat_testpin = 2;
int UV_autopin = 12;
int UV_onpin = 11;
int UV_offpin = 10;
int UV_testpin = 9;
int fan_autopin = 13;
int fan_speedpin = A0;
int fan_speed_value;
const int fanControlPin = 6;
const int uvControlPin = 7;
const int heatControlPin = 8;
int fanPreStatus = 0;
int uvPreStatus = 2;
int heatPreStatus = 2;
String jsonreadstatus;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=2;i<6;i++)
  {
    pinMode(i, INPUT_PULLUP);
  }
  for(int i=9;i<13;i++)
  {
    pinMode(i, INPUT_PULLUP);
  }
  pinMode(A0, INPUT);
  pinMode(fanControlPin, OUTPUT);
  pinMode(uvControlPin, OUTPUT);
  pinMode(heatControlPin, OUTPUT); 
  analogWrite(fanControlPin, 0);
  digitalWrite(uvControlPin, 1);
  digitalWrite(heatControlPin, 1);
}

void loop() {
  if(digitalRead(UV_onpin) == HIGH){
    uvPreStatus = 1;
    Serial.println("uv on");
    digitalWrite(uvControlPin,0);
  }
  if(digitalRead(UV_offpin) == HIGH){
    uvPreStatus = 0;
    Serial.println("uv off");
    digitalWrite(uvControlPin,1);
  }
  if(digitalRead(heat_onpin) == HIGH){
    heatPreStatus = 1;
    Serial.println("heat on");
    digitalWrite(heatControlPin,0);
  }
  if(digitalRead(heat_offpin) == HIGH){
    heatPreStatus = 0;
    Serial.println("heat off");
    digitalWrite(heatControlPin,1);
  }
  if(digitalRead(heat_autopin) == HIGH){
    Serial.println("heat_automode");
  }
  if(digitalRead(UV_autopin) == HIGH){
    Serial.println("UV_automode");
  }
  if(digitalRead(fan_autopin) == LOW){
    Serial.println("fan_automode");
  }
  if(digitalRead(fan_autopin) == HIGH){
    Serial.println("fan_contorlmode");
    int A0_read_value = analogRead(fan_speedpin);
    fan_speed_value = (A0_read_value/5)-102 ;
   fanPreStatus = (fan_speed_value+30)/60;
    if( fan_speed_value >= 0){
        fanPreStatus = 1;
       analogWrite(fanControlPin,fan_speed_value+30);
       Serial.print("fan_speedvalue:");
       Serial.println(fan_speed_value+30);
    }
    else{
       analogWrite(fanControlPin,0);
       Serial.print("fan_speedvalue:");
       Serial.println(0);
    }
  }
  String data;
  int count = 0;
  StaticJsonDocument<200> readjson;
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    data = Serial.readString();
    count = data.length();
    char json[count+1];
    data.toCharArray(json, count+1);
    Serial.println(json);
    //  char json[] = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";
    StaticJsonDocument<200> jsonBuffer;
    DeserializationError error = deserializeJson(jsonBuffer, json);
//    Serial.println(); 
    // Test if parsing succeeds.
    if (error) {
//      Serial.print(F("deserializeJson() failed: "));
//      Serial.println(error.c_str());
      return;
    }
    if (jsonBuffer["fan"].is<int>() and (jsonBuffer["fan"] >= 0 or jsonBuffer["fan"] <= 3) and digitalRead(fan_autopin) == LOW ) {
        Serial.print("fan-receiveStatus:");
        Serial.println(int(jsonBuffer["fan"]));
        if (fanPreStatus != jsonBuffer["fan"]){
          fanPreStatus = jsonBuffer["fan"];
          analogWrite(fanControlPin, int(jsonBuffer["fan"])*60);
        }
    }
    
    if (jsonBuffer["uv"].is<int>() and (jsonBuffer["uv"] == 0 or jsonBuffer["uv"] == 1) and digitalRead(UV_autopin) == HIGH ) {
        Serial.print("uv-receiveStatus:");
        Serial.println(int(jsonBuffer["uv"]));
        if (uvPreStatus != jsonBuffer["uv"]){
          uvPreStatus = jsonBuffer["uv"];
          digitalWrite(uvControlPin, !int(jsonBuffer["uv"]));
        }
    }
    
    if (jsonBuffer["heat"].is<int>() and (jsonBuffer["heat"] == 0 or jsonBuffer["heat"] == 1) and digitalRead(heat_autopin) == HIGH) {
        Serial.print("heat-receiveStatus:");
        Serial.println(int(jsonBuffer["heat"]));
        if (heatPreStatus != jsonBuffer["heat"]){
          heatPreStatus = jsonBuffer["heat"];
          digitalWrite(heatControlPin, !int(jsonBuffer["heat"]));
        }
    }
    jsonreadstatus = "";
    serializeJson(jsonBuffer, jsonreadstatus);
  }
  else{
       Serial.println("fan Status:");
       Serial.print(fanPreStatus);
//        Serial.print("uvstatus:");
//        Serial.println(uvPreStatus);
//        Serial.print("heatstatus:");
//        Serial.println(heatPreStatus);
      DeserializationError error =  deserializeJson(readjson, jsonreadstatus);
    if(readjson["uv"].is<int>() and int(readjson["uv"]) != uvPreStatus  and digitalRead(UV_autopin) == HIGH ){
    Serial.println("write uv automode last value");
    uvPreStatus = int(readjson["uv"]);
    digitalWrite(uvControlPin, !int(readjson["uv"]));    
  }
  if(readjson["heat"].is<int>() and int(readjson["heat"]) != heatPreStatus  and digitalRead(heat_autopin) == HIGH ){
    Serial.println("write heat automode last value");
    heatPreStatus = int(readjson["heat"]);
    digitalWrite(heatControlPin, !int(readjson["uv"]));    
  }
  if(readjson["fan"].is<int>() and int(readjson["fan"]) != fanPreStatus  and digitalRead(fan_autopin) == LOW){
    Serial.println("write fan automode last value");
    fanPreStatus = int(readjson["fan"]);
    analogWrite(fanControlPin, int(readjson["fan"])*60);    
  }
  }
  if(digitalRead(UV_testpin) == HIGH){
    Serial.println("UV Debug Mode:");
    Serial.print("uvstatus:");
    Serial.println(uvPreStatus);
  }
  if(digitalRead(heat_testpin) == HIGH){
    Serial.println("heat Debug Mode:");
    Serial.print("heatstatus:");
    Serial.println(heatPreStatus);
  }
  Serial.println(jsonreadstatus);
//  Serial.print(int(readjson["uv"]));
//  Serial.print("==========");
delay(1000);
}
