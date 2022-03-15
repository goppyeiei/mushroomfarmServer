#include <Arduino_JSON.h>

#include <dummy.h>

#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "12345";
const char* password = "123456789";
int user_id = 1;
int farm_id = 1;
int fan = 27;
int fog = 26;
String fan_status;
String fog_status;

void setup () {

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.print("Connecting..");
  }

  Serial.println("Connected");

  pinMode(fan, OUTPUT);
  pinMode(fog, OUTPUT);

}

void loop() {

  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, "http://139.59.249.192/check-iot/"+ String(user_id) + "/" + String(farm_id) );
    int dataa = http.GET();
    String iot_status = http.getString();
    http.end();
    fan_status = iot_status[0];
    fog_status = iot_status[3];
    Serial.println("http://139.59.249.192/check-condition/"+ String(user_id) + "/" + String(farm_id) + "/" + String(fan_status) + "/" + String(fog_status));
    
    http.begin(client, "http://139.59.249.192/check-condition/"+ String(user_id) + "/" + String(farm_id) + "/" + String(fan_status) + "/" + String(fog_status) );
    http.GET();
    http.end();
    delay(1000);
  };

  if (fan_status == "1") {
    digitalWrite(fan,LOW);
    Serial.println("Fan on");
  } else {
    digitalWrite(fan,HIGH);
    Serial.println("Fan off");
  }
  
  if (fog_status == "1") {
    digitalWrite(fog,LOW);
    Serial.println("Fog on");
  } else {
    digitalWrite(fog,HIGH);
    Serial.println("Fog off");
  }

  
}
