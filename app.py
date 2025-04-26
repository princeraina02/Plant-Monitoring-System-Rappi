from flask import Flask, render_template, jsonify
import threading
import time
import json
from datetime import datetime
import sensor_controller
import database

app = Flask(__name__)

# Initialize database
database.init_db()

# Flag to control the sensor reading thread
running = True

def sensor_loop():
    """Background thread for reading sensors and saving to database"""
    try:
        while running:
            # Read sensors
            data = sensor_controller.read_sensors()
            
            # Save to database
            database.save_reading(data)
            
            # Print status to console
            print("="*40)
            print(f"Timestamp: {data['timestamp']}")
            print(f"Temperature: {data['temperature']}°C" if data['temperature'] is not None else "Temperature: Error")
            print(f"Humidity: {data['humidity']}%" if data['humidity'] is not None else "Humidity: Error")
            print(f"Soil Dry: {'Yes' if data['soil_moisture'] else 'No'}")
            print(f"Motor Status: {data['motor_status']}")
            print("="*40)
            
            # Wait before next reading
            time.sleep(5)  # Read every 5 seconds
    except Exception as e:
        print(f"Error in sensor loop: {e}")
    finally:
        sensor_controller.cleanup()

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/visualization')
def visualization():
    """Render the visualization dashboard"""
    return render_template('visualization.html')

@app.route('/api/current')
def current_data():
    """API endpoint to get current sensor data"""
    data = database.get_latest_reading()
    return jsonify(data)

@app.route('/api/history/<int:hours>')
def history_data(hours):
    """API endpoint to get historical sensor data"""
    data = database.get_readings(hours)
    return jsonify(data)

if __name__ == '__main__':
    # Start the sensor reading thread
    sensor_thread = threading.Thread(target=sensor_loop)
    sensor_thread.daemon = True
    sensor_thread.start()
    
    try:
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        # Set the flag to stop the sensor thread
        running = False
        sensor_controller.cleanup()
