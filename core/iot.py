import requests
import json
import random

class IotEngine:
    """Manages integration with external hardware modules (e.g. Raspberry Pi), sensors."""
    def __init__(self):
        # Defaulting to localhost for local testing (until the actual Pi is on the network)
        # Change this IP to the Pi's Wi-Fi IP address (like 192.168.1.50) when deploying!
        self.rpi_ip = "http://127.0.0.1:5000"
        
    def get_health_report(self):
        """Fetch vitals via REST API request to the Raspberry Pi."""
        try:
            response = requests.get(f"{self.rpi_ip}/api/vitals", timeout=3)
            if response.status_code == 200:
                data = response.json()
                
                report = (f"Your latest vitals from the hardware read: "
                          f"Heart rate is {data['heart_rate']} bpm, "
                          f"you stepped {data['steps']} times today, "
                          f"burned {data['calories']} calories, "
                          f"and got {data['sleep_hours']} hours of sleep.")
                return report
            else:
                return "The Raspberry Pi sensor node returned an error."
        except requests.exceptions.RequestException:
            return "Sir, I am unable to connect to the Raspberry Pi hardware node. It might be offline."

    def get_environment_report(self):
        """Fetch room temperature from the Pi."""
        try:
            response = requests.get(f"{self.rpi_ip}/api/environment", timeout=3)
            if response.status_code == 200:
                data = response.json()
                
                report = (f"The current room temperature is {data['temperature_c']} degrees Celsius, "
                          f"with a humidity of {data['humidity_percent']} percent, "
                          f"and an air quality index of {data['air_quality_index']}.")
                return report
            else:
                return "The environmental sensor on the Pi returned an error."
        except requests.exceptions.RequestException:
            return "Sir, the Raspberry Pi environmental sensors are currently unreachable."
