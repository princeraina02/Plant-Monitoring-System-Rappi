### Plant Monitoring System

A comprehensive Raspberry Pi-based system for monitoring and automating plant care. This project uses sensors to track temperature, humidity, and soil moisture, automatically controlling a water pump based on soil conditions.


## Features

- Real-time monitoring of:

- Temperature (via DHT11 sensor)
- Humidity (via DHT11 sensor)
- Soil moisture



- Automated water pump control based on soil moisture levels
- Data logging to SQLite database with timestamps
- Responsive web interface with real-time updates
- Historical data visualization with interactive charts
- Multiple time range options for data analysis (6 hours to 1 week)


## Hardware Requirements

- Raspberry Pi (3 or 4 recommended)
- DHT11 Temperature and Humidity Sensor
- Soil Moisture Sensor (with digital output)
- Water Pump (5V DC)
- Relay Module (to control the water pump)
- Jumper Wires
- Breadboard
- 5V Power Supply


## Software Requirements

- Raspberry Pi OS (Bullseye or newer recommended)
- Python 3.7+
- Flask web framework
- Required Python libraries (see Installation)


## Installation

### 1. Update your Raspberry Pi

```shellscript
sudo apt update
sudo apt upgrade -y
```

### 2. Install required system packages

```shellscript
sudo apt install -y python3-pip python3-dev python3-venv libgpiod2
```

### 3. Clone the repository , set up virtual environment

```shellscript
# Create project directory
git clone https://github.com/princeraina02/Plant-Monitoring-System-Rappi
cd Plant-Monitoring-System-Rappi

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 4. Install required Python packages

```shellscript
pip install RPi.GPIO adafruit-circuitpython-dht flask flask-socketio
or
pip install -r requirements.txt
```

## Hardware Setup

Connect the components to your Raspberry Pi as follows:

### DHT11 Temperature/Humidity Sensor

- VCC → 3.3V or 5V (depending on your sensor)
- GND → Ground
- DATA → GPIO16


### Soil Moisture Sensor

- VCC → 3.3V or 5V (depending on your sensor)
- GND → Ground
- D0 (Digital Output) → GPIO26


### Water Pump (via Relay)

- Connect relay control pin to GPIO6
- Connect relay power to 5V and GND
- Connect water pump to relay output and external power supply


## Configuration

### 1. Create project structure

Ensure your project has the following structure:

```plaintext
plant_monitoring/
├── venv/                      # Virtual environment
├── app.py                     # Main application file
├── database.py                # Database handling
├── sensor_controller.py       # Sensor reading and motor control
├── templates/                 # Web templates
│   ├── index.html             # Main dashboard
│   └── visualization.html     # Data visualization dashboard
└── requirements.txt           # Dependencies
```

### 2. Adjust GPIO pins (if needed)

If your wiring differs from the default setup, modify the pin definitions in `sensor_controller.py`:

```python
# Pin setup
DHT_PIN = 16  # Change if using different GPIO pin
SOIL_MOISTURE_PIN = 26  # Change if using different GPIO pin
PUMP_PIN = 6  # Change if using different GPIO pin
```

## Usage

### 1. Start the application

Make sure you're in the project directory with the virtual environment activated:

```shellscript
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the application
python app.py
```

### 2. Access the web interface

Open a web browser and navigate to:

```plaintext
http://[your-raspberry-pi-ip]:5000
```

Replace `[your-raspberry-pi-ip]` with the IP address of your Raspberry Pi.

### 3. Set up autostart (optional)

To make the application start automatically when the Raspberry Pi boots:

Create a systemd service file:

```shellscript
sudo nano /etc/systemd/system/plant_monitor.service
```

Add the following content (adjust paths as needed):

```plaintext
[Unit]
Description=Plant Monitoring System
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/plant_monitoring
ExecStart=/home/pi/plant_monitoring/venv/bin/python /home/pi/plant_monitoring/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```shellscript
sudo systemctl enable plant_monitor.service
sudo systemctl start plant_monitor.service
```

## Web Interface

### Main Dashboard

The main dashboard displays real-time sensor readings:

- Temperature (°C)
- Humidity (%)
- Soil Moisture Status (Wet/Dry)
- Pump Status (On/Off)


Data refreshes automatically every 5 seconds.

### Visualization Dashboard

The visualization dashboard shows historical data as interactive charts:

- Temperature over time
- Humidity over time
- Soil moisture status over time
- Pump activity over time


You can select different time ranges:

- 6 Hours
- 12 Hours
- 24 Hours
- 2 Days
- 1 Week


## Database

The system uses SQLite to store sensor readings. The database file (`plant_data.db`) is created automatically in the project directory.

### Database Schema

```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    temperature REAL,
    humidity REAL,
    soil_moisture INTEGER,
    motor_status TEXT
)
```

## Troubleshooting

### Sensor Reading Errors

If you encounter issues with sensor readings:

1. **Check wiring connections**

1. Ensure all wires are properly connected
2. Verify power connections (3.3V or 5V as required by your sensors)



2. **DHT11 Sensor Issues**

1. The DHT11 can be sensitive; try increasing the delay between readings
2. Make sure you've installed the correct library: `adafruit-circuitpython-dht`
3. Some DHT11 sensors require a pull-up resistor (4.7kΩ to 10kΩ) between data and VCC



3. **Soil Moisture Sensor Issues**

1. Check if the sensor is properly inserted into the soil
2. Adjust the sensitivity using the potentiometer on the sensor module (if available)
3. Clean the sensor probes if they're dirty





### Web Interface Issues

1. **Cannot access web interface**

1. Verify the Raspberry Pi is connected to the network
2. Check if the Flask application is running (`ps aux | grep app.py`)
3. Ensure port 5000 is not blocked by a firewall



2. **Charts not displaying data**

1. Check if there are entries in the database
2. Verify the API endpoints are working by accessing them directly:

1. `http://[your-raspberry-pi-ip]:5000/api/current`
2. `http://[your-raspberry-pi-ip]:5000/api/history/24`








### Database Issues

1. **Database errors**

1. Check file permissions for the database file
2. Ensure the directory is writable by the application





## Future Enhancements

Potential improvements for the project:

1. **Automated Watering Schedule**

1. Add time-based watering in addition to moisture-based
2. Create a schedule for watering at specific times



2. **Email/SMS Alerts**

1. Send notifications when soil is too dry for extended periods
2. Alert when temperature goes outside optimal range



3. **Camera Integration**

1. Add a Raspberry Pi camera to take periodic photos of your plant
2. Create a timelapse of plant growth



4. **Weather API Integration**

1. Fetch local weather data to adjust watering schedule
2. Compare indoor and outdoor conditions



5. **Multiple Plant Support**

1. Expand the system to monitor multiple plants with different sensors
2. Create plant profiles with optimal conditions for each type
