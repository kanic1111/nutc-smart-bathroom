#include <DHT.h>

#define DHTPIN 2     
#define DHTTYPE DHT22   // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
//    Serial.println(F("Failed to read from DHT11 sensor!"));
    return;
  }
  float absolute_humi = (6.112*(2.718*((17.67*t)/(t+243.5))*h*2.1674/(273.15+t)));
  Serial.print("{\"humidity\": ");
  Serial.print(h);
  Serial.print(", \"temperature\": ");
  Serial.print(t);
  Serial.print(", \"absolute_humidity\": ");
  Serial.print(absolute_humi);
  Serial.println("}");
  delay(1000);
}
