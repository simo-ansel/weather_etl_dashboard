# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAZIONE API
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

LAT = os.getenv("LAT", "41.8919")
LON = os.getenv("LON", "12.5113")
TIMEZONE = os.getenv("TIMEZONE", "Europe/Rome")

BASE_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "hourly": "windspeed_10m,windgusts_10m",
    "timezone": TIMEZONE
}

# ─────────────────────────────────────────────────────────────────────────────
# FETCH PER I DATI DEL VENTO
# ─────────────────────────────────────────────────────────────────────────────
def fetch_wind():
    # ─────────────────────────────────────────────────────────────────────────────
    # CHIAMATA API
    # ─────────────────────────────────────────────────────────────────────────────
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status() # Solleva eccezione in caso di error

    # ─────────────────────────────────────────────────────────────────────────────
    # PARSING E SELEZIONE DATI
    # ─────────────────────────────────────────────────────────────────────────────
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["datetime"] = pd.to_datetime(df["time"])
    df = df[["datetime", "windspeed_10m", "windgusts_10m"]]

    # ─────────────────────────────────────────────────────────────────────────────
    # SALVATAGGIO SU FILE CSV
    # ─────────────────────────────────────────────────────────────────────────────
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "wind.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
