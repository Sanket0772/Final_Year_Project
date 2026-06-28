import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load data
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

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

predictions = model.fit_predict(X_scaled)

scores = model.decision_function(X_scaled)
risk_scaler = MinMaxScaler(feature_range=(0,100))
risk_scaler.fit(scores.reshape(-1,1))

df["anomaly"] = predictions

df["anomaly"] = df["anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})


from sklearn.preprocessing import MinMaxScaler

risk_scaler = MinMaxScaler(feature_range=(0,100))

df["failure_risk"] = (
    100 -
    risk_scaler.fit_transform(
        scores.reshape(-1,1)
    )
).flatten()


# Save back to PostgreSQL
df.to_sql(
    "sensor_predictions",
    engine,
    if_exists="replace",
    index=False
)

print(df["anomaly"].value_counts())
print("Predictions saved to PostgreSQL!")




print(df.columns.tolist())