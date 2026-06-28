import pandas as pd
import random
import time
from sensor_manager import get_sensor_data
from sqlalchemy import create_engine
from datetime import datetime

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler



# ==========================
# DATABASE CONFIGURATION
# ==========================

from config import *

engine = create_engine(DATABASE_URL)

print("Connected to PostgreSQL")


# ==========================
# LOAD TRAINING DATA
# ==========================

print("Loading historical sensor data...")

df = pd.read_sql(
    "SELECT * FROM sensor_data;",
    engine
)

print(f"Loaded {len(df)} historical records")


model = IsolationForest(
    contamination=MODEL_CONTAMINATION,
    random_state=RANDOM_STATE
)

# ==========================
# FEATURES
# ==========================

features = [
    "rpm",
    "motor_power",
    "torque",
    "outlet_pressure_bar",
    "air_flow",
    "noise_db",
    "outlet_temp",
    "water_flow"
]

X = df[features]


# ==========================
# SCALE DATA
# ==========================

print("Scaling sensor data...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ==========================
# TRAIN MODEL
# ==========================

print("Training Isolation Forest...")



model.fit(X_scaled)

print("\n")
print("=" * 50)
print("Model Loaded Successfully")
print("=" * 50)


import time

print("\nPrediction Engine Started...\n")

while True:

    sensor = get_sensor_data()
    new_data = pd.DataFrame([sensor])
    X_new = scaler.transform(new_data[features])

    # Predict anomaly
    prediction = model.predict(X_new)[0]
    new_data["anomaly"] = (
    "Anomaly"
    if prediction == -1
    else "Normal"
)

    # Get anomaly score
    score = model.decision_function(X_new)[0]
    new_data["anomaly_score"] = round(float(score), 4)

    # Failure Risk
    if prediction == -1:
        failure_risk = random.uniform(65, 90)
    else:
        failure_risk = random.uniform(10, 35)
        
    new_data["failure_risk"] = round(failure_risk, 2)
    # Health Score
    new_data["health_score"] = round(
        100 - failure_risk,
        2
    )
    new_data["timestamp"] = datetime.now()
    print("\n==============================")
    print(new_data)

    new_data.to_sql(
    "sensor_predictions",
    engine,
    if_exists="append",
    index=False
)
    print("Record saved to PostgreSQL")
    print("==============================\n")

    time.sleep(UPDATE_INTERVAL)