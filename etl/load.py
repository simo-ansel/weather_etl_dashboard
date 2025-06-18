# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import os
import pandas as pd
from sqlalchemy import create_engine

# ─────────────────────────────────────────────────────────────────────────────
# CREDENZIALI DEL DATABASE DALLE VARIABILI D'AMBIENTE
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI NEL DATABASE
# ─────────────────────────────────────────────────────────────────────────────
def load_data_to_postgres():
    # ─────────────────────────────────────────────────────────────────────────────
    # DIRECTORY DEI CSV GENERATI
    # ─────────────────────────────────────────────────────────────────────────────
    data_dir = "/opt/airflow/data"

    # ─────────────────────────────────────────────────────────────────────────────
    # MAPPA I NOMI DEI FILE NEI NOMI DELLE TABELLE
    # ─────────────────────────────────────────────────────────────────────────────
    files_to_tables = {
        "weather_weekly_transformed.csv": "weather_hourly_one_week",
        "daily_temperature_summary.csv": "temperature_daily_summary",
        "temperature_hourly.csv": "temperature_hourly",
        "precipitation_hourly.csv": "precipitation_hourly",
        "humidity_hourly.csv": "humidity_hourly",
        "wind_hourly.csv": "wind_hourly",
        "weather_alerts.csv": "weather_alerts"
    }

    # ─────────────────────────────────────────────────────────────────────────────
    # CONNESSIONE AL DATABASE
    # ─────────────────────────────────────────────────────────────────────────────
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # ─────────────────────────────────────────────────────────────────────────────
    # CARICAMENTO E SCRITTURA DI OGNI FILE NEL DATABASE
    # ─────────────────────────────────────────────────────────────────────────────
    for filename, table_name in files_to_tables.items():
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
