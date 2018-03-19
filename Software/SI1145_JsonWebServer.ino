// Now using ESP8266.....
// Sample Arduino Json Web Server
// Created by Benoit Blanchon.
// Heavily inspired by "Web Server" from David A. Mellis and Tom Igoe


#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_SI1145.h>

Adafruit_SI1145 uv = Adafruit_SI1145();

 //needed to avoid link error on ram check
extern "C" 
{
#include "user_interface.h"
}

WiFiServer server(80);
WiFiClient client;
const char* ssid = "Restricted Wireless";
const char* password = "B=SP7e&aNK";
  
bool readRequest(WiFiClient& client) {
  bool currentLineIsBlank = true;
  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      if (c == '\n' && currentLineIsBlank) {
        return true;
      } else if (c == '\n') {
        currentLineIsBlank = true;
      } else if (c != '\r') {
        currentLineIsBlank = false;
      }
    }
  }
  return false;
}

uint16_t visible_light;
uint16_t uv_light;
float uv_index;

JsonObject& prepareResponse(JsonBuffer& jsonBuffer) {
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& visibleValues = root.createNestedArray("visible_light");
    visibleValues.add(visible_light);
  JsonArray& irValues = root.createNestedArray("IR_light");
    irValues.add(uv_light);
  JsonArray& uvValues = root.createNestedArray("UV_light");
    uvValues.add(uv_index);
  return root;
}

void writeResponse(WiFiClient& client, JsonObject& json) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();

  json.prettyPrintTo(client);
}

void readLight(){
  float uv_index_original = uv.readUV();
  uv_index = uv_index_original / 100.0;
  visible_light = uv.readVisible();
  uv_light = uv.readIR();

  Serial.print("Visible Light: "); Serial.println(visible_light);
  Serial.print("IR Light: "); Serial.println(uv_light);
  Serial.print("UV Index: ");  Serial.println(uv_index);
  
 delay(5000);
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  
  if (!uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }
  else {
    Serial.println("Si1145 ready.");
  }
  
  // inital connect
  WiFi.mode(WIFI_STA);
  delay(1000);
  
  // Connect to WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid,password);  
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Start the server
  server.begin();
  Serial.println("Server started");
  
  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    bool success = readRequest(client);
    
    if (success) {
      delay(1000);
      readLight();
      delay(500);

      StaticJsonBuffer<500> jsonBuffer;
      JsonObject& json = prepareResponse(jsonBuffer);
      writeResponse(client, json);
    }
    delay(1);
    client.stop();
  }
delay(5000);
}




