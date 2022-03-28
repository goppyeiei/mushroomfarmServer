#include <DHT.h>
#include <DHT_U.h>

#include <dummy.h>

#include <WiFi.h>
#include "DHT.h"
#include <HTTPClient.h>

#define DHTPIN 27     // what digital pin we're connected to
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Goppy";
const char* password = "123456789";
const int farm_id = 1020;
uint32_t notConnectedCounter = 0;
void setup () {

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(100);
    notConnectedCounter++;
    if(notConnectedCounter > 150) { // Reset board if not connected after 5s
        Serial.println("Resetting due to Wifi not connecting...");
        ESP.restart();
    }
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
    Serial.println(humid);
    Serial.println(temp);
    http.begin(client, "http://139.59.249.192/sent/" + String(farm_id) + "/" + String(temp) + "/" + String(humid) );
    http.GET();
    http.end();
    Serial.println("Sent");


    delay(5000);
  } else {
    Serial.println("restart");
    ESP.restart();
  }
}
