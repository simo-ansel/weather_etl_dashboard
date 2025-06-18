# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import os
import requests
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAZIONE API
# ─────────────────────────────────────────────────────────────────────────────
BASE_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 41.8919,
    "longitude": 12.5113,
    "hourly": "precipitation,precipitation_probability",
    "timezone": "Europe/Rome"
}

# ─────────────────────────────────────────────────────────────────────────────
# FETCH PER DATI DELLE PRECIPITAZINOI
# ─────────────────────────────────────────────────────────────────────────────
def fetch_precipitation():
    # ─────────────────────────────────────────────────────────────────────────────
    # CHIAMATA API
    # ─────────────────────────────────────────────────────────────────────────────
    response = requests.get(BASE_URL, params=PARAMS)
    response.raise_for_status() # Solleva eccezione in caso di errore

    # ─────────────────────────────────────────────────────────────────────────────
    # PARSING E SELEZIONE DATI
    # ─────────────────────────────────────────────────────────────────────────────
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["datetime"] = pd.to_datetime(df["time"])
    df = df[["datetime", "precipitation", "precipitation_probability"]]

    # ─────────────────────────────────────────────────────────────────────────────
    # SALVATAGGIO SU FILE CSV
    # ─────────────────────────────────────────────────────────────────────────────
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "precipitation.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
