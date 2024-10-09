#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <HTTPClient.h>

// WiFi credentials (Orange Pi 3 hotspot)
const char* ssid = "OrangePi3_Hotspot";
const char* password = "your_hotspot_password";

// Orange Pi 3 server details
const char* serverName = "http://[Orange_Pi_3_IP]:5000/update_sensor_data";

// BME280 sensor
Adafruit_BME280 bme;

// Photoresistor pin
const int photoresistorPin = 34;  // Change this to the actual pin you're using

// Time interval (10 minutes in milliseconds)
const unsigned long interval = 600000;

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize BME280
  if (!bme.begin(0x76)) {  // Change address if needed
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  // Set up photoresistor pin
  pinMode(photoresistorPin, INPUT);
}

void loop() {
  // Read sensor data
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;
  int light = analogRead(photoresistorPin);

  // Prepare data string
  String data = "temperature=" + String(temperature) +
                "&humidity=" + String(humidity) +
                "&pressure=" + String(pressure) +
                "&light=" + String(light);

  // Send data via WiFi
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    int httpResponseCode = http.POST(data);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  // Wait for 10 minutes
  delay(interval);
}