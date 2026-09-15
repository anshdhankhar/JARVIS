from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

@app.route('/api/vitals', methods=['GET'])
def get_vitals():
    """
    Simulates getting data from real MAX30100/MAX30102 sensors attached to the Pi.
    When you build the circuit, replace the random generators with I2C bus readings.
    """
    data = {
        "heart_rate": random.randint(60, 100),
        "steps": random.randint(2000, 8000),
        "calories": random.randint(1500, 2500),
        "sleep_hours": round(random.uniform(6.0, 9.0), 1),
        "timestamp": datetime.datetime.now().isoformat()
    }
    return jsonify(data)

@app.route('/api/environment', methods=['GET'])
def get_environment():
    """
    Simulates getting data from a DHT11 or DHT22 temperature/humidity sensor.
    """
    data = {
        "temperature_c": round(random.uniform(20.0, 25.0), 1),
        "humidity_percent": random.randint(30, 60),
        "air_quality_index": random.randint(40, 100),
        "timestamp": datetime.datetime.now().isoformat()
    }
    return jsonify(data)

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "message": "JARVIS Raspberry Pi Hardware Node Active"})

if __name__ == '__main__':
    # Run the server on all network interfaces so the main Mac can reach it
    print("========================================")
    print("🍓 JARVIS Hardware Node Started")
    print("========================================")
    app.run(host='0.0.0.0', port=5000)
