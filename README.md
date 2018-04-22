# Project "Green"

Green Lantern Green House Project

With our project, we hope to aid the students and faculty working in the greenhouse by collecting, providing and monitoring data for them. This subset of data would include moisture, temperature, humidity, light intensity, and UV index. Our ultimate goal is to use this data to be able to automate certain tasks, such as water pump activity and fan automation. 
1. Humidity
2. Temperature
3. Moisture
4. Light
5. UV Index

Using this data, we will be able to automate certain *tasks* accordingly.

These tasks include:
* Automated water pumps
* Automated lighting
* Automated fans

![DU Greenhouse](http://newsroom.dom.edu/sites/newsroom.dom.edu/files/styles/large/public/kaleys.jpg?itok=Kj-7vdjN)

Instructions used:

## Hardware Software
* Raspbian Apache Web Server
  * [Apache](https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md)
* MySQL Server
  * [MySQL](https://www.stewright.me/2014/06/tutorial-install-mysql-server-on-raspberry-pi/)
* Connecting ESP8266 Board to Arduino
  * [Getting started](https://www.youtube.com/watch?v=p06NNRq5NTU)
  * [ESP8266 Board Manager](http://arduino.esp8266.com/stable/package_esp8266com_index.json)
* Connecting Sensors to ESP8266 Chip
  * [Sensor Connection 
Guide](https://medium.com/oracledevs/monitoring-sensor-data-in-jet-mobile-app-over-websockets-part-1-2-f7fa81d9774b)
* Libraries used for all sensors
  * [ArduinoJson](https://github.com/bblanchon/ArduinoJson/releases)
  * [ESP8266WiFi.h](https://github.com/esp8266/Arduino/blob/master/libraries/ESP8266WiFi/src/ESP8266WiFi.h) 
* [DHT11 Connection Guide](http://www.instructables.com/id/Interface-DHT11-Humidity-Sensor-Using-NodeMCU/)
  * [DHT.h Library](https://github.com/esp8266/Basic/blob/master/libraries/DHT_sensor_library/DHT.h)
  * [Adafruit Sensor Library](https://github.com/adafruit/Adafruit_Sensor)
* [YL69 Connection Guide](https://www.youtube.com/watch?v=9TD6mOyowcg)
* [SI1145 Connection Guide](http://www.techparva.com/index.php/2017/08/31/bh1750-light-sensor-nodemcu-micropython/)
  * [Adafruit SI1145 Library](https://github.com/adafruit/Adafruit_SI1145_Library)
  * [Wire.h](https://github.com/esp8266/Arduino/blob/master/libraries/Wire/Wire.h)
* Arduino IDE
  * [Arduino](https://www.arduino.cc/en/Main/Software)
## Website Software
* Flask 
	* [Website Development with Flask](https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/9)

