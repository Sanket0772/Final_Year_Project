import serial
import json
import time

# Change this later to your Arduino COM port
PORT = "COM3"

# Change if your Arduino uses a different baud rate
BAUD_RATE = 9600


def get_live_data():
    """
    Reads one sensor record from Arduino.
    Returns a dictionary.
    Raises an exception if sensors are unavailable.
    """

    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=2)

        # Give Arduino time to reset
        time.sleep(2)

        line = ser.readline().decode().strip()

        ser.close()

        if not line:
            raise Exception("No sensor data received")

        data = json.loads(line)

        return {
            "rpm": data["rpm"],
            "motor_power": data["motor_power"],
            "torque": data["torque"],
            "outlet_pressure_bar": data["outlet_pressure_bar"],
            "air_flow": data["air_flow"],
            "noise_db": data["noise_db"],
            "outlet_temp": data["outlet_temp"],
            "water_flow": data["water_flow"]
        }

    except Exception as e:
        raise Exception(f"Live sensor unavailable: {e}")