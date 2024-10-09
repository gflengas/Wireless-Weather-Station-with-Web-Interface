# ESP32-S2 + Orange Pi 3 Sensor Monitoring System

## Overview

This project is a simple sensor monitoring system using an **ESP32-S2**, **BME280 sensor**, and a **photoresistor**. The ESP32-S2 collects temperature, humidity, pressure, and light data from the sensors and sends it to an **Orange Pi 3** over WiFi every 10 minutes.

The Orange Pi 3 acts as a server, hosting a Flask-based web interface that displays both **indoor sensor data** (from a **DHT11** sensor) and **outdoor sensor data** (from the ESP32-S2). The sensor readings are saved in a text file on the Orange Pi 3.

## Components

1. **ESP32-S2**: Collects sensor data from the BME280 and a photoresistor, and sends it to the Orange Pi 3 via HTTP POST.
2. **Orange Pi 3**: Hosts the WiFi hotspot, receives sensor data, stores it in a text file, and serves a web page to display the data.
3. **BME280 Sensor**: Measures temperature, humidity, and pressure (connected to the ESP32-S2).
4. **Photoresistor**: Measures light intensity (connected to the ESP32-S2).
5. **DHT11 Sensor**: Measures indoor temperature and humidity (connected to the Orange Pi 3).

## How It Works

### ESP32-S2 Code

- The ESP32-S2 connects to the WiFi hotspot created by the Orange Pi 3.
- Every 10 minutes, the ESP32-S2 reads data from the BME280 sensor and the photoresistor.
- The sensor data (temperature, humidity, pressure, and light) is sent via HTTP POST to the Orange Pi 3.

### Orange Pi 3 Code

- The Flask-based server (`sensor_server.py`) receives the sensor data from the ESP32-S2 and writes it to a text file (`sensor_data.txt`).
- The DHT11 sensor (connected to the Orange Pi 3) measures indoor temperature and humidity every minute.
- A web page is served at `http://[Orange_Pi_3_IP]:5000` that displays both indoor and outdoor sensor data. The page refreshes every 60 seconds to show the latest readings.

### Web Interface

The web interface displays:
- **Outdoor sensor data** from the ESP32-S2 (temperature, humidity, pressure, and light).
- **Indoor sensor data** from the DHT11 (temperature and humidity).

## Prerequisites

- **ESP32-S2 Development Environment** (e.g., Arduino IDE with ESP32 core installed)
- **Orange Pi 3** running a Python environment (with Flask and `Adafruit_DHT` library installed)
- **Sensors**:
  - BME280 connected to ESP32-S2
  - Photoresistor connected to ESP32-S2
  - DHT11 connected to Orange Pi 3

## Setup

### ESP32-S2 Code

1. Connect the **BME280** and **photoresistor** to the ESP32-S2.
2. Update the **WiFi credentials** in `esp32_sensor_wifi.ino` to match the WiFi hotspot hosted by the Orange Pi 3.
3. Flash the ESP32-S2 with the code using the Arduino IDE.

### Orange Pi 3 Code

1. Install Flask and Adafruit DHT library:
   ```bash
   pip install Flask Adafruit_DHT
2. Connect the DHT11 sensor to the Orange Pi 3.
3. Run the sensor_server.py script:
   ```bash
   python3 sensor_server.py
4. Access the web interface by opening http://[Orange_Pi_3_IP]:5000 in a web browser.
   
## Usage
- Once both the ESP32-S2 and Orange Pi 3 are set up, the ESP32-S2 will send outdoor sensor data every 10 minutes to the Orange Pi 3.
- The Orange Pi 3 will display both outdoor and indoor sensor data on a web page that refreshes every 60 seconds.
- The data is also stored in a file named sensor_data.txt on the Orange Pi 3.

## Notes
- The ESP32-S2 should be within the range of the Orange Pi 3’s WiFi hotspot.
- Ensure that the BME280 sensor is properly wired and the I2C address is correctly set in the ESP32 code (0x76 or 0x77).
- The web interface only shows the latest sensor data, but you can modify the Flask app to log historical data if needed.

## License 
This project is open source. Feel free to modify and share it as needed.