import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import sqlite3
from datetime import datetime

# Pin setup
DHT_PIN = 16
SOIL_MOISTURE_PIN = 26
PUMP_PIN = 6

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.output(PUMP_PIN, GPIO.LOW)  # motor off initially

# DHT sensor setup
dht_sensor = adafruit_dht.DHT11(board.D16)

def read_soil_moisture():
    """Read soil moisture status (Digital Read). Return 1 if dry, 0 if wet."""
    return GPIO.input(SOIL_MOISTURE_PIN)

def read_sensors():
    """Read all sensors and return their values"""
    # Read DHT11 sensor
    try:
        temperature_c = dht_sensor.temperature
        humidity = dht_sensor.humidity
    except Exception as e:
        temperature_c = None
        humidity = None
        print(f"DHT read error: {e}")

    # Read soil moisture sensor
    soil_moisture_status = read_soil_moisture()

    # Motor control based on soil dryness
    if soil_moisture_status == 1:  # Dry soil (digital output HIGH)
        GPIO.output(PUMP_PIN, GPIO.HIGH)
        motor_status = "ON"
    else:  # Wet soil
        GPIO.output(PUMP_PIN, GPIO.LOW)
        motor_status = "OFF"
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature_c,
        "humidity": humidity,
        "soil_moisture": soil_moisture_status,
        "motor_status": motor_status
    }

def cleanup():
    """Clean up GPIO pins"""
    GPIO.cleanup()
