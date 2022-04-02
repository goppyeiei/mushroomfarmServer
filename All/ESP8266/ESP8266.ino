

#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include "DHT.h"

#define DHTPIN D2     // what digital pin we're connected to
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "12345";
const char* password = "123456789";
int i = 0;
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

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  if (WiFi.status() == WL_CONNECTED){
   WiFiClient client;
   HTTPClient http;

   float hic = dht.computeHeatIndex(temperature, humidity, false);
   Serial.println(humidity);
   Serial.println(temperature);
   Serial.println("---------------------!");
 
   http.begin(client, "http://139.59.249.192/data/farm1/esp8266/"+String(temperature)+"/"+String(humidity) );
   http.GET();
   http.end();

  
   delay(10000);
  }
}
