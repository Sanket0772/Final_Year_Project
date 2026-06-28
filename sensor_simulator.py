import random

def get_simulated_data():

    fault = random.random() < 0.10

    if not fault:

        return {
            "rpm": random.randint(1200, 1700),
            "motor_power": random.uniform(3500, 7000),
            "torque": random.uniform(30, 55),
            "outlet_pressure_bar": random.uniform(2, 4),
            "air_flow": random.uniform(700, 1200),
            "noise_db": random.uniform(42, 52),
            "outlet_temp": random.uniform(85, 105),
            "water_flow": random.uniform(45, 55)
        }

    else:

        return {
            "rpm": random.randint(2200, 2600),
            "motor_power": random.uniform(15000, 20000),
            "torque": random.uniform(75, 95),
            "outlet_pressure_bar": random.uniform(6, 8),
            "air_flow": random.uniform(100, 300),
            "noise_db": random.uniform(65, 75),
            "outlet_temp": random.uniform(155, 180),
            "water_flow": random.uniform(35, 42)
        }