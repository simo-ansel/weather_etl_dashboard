# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# FUNZIONE AUSILIARIA PER CARICARE I DATI DAL DATABASE
# ─────────────────────────────────────────────────────────────────────────────
def load_table_with_datetime(engine, table_name, date_col="Data", time_col="Ora", datetime_col="datetime", fmt="%d/%m/%Y %H:%M"):
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    df.columns = [c.strip() for c in df.columns]
    df[datetime_col] = pd.to_datetime(df[date_col] + " " + df[time_col], format=fmt)
    return df

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DELLA TEMPERATURA
# ─────────────────────────────────────────────────────────────────────────────
def load_temperature_hourly(engine):
    return load_table_with_datetime(engine, "temperature_hourly")

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DELLE PRECIPITAZIONI
# ─────────────────────────────────────────────────────────────────────────────
def load_precipitation_hourly(engine):
    return load_table_with_datetime(engine, "precipitation_hourly")

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DELL'UMIDITA'
# ─────────────────────────────────────────────────────────────────────────────
def load_humidity_hourly(engine):
    return load_table_with_datetime(engine, "humidity_hourly")

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DEL VENTO
# ─────────────────────────────────────────────────────────────────────────────
def load_wind_hourly(engine):
    return load_table_with_datetime(engine, "wind_hourly")

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DELLA TEMPERATURA
# ─────────────────────────────────────────────────────────────────────────────
def load_temperature_daily(engine):
    # Esegue una query per caricare l'intera tabella
    df = pd.read_sql("SELECT * FROM temperature_daily_summary", engine)

    # Rimuove eventuali spazi bianchi dai nomi delle colonne
    df.columns = [c.strip() for c in df.columns]

    # Converte la colonna 'Data' in oggetto datetime (formato: giorno/mese/anno)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

    return df

# ─────────────────────────────────────────────────────────────────────────────
# CARICA I DATI DELL'ALLERTA METEO
# ─────────────────────────────────────────────────────────────────────────────
def load_weather_alerts(engine):
    df = pd.read_sql("SELECT * FROM weather_alerts", engine)
    df.columns = [c.strip() for c in df.columns]

    return df
