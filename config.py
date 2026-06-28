# ==========================
# DATABASE CONFIGURATION
# ==========================

DB_USER = "postgres"
DB_PASSWORD = "Sanket7721"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Predictive_Maintainence"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================
# APPLICATION SETTINGS
# ==========================

UPDATE_INTERVAL = 5        # seconds

LIVE_MODE = True           # Try live sensors first

FAULT_PROBABILITY = 0.10   # 10% abnormal readings in simulator

MODEL_CONTAMINATION = 0.01

RANDOM_STATE = 42