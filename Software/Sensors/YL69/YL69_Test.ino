/*
 # Example code for the moisture sensor
 # Connect the sensor to the A0 (Analog 0) pin on the Arduino board
 # the sensor value description
 # 0 ~300 dry soil
 # 300~700 humid soil
 # 700~950 in water
*/ 

// Initialize variable
double analogValue = 0.0;

// Initial loop of board
void setup(){
 Serial.begin(57600);
}

// Board loops
void loop(){
  Serial.begin(115200);
  // Read data from sensor
  analogValue = analogRead(0);

  // Convert to percentage value
  int chartValue = (analogValue * 100) / 1024;

 // Print value to console
 Serial.print("Moisture Sensor Value:");
 Serial.println(chartValue);
 delay(100);
}
