#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_SI1145.h>
 

Adafruit_SI1145 uv = Adafruit_SI1145();
 
/*************************** Sketch Code ************************************/
 
void setup() {
  Serial.begin(115200);
  delay(10);
 
  Serial.println("Sensor Test");

  if (!uv.begin()) {
    Serial.println("Didn't find Si1145");
    while (1);
  }
  else {
    Serial.println("Si1145 ready.");
  }
}

void loop() {
  
  float uv_index_original = uv.readUV();
  float uv_index = uv_index_original / 100.0;
  uint16_t visible_light = uv.readVisible();
  uint16_t uv_light = uv.readIR();

  Serial.println("");
  
  Serial.print("Visible Light: "); Serial.println(visible_light);
  Serial.print("IR Light: "); Serial.println(uv_light);
  Serial.print("UV Index: ");  Serial.println(uv_index);

  Serial.println("");
  

  Serial.println("");
  
  delay(5000);
}

