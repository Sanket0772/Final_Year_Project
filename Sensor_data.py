import pandas as pd
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

required_columns = [
    "id",
    "rpm",
    "motor_power",
    "torque",
    "outlet_pressure_bar",
    "air_flow",
    "noise_db",
    "outlet_temp",
    "water_flow",
]

df = pd.read_excel("D:/Datasets_project/sensor_data.xlsx")

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns in Excel file: {missing_columns}")

df = df[required_columns]

df.to_sql(
    "sensor_data",
    engine,
    if_exists="append",
    index=False,
)

print("Data imported successfully!")





print(df.head())
print(df.info())
print(df.describe())