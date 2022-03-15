#include <dummy.h>


#include "DHT.h"

#define DHTPIN 27     // what digital pin we're connected to
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "12345";
const char* password = "123456789";
int i = 0;
const int fan_in = 25;
const int fan_out = 26;
const int water = 33;
void setup () {
 
  Serial.begin(115200);
  pinMode(fan_in, OUTPUT);
  pinMode(fan_out, OUTPUT);
  pinMode(water, OUTPUT);
 
//  WiFi.begin(ssid, password);
// 
//  while (WiFi.status() != WL_CONNECTED) {
// 
//    delay(1000);
//    Serial.print("Connecting..");
// 
//  }
//
//  Serial.println("Connected");
  dht.begin();
 
}

void loop() {

  int humid = dht.readHumidity();
  float temp = dht.readTemperature();
  
//  if (WiFi.status() == WL_CONNECTED){
//   WiFiClient client;
//   HTTPClient http;

   float hic = dht.computeHeatIndex(temp, humid, false);
   Serial.println("Humidity : "+String(humid)+" %");
   Serial.println("Temperature : "+String(temp));


   if (humid >= 75 and humid <= 85 and temp <= 32 and temp >= 30 ){ //ปกติ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, LOW);
    Serial.println("Normal");
   }
   /////////////////////////////////////////////////////////////////////
   else if (humid <= 75 and temp <= 32 and temp >= 30){ //ชื้นต่ำ tempปกติ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, HIGH);
    Serial.println("Humid Low Normal Temp");
   }
   else if (humid <= 75 and temp >= 32 ){ //ชื้นต่ำ tempสูง
    digitalWrite(fan_in, HIGH);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, HIGH);
    Serial.println("Humid Low High Temp");
   }
   else if (humid <= 75 and temp <= 30){ //ชื้นต่ำ tempต่ำ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, HIGH);
    Serial.println("All Low");
   }
   else if (humid >= 75 and humid <= 85 and temp <= 30){ //ชื้นปกติ tempต่ำ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, LOW);
    Serial.println("Low temp Normal Humid");
   }
   /////////////////////////////////////////////////////////////////////
   else if (humid >= 85 and temp <= 32 and temp >= 30){ //ชื้นสูง tempปกติ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, HIGH);
    digitalWrite(water, LOW);
    Serial.println("Humid High Normal Temp");
   }
   else if (humid >= 85 and temp <= 30 ){ //ชื้นสูง tempต่ำ
    digitalWrite(fan_in, LOW);
    digitalWrite(fan_out, HIGH);
    digitalWrite(water, LOW);
    Serial.println("Humid High Low Temp");
   }
   else if (humid >= 75 and temp >= 32 ){ //ชื้นปกติ tempสูง
    digitalWrite(fan_in, HIGH);
    digitalWrite(fan_out, LOW);
    digitalWrite(water, LOW);
    Serial.println("Normal Humid High Temp");
   }
   //////////////////////////////////////////////////////////////////////
   else if (humid >= 85 and temp >= 32){ //ชิ้นสูง tempสูง
    digitalWrite(fan_in, HIGH);
    digitalWrite(fan_out, HIGH);
    digitalWrite(water, LOW);
    Serial.println("All High");
   }
   else {
    Serial.println("Error");
   }
   Serial.println("--------------------------");
 
//   http.begin(client, "http://139.59.249.192/data/farm1/esp8266/"+String(temperature)+"/"+String(humidity) );
//   http.GET();
//   http.end();
   

  
   delay(10000);
  }
