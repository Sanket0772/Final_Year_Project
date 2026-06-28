import pandas as pd
import random
import time
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler


DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Train model using existing historical data
df = pd.read_sql("SELECT * FROM sensor_data;", engine)

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

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    contamination=0.01,
    random_state=42
)

model.fit(X_scaled)





while True:
    new_data = pd.DataFrame([{
        "id": current_id,
        "rpm": random.randint(450, 2600),
        "motor_power": random.uniform(1300, 20000),
        "torque": random.uniform(20, 95),
        "outlet_pressure_bar": random.uniform(1, 8),
        "air_flow": random.uniform(100, 1600),
        "noise_db": random.uniform(40, 75),
        "outlet_temp": random.uniform(75, 180),
        "water_flow": random.uniform(38, 60)
    }])

    X_new = scaler.transform(new_data[features])

    prediction = model.predict(X_new)[0]
    new_data["anomaly"] = "Anomaly" if prediction == -1 else "Normal"

    if prediction == -1:
        failure_risk = random.uniform(65, 90)
    else:
        failure_risk = random.uniform(10, 35)

    new_data["failure_risk"] = round(failure_risk, 2)
    new_data["health_score"] = round(100 - failure_risk, 2)

    # Save to database
    new_data.to_sql(
        "sensor_predictions",
        engine,
        if_exists="append",
        index=False
    )

    print(f"Inserted record {current_id} | Status: {new_data['anomaly'].iloc[0]}")

    current_id += 1
    time.sleep(5)




print(df.columns)    