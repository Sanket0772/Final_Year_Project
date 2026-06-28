import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_sql("SELECT * FROM sensor_predictions;", engine)

normal = df[df["anomaly"] == "Normal"]
anomaly = df[df["anomaly"] == "Anomaly"]

plt.figure(figsize=(10, 6))

plt.scatter(
    normal["rpm"],
    normal["outlet_temp"],
    label="Normal",
    alpha=0.6
)

plt.scatter(
    anomaly["rpm"],
    anomaly["outlet_temp"],
    label="Anomaly",
    alpha=0.9
)

plt.xlabel("RPM")
plt.ylabel("Outlet Temperature")
plt.title("Predictive Maintenance Anomaly Detection")
plt.legend()
plt.show()