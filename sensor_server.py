import Adafruit_DHT
from flask import Flask, request, render_template_string
import datetime
import threading
import time

app = Flask(__name__)

DATA_FILE = 'sensor_data.txt'
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin number, change if necessary

inside_temp = 0
inside_humidity = 0

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sensor Data</title>
    <meta http-equiv="refresh" content="60">  <!-- Refresh every 60 seconds -->
</head>
<body>
    <h1>Latest Sensor Data</h1>
    <h2>Outdoor (ESP32)</h2>
    <p>Last updated: {{ last_update }}</p>
    <ul>
        <li>Temperature: {{ temperature }} °C</li>
        <li>Humidity: {{ humidity }} %</li>
        <li>Pressure: {{ pressure }} hPa</li>
        <li>Light: {{ light }}</li>
    </ul>
    <h2>Indoor (Orange Pi 3 - DHT11)</h2>
    <ul>
        <li>Inside Temp: {{ inside_temp }} °C</li>
        <li>Inside Humidity: {{ inside_humidity }} %</li>
    </ul>
</body>
</html>
'''

def read_dht11():
    global inside_temp, inside_humidity
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            inside_temp = temperature
            inside_humidity = humidity
        time.sleep(60)  # Read every 60 seconds

@app.route('/')
def index():
    try:
        with open(DATA_FILE, 'r') as f:
            last_line = f.readlines()[-1]
        
        # Parse the last line
        data = dict(item.split(":") for item in last_line.strip().split(", "))
        data['inside_temp'] = f"{inside_temp:.1f}"
        data['inside_humidity'] = f"{inside_humidity:.1f}"
        return render_template_string(HTML_TEMPLATE, **data)
    except:
        return "No data available"

@app.route('/update_sensor_data', methods=['POST'])
def update_sensor_data():
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    pressure = request.form.get('pressure')
    light = request.form.get('light')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_string = f"last_update: {timestamp}, temperature: {temperature}, humidity: {humidity}, pressure: {pressure}, light: {light}\n"
    
    with open(DATA_FILE, 'a') as f:
        f.write(data_string)
    
    return "Data received", 200

if __name__ == '__main__':
    # Start the DHT11 reading thread
    dht_thread = threading.Thread(target=read_dht11, daemon=True)
    dht_thread.start()

    app.run(host='0.0.0.0', port=5000)