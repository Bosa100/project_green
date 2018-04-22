// Now using ESP8266.....
// Sample Arduino Json Web Server
// Created by Benoit Blanchon.
// Heavily inspired by "Web Server" from David A. Mellis and Tom Igoe
// Modified by Martin Morales

// Library imports
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include "DHT.h"
#define DHTPIN 14
#define DHTTYPE DHT11   // DHT 11 

// init DHT
DHT dht(DHTPIN, DHTTYPE,15); 

// needed to avoid link error on ram check
extern "C" 
{
#include "user_interface.h"
}
ADC_MODE(ADC_VCC);

//Initialize variables
WiFiServer server(80);
WiFiClient client;
const char* ssid = "Restricted Wireless";
const char* password = "B=SP7e&aNK";
float pfHum,pfTemp;

//Method that reads request from client
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

// Prepares response / Uses the data read from sensors and formulates JsonObject to be written
JsonObject& prepareResponse(JsonBuffer& jsonBuffer) {
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& tempValues = root.createNestedArray("temperature");
    tempValues.add(pfTemp);
  JsonArray& humiValues = root.createNestedArray("humidity");
    humiValues.add(pfHum); 
  return root;
}

// Uses Json object passed to write response to client
void writeResponse(WiFiClient& client, JsonObject& json) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();

  json.prettyPrintTo(client);
}

// Initial setup of board
void setup() {
  Serial.begin(115200);
  delay(2000);
  
  dht.begin();
  
  // inital connect
  WiFi.mode(WIFI_STA);
  delay(1000);
  
  // Connect to WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);

  //Begin connection to wifi
  WiFi.begin(ssid, password);

  // While board not connected to wifi: delay until successful connection
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
  //Serial.println(WiFi.macAddress());   // Used for testing
}

// To loop while board is connected: 
void loop() {
  // Set client whenver server connection is available
  WiFiClient client = server.available();

  //If successful connection to client:
  if (client) {

    //Read request from client
    bool success = readRequest(client);

    //If successful request:
    if (success) {
     //delay(1000);

     // Read data from sensor
     pfTemp = dht.readTemperature();   
     pfHum = dht.readHumidity();

     // Give the sensor time to read data
     delay(500);

     // Initialize JsonBuffer
     StaticJsonBuffer<500> jsonBuffer;

     // Prepare response generated
     JsonObject& json = prepareResponse(jsonBuffer);

     // Write response to client
     writeResponse(client, json);
    }

    // Give the program time to write response and disconnect from client
    delay(1);
    client.stop();
  }
}
