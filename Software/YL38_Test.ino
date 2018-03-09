/* ESP8266 Moisture Sensor
   This sketch uses an ESP8266 to read the analog signal from a moisture sensor. The data is then displayed
   using the serial console or a web browser. Based on the moisture reading, the ESP8266 will blink a RGB LED
   red, green or blue.

   Red = Dry
   Green = In between Wet and Dry
   Blue = Wet

     Viewing the data via web browser by going to the ip address. In this sketch the address is
     http://192.168.1.221

      The browser data includes a Google Chart to visually illustrate the moisture reading as a guage.

   ///////////////////////////////////////
   Arduino IDE Setup
   File:
      Preferences
        Add the following link to the "Additional Boards Manager URLs" field: 
        http://arduino.esp8266.com/stable/package_esp8266com_index.json
   Tools:
      board: NodeMCU 1.0 (ESP-12 Module)
      programmer: USBtinyISP

      
  ///////////////////////////////
*/
#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(10);
}

double analogValue = 0.0;
double analogVolts = 0.0;
unsigned long timeHolder = 0;


void loop() {
  analogValue = analogRead(A0); // read the analog signal

  // convert the analog signal to voltage
  // the ESP2866 A0 reads between 0 and ~3 volts, producing a corresponding value
  // between 0 and 1024. The equation below will convert the value to a voltage value.



  analogVolts = (analogValue * 3.08) / 1024;

  // now get our chart value by converting the analog (0-1024) value to a value between 0 and 100.
  // the value of 400 was determined by using a dry moisture sensor (not in soil, just in air).
  // When dry, the moisture sensor value was approximately 400. This value might need adjustment
  // for fine tuning of the chartValue.

  int chartValue = (analogValue * 100) / 400;

  // now reverse the value so that the value goes up as moisture increases
  // the raw value goes down with wetness, we want our chart to go up with wetness
  chartValue = 100 - chartValue;

  // Serial data
  Serial.print("Analog raw: ");
  Serial.println(analogValue);
  Serial.print("Analog V: ");
  Serial.println(analogVolts);
  Serial.print("ChartValue: ");
  Serial.println(chartValue);
  Serial.println(" ");
  delay(1000); // slows amount of data sent via serial
}

