// Now using ESP8266.....
// Sample Arduino Json Web Server
// Origninally Created by Benoit Blanchon.
// Heavily inspired by "Web Server" from David A. Mellis and Tom Igoe
// Modified by Martin Morales

#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include "DHT.h"
//////////////////////////////
// DHT21 / AMS2301 is at GPIO2
//////////////////////////////
#define DHTPIN 14

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11 
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// init DHT; 3rd parameter = 16 works for ESP8266@80MHz
DHT dht(DHTPIN, DHTTYPE,15); 

// needed to avoid link error on ram check
extern "C" 
{
#include "user_interface.h"
}
ADC_MODE(ADC_VCC);

WiFiServer server(80);
WiFiClient client;
const char* ssid = "DU Public Resident";
const char* password = "Your-PASSWORD";
float pfHum,pfTemp;

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

JsonObject& prepareResponse(JsonBuffer& jsonBuffer) {
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& tempValues = root.createNestedArray("temperature");
    tempValues.add(pfTemp);
  JsonArray& humiValues = root.createNestedArray("humidity");
    humiValues.add(pfHum); 
  return root;
}

void writeResponse(WiFiClient& client, JsonObject& json) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();

  json.prettyPrintTo(client);
}

void setup() {
delay(2000);
  dht.begin();
  // inital connect
  WiFi.mode(WIFI_STA);
  delay(1000);
    // Connect to WiFi network
  WiFi.begin(ssid);  
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
  }

    Serial.println("");
  Serial.println("WiFi connected");
 
  server.begin();

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
   pfTemp = dht.readTemperature();   
   pfHum = dht.readHumidity();
   delay(500);
      StaticJsonBuffer<500> jsonBuffer;
      JsonObject& json = prepareResponse(jsonBuffer);
      writeResponse(client, json);
    }
    delay(1);
    client.stop();
  }
}
