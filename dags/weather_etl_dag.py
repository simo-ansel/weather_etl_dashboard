# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pendulum
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# PERCORSI PER SCRIPT DELLA ETL
# ─────────────────────────────────────────────────────────────────────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../etl')))

# ─────────────────────────────────────────────────────────────────────────────
# IMPORT DELLE FUNZIONI DELLA ETL
# ─────────────────────────────────────────────────────────────────────────────
from fetch_temperature import fetch_temperature
from fetch_humidity import fetch_humidity
from fetch_precipitation import fetch_precipitation
from fetch_wind import fetch_wind
from transform import transform_data
from load import load_data_to_postgres

# ─────────────────────────────────────────────────────────────────────────────
# DIRECTORY DATI
# ─────────────────────────────────────────────────────────────────────────────
DATA_DIR = '/opt/airflow/data'

# ─────────────────────────────────────────────────────────────────────────────
# FETCH TEMPERATURA
# ─────────────────────────────────────────────────────────────────────────────
def run_fetch_temperature():
    df = fetch_temperature()
    df.to_csv(f'{DATA_DIR}/temperature.csv', index=False)

# ─────────────────────────────────────────────────────────────────────────────
# FETCH UMIDITA'
# ─────────────────────────────────────────────────────────────────────────────
def run_fetch_humidity():
    df = fetch_humidity()
    df.to_csv(f'{DATA_DIR}/humidity.csv', index=False)

# ─────────────────────────────────────────────────────────────────────────────
# FETCH PRECIPITAZIONI
# ─────────────────────────────────────────────────────────────────────────────
def run_fetch_precipitation():
    df = fetch_precipitation()
    df.to_csv(f'{DATA_DIR}/precipitation.csv', index=False)

# ─────────────────────────────────────────────────────────────────────────────
# FETCH VENTO
# ─────────────────────────────────────────────────────────────────────────────
def run_fetch_wind():
    df = fetch_wind()
    df.to_csv(f'{DATA_DIR}/wind.csv', index=False)

# ─────────────────────────────────────────────────────────────────────────────
# TRASFORMAZIONE
# ─────────────────────────────────────────────────────────────────────────────
def run_transform():
    # ─────────────────────────────────────────────────────────────────────────────
    # CARICA I CSV PRODOTTI DALLE FETCH
    # ─────────────────────────────────────────────────────────────────────────────
    df_temp = pd.read_csv(f'{DATA_DIR}/temperature.csv', parse_dates=['datetime'])
    df_hum = pd.read_csv(f'{DATA_DIR}/humidity.csv', parse_dates=['datetime'])
    df_prec = pd.read_csv(f'{DATA_DIR}/precipitation.csv', parse_dates=['datetime'])
    df_wind = pd.read_csv(f'{DATA_DIR}/wind.csv', parse_dates=['datetime'])

    dfs = {
        'temperature': df_temp,
        'humidity': df_hum,
        'precipitation': df_prec,
        'wind': df_wind
    }

    # ─────────────────────────────────────────────────────────────────────────────
    # TRASFORMAZIONE DEI DATAFRAME
    # ─────────────────────────────────────────────────────────────────────────────
    (
        df_finale,
        df_temp_summary,
        df_temp_hourly,
        df_prec_hourly,
        df_hum_hourly,
        df_wind_hourly,
        alerts_df
    ) = transform_data(dfs)

    # ─────────────────────────────────────────────────────────────────────────────
    # SALVATAGGIO SU FILE CSV
    # ─────────────────────────────────────────────────────────────────────────────
    df_finale.to_csv(f'{DATA_DIR}/weather_weekly_transformed.csv', index=False)
    df_temp_summary.to_csv(f'{DATA_DIR}/daily_temperature_summary.csv', index=False)
    df_temp_hourly.to_csv(f'{DATA_DIR}/temperature_hourly.csv', index=False)
    df_prec_hourly.to_csv(f'{DATA_DIR}/precipitation_hourly.csv', index=False)
    df_hum_hourly.to_csv(f'{DATA_DIR}/humidity_hourly.csv', index=False)
    df_wind_hourly.to_csv(f'{DATA_DIR}/wind_hourly.csv', index=False)

# ─────────────────────────────────────────────────────────────────────────────
# CARICAMENTO NEL DATABASE
# ─────────────────────────────────────────────────────────────────────────────
def run_load():
    load_data_to_postgres()  # funzione che legge i csv e li carica nel DB

# ─────────────────────────────────────────────────────────────────────────────
# AIRFLOW DAG
# ─────────────────────────────────────────────────────────────────────────────

# Orario schedule di default
load_dotenv()

TIMEZONE = os.getenv("TIMEZONE", "Europe/Rome")
SCHEDULE = os.getenv("SCHEDULE", "0 0 * * *")  # default ogni giorno a mezzanotte

# Variabile personalizzabile
local_tz = pendulum.timezone(TIMEZONE)

with DAG(
    'weather_etl',
    start_date=datetime(2025, 5, 29, 0, 0, tzinfo=local_tz),
    schedule=SCHEDULE,
    catchup=False
) as dag:

    # ─────────────────────────────────────────────────────────────────────────────
    # TASK FETCH DATI
    # ─────────────────────────────────────────────────────────────────────────────
    task_temperature = PythonOperator(task_id='fetch_temperature', python_callable=run_fetch_temperature)
    task_humidity = PythonOperator(task_id='fetch_humidity', python_callable=run_fetch_humidity)
    task_precipitation = PythonOperator(task_id='fetch_precipitation', python_callable=run_fetch_precipitation)
    task_wind = PythonOperator(task_id='fetch_wind', python_callable=run_fetch_wind)

    # ─────────────────────────────────────────────────────────────────────────────
    # TASK TRASFORMAZIONE
    # ─────────────────────────────────────────────────────────────────────────────
    task_transform = PythonOperator(task_id='transform', python_callable=run_transform)

    # ─────────────────────────────────────────────────────────────────────────────
    # TASK DI CARICAMENTO
    # ─────────────────────────────────────────────────────────────────────────────
    task_load = PythonOperator(task_id='load', python_callable=run_load)

    # ─────────────────────────────────────────────────────────────────────────────
    # PIPELINE: FETCH (PARALLELE) --> TRASFORMAZIONE --> CARICAMENTO
    # ─────────────────────────────────────────────────────────────────────────────
    [task_temperature, task_humidity, task_precipitation, task_wind] >> task_transform >> task_load
