from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

app = FastAPI()

DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

@app.get("/")
def root():
    return {"message": "Predictive Maintenance API Running"}


@app.get("/latest")
def latest_data():

    df = pd.read_sql(
        """
        SELECT *
        FROM sensor_predictions
        ORDER BY id DESC
        LIMIT 1
        """,
        engine
    )

    return df.to_dict(orient="records")[0]



@app.get("/history")
def history():

    df = pd.read_sql(
        """
        SELECT *
        FROM sensor_predictions
        ORDER BY id DESC
        LIMIT 500
        """,
        engine
    )

    # Replace NaN values with None so JSON can serialize them
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")


def get_recommendations(row):

    recommendations = []

    if row["rpm"] < 900:
        recommendations.append("Inspect motor bearings.")

    if row["outlet_temp"] > 60:
        recommendations.append("Check cooling system.")

    if row["noise_db"] > 85:
        recommendations.append("Inspect rotor alignment.")

    if row["water_flow"] < 20:
        recommendations.append("Inspect water circulation.")

    if not recommendations:
        recommendations.append("System operating normally.")

    return recommendations

@app.get("/recommendations")
def recommendations():

    df = pd.read_sql(
        """
        SELECT *
        FROM sensor_predictions
        ORDER BY id DESC
        LIMIT 1
        """,
        engine
    )

    row = df.iloc[0]

    return {
        "recommendations": get_recommendations(row)
    }

@app.get("/health")
def health():

    df = pd.read_sql(
        """
        SELECT anomaly
        FROM sensor_predictions
        ORDER BY id DESC
        LIMIT 500
        """,
        engine
    )

    total = len(df)

    normal = len(
        df[df["anomaly"] == "Normal"]
    )

    score = round(
        (normal / total) * 100,
        2
    )

    return {
        "health_score": score
    }