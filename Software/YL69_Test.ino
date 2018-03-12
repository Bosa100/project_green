/*
 # Example code for the moisture sensor
 # Connect the sensor to the A0 (Analog 0) pin on the Arduino board
 # the sensor value description
 # 0 ~300 dry soil
 # 300~700 humid soil
 # 700~950 in water
*/ 

void setup(){
 Serial.begin(57600);
}

double analogValue = 0.0;

void loop(){
  analogValue = analogRead(0);
  int chartValue = (analogValue * 100) / 1024;
 
 Serial.print("Moisture Sensor Value:");
 Serial.println(chartValue);
 delay(100);
}
