from live_sensor import get_live_data
from sensor_simulator import get_simulated_data


def get_sensor_data():
    """
    Returns sensor data from live sensors if available.
    Otherwise automatically switches to simulator.
    """

    try:
        data = get_live_data()

        print("🟢 Live Sensor Mode")

        return data

    except Exception as e:

        print(f"⚠ Live sensor unavailable: {e}")
        print("🟡 Switching to Simulation Mode")

        return get_simulated_data()