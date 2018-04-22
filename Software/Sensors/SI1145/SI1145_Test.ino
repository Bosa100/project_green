#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_SI1145.h>
 
// Initialize sensor
Adafruit_SI1145 uv = Adafruit_SI1145();
 

// First run of board 
void setup() {
  //Initalize console
  Serial.begin(115200);
  delay(10);
 
  Serial.println("Sensor Test");

  // If sensor not ready:
  if (!uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }

  //Else indicate successful connection
  else {
    Serial.println("Si1145 ready.");
  }
}

// To be looped by board: 
void loop() {
  // Initialize data variables
  float uv_index_original = uv.readUV();
  float uv_index = uv_index_original / 100.0;
  uint16_t visible_light = uv.readVisible();
  uint16_t uv_light = uv.readIR();

  Serial.println("");

  // Print data read from sensor
  Serial.print("Visible Light: "); Serial.println(visible_light);
  Serial.print("IR Light: "); Serial.println(uv_light);
  Serial.print("UV Index: ");  Serial.println(uv_index);

  Serial.println("");
 
  delay(5000);
}

