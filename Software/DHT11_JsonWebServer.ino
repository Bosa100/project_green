// Now using ESP8266.....
// Sample Arduino Json Web Server
// Created by Benoit Blanchon.
// Heavily inspired by "Web Server" from David A. Mellis and Tom Igoe
// Modified by Martin Morales

// Import libraries
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include "DHT.h"
#define DHTPIN 14
#define DHTTYPE DHT11   // DHT 11 

// init DHT; 3rd parameter = 16 works for ESP8266@80MHz
DHT dht(DHTPIN, DHTTYPE,15); 

// needed to avoid link error on ram check
extern "C" 
{
#include "user_interface.h"
}
ADC_MODE(ADC_VCC);

//Initialize server properties and variables
WiFiServer server(80);
WiFiClient client;
const char* ssid = "Restricted Wireless";
const char* password = "B=SP7e&aNK";
float pfHum,pfTemp;

//Function to check client availability
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

//Function for initializing Json obkects
JsonObject& prepareResponse(JsonBuffer& jsonBuffer) {
  JsonObject& root = jsonBuffer.createObject();
  JsonArray& tempValues = root.createNestedArray("temperature");
    tempValues.add(pfTemp);
  JsonArray& humiValues = root.createNestedArray("humidity");
    humiValues.add(pfHum); 
  return root;
}

//Function for writing response to client
void writeResponse(WiFiClient& client, JsonObject& json) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");
  client.println();

  json.prettyPrintTo(client);
}

//Startup Function
void setup() {
  //Initialize serial 
  Serial.begin(115200);
  delay(2000);
  
  //Initialize sensor
  dht.begin();
  
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

//Loop function
void loop() {
  //Check for clients while server is available
  WiFiClient client = server.available();
  if (client) {
    bool success = readRequest(client);
    
    //If client is ready for response:	
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
