#include <dummy.h>

#include <WiFi.h>
#include "DHT.h"
#include <HTTPClient.h>

#define DHTPIN 27     // what digital pin we're connected to
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "12345";
const char* password = "123456789";
const int farm_id = 1;

void setup () {

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.print("Connecting..");
  }

  Serial.println("Connected");
  dht.begin();
}

void loop() {

  int humid = dht.readHumidity();
  float temp = dht.readTemperature();

  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    Serial.println(humid, temp);
    http.begin(client, "http://139.59.249.192/sent/" + String(farm_id) + "/" + String(temp) + "/" + String(humid) );
    http.GET();
    http.end();
    Serial.println("Sent");


    delay(5000);
  }
}
