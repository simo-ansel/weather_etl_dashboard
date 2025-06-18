# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# TRASFORMA I DATI METEO
# ─────────────────────────────────────────────────────────────────────────────
def transform_data(dfs):
    # ─────────────────────────────────────────────────────────────────────────────
    # ESTRAZIONE DATI - TEMPERATURA
    # ─────────────────────────────────────────────────────────────────────────────
    df_temp = dfs['temperature']
    df_temp['date'] = df_temp['datetime'].dt.strftime('%d/%m/%Y')

    # ─────────────────────────────────────────────────────────────────────────────
    # TEMPERATURE MIN - MAX GIORNALIERE
    # ─────────────────────────────────────────────────────────────────────────────
    daily_temps = (
        df_temp.groupby('date')['temperature_2m']
        .agg(['min', 'max'])
        .rename(columns={'min': 'Temperatura Minima', 'max': 'Temperatura Massima'})
        .reset_index()
        .rename(columns={'date': 'Data'})
    )
    daily_temps['Data'] = pd.to_datetime(daily_temps['Data'], format='%d/%m/%Y')
    daily_temps['Data'] = daily_temps['Data'].dt.strftime('%d/%m/%Y')

    # ─────────────────────────────────────────────────────────────────────────────
    # MERGE DATI ORARI PER TRASFORMAZIONE
    # ─────────────────────────────────────────────────────────────────────────────
    df_merged = df_temp.copy()
    for key in ['humidity', 'precipitation', 'wind']:
        df_merged = pd.merge(df_merged, dfs[key], on='datetime', how='outer')

    df_merged = df_merged.sort_values('datetime').ffill().bfill()

    # ─────────────────────────────────────────────────────────────────────────────
    # FORMATTAZIONE DATA, ORA E FASCE ORARIE
    # ─────────────────────────────────────────────────────────────────────────────
    df_merged['Data'] = df_merged['datetime'].dt.strftime('%d/%m/%Y')
    df_merged['Ora'] = df_merged['datetime'].dt.strftime('%H:%M')

    def get_period(ora):
        h = int(ora.split(':')[0])
        if 6 <= h < 12: return 'Mattina'
        elif 12 <= h < 18: return 'Pomeriggio'
        elif 18 <= h < 24: return 'Sera'
        return 'Notte'

    df_merged['Fascia Oraria'] = df_merged['Ora'].apply(get_period)

    # ─────────────────────────────────────────────────────────────────────────────
    # RINOMINA DELLE COLONNE
    # ─────────────────────────────────────────────────────────────────────────────
    df_merged.rename(columns={
        'temperature_2m': 'Temperatura (°C)',
        'apparent_temperature': 'Temperatura Percepita (°C)',
        'relative_humidity_2m': 'Umidità (%)',
        'precipitation': 'Precipitazioni (mm)',
        'precipitation_probability': 'Probabilità di Precipitazione',
        'windspeed_10m': 'Velocità Vento (km/h)',
        'windgusts_10m': 'Raffiche di Vento (km/h)'
    }, inplace=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # CLASSIFICAZIONI PER ALLERTA METEO
    # ─────────────────────────────────────────────────────────────────────────────
    def classify_weather(row):
        if row['Precipitazioni (mm)'] > 10:
            return "Pioggia intensa"
        elif row['Velocità Vento (km/h)'] > 50:
            return "Vento forte"
        elif row['Temperatura (°C)'] > 35:
            return "Caldo estremo"
        elif row['Temperatura (°C)'] < 0:
            return "Freddo estremo"
        return "Normale"

    df_merged['Allerta Meteo'] = df_merged.apply(classify_weather, axis=1)

    # ─────────────────────────────────────────────────────────────────────────────
    # TABELLE SEPARATE
    # ─────────────────────────────────────────────────────────────────────────────
    base_cols = ['datetime', 'Data', 'Ora']
    temperature_hourly = df_merged[base_cols + ['Temperatura (°C)', 'Temperatura Percepita (°C)']]
    precipitation_hourly = df_merged[base_cols + ['Precipitazioni (mm)', 'Probabilità di Precipitazione']]
    humidity_hourly = df_merged[base_cols + ['Umidità (%)']]
    wind_hourly = df_merged[base_cols + ['Velocità Vento (km/h)', 'Raffiche di Vento (km/h)']]

    # ─────────────────────────────────────────────────────────────────────────────
    # ALLERTA METEO
    # ─────────────────────────────────────────────────────────────────────────────
    alerts_df = (
        df_merged[df_merged['Allerta Meteo'] != 'Normale']
        [['Data', 'Fascia Oraria', 'Allerta Meteo']]
        .drop_duplicates()
        .sort_values('Data')
        .reset_index(drop=True)
    )

    alerts_df.to_csv('/opt/airflow/data/weather_alerts.csv', index=False)

    # ─────────────────────────────────────────────────────────────────────────────
    # RITORNA TABELLE PRONTA AL CARICAMENTO
    # ─────────────────────────────────────────────────────────────────────────────
    return (
        df_merged,
        daily_temps,
        temperature_hourly,
        precipitation_hourly,
        humidity_hourly,
        wind_hourly,
        alerts_df
    )
