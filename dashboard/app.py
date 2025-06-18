# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from config import get_db_engine
from data_access import (
    load_temperature_daily,
    load_temperature_hourly,
    load_precipitation_hourly,
    load_humidity_hourly,
    load_wind_hourly,
    load_weather_alerts
)
from charts import (
    temperature_hourly_chart,
    temperature_weekly_chart,
    temperature_daily_min_max_chart,
    precipitation_daily_chart,
    precipitation_weekly_chart,
    humidity_daily_chart,
    humidity_weekly_chart,
    wind_daily_chart,
    wind_weekly_chart,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAZIONE INIZIALE DELLA PAGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard Meteo", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# FUNZIONE PER CARICARE I DATI IN CACHE
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def load_all_data(_engine):
    return (
        load_temperature_daily(_engine),
        load_temperature_hourly(_engine),
        load_precipitation_hourly(_engine),
        load_humidity_hourly(_engine),
        load_wind_hourly(_engine),
    )

# ─────────────────────────────────────────────────────────────────────────────
# RIMUOVE COLONNA DATETIME DAI DATAFRAME
# ─────────────────────────────────────────────────────────────────────────────
def hide_datetime_columns(df):
    datetime_cols = df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
    return df.drop(columns=datetime_cols)

# ─────────────────────────────────────────────────────────────────────────────
# FUNZIONE MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # ─────────────────────────────────────────────────────────────────────────────
    # TITOLO CENTRALE
    # ─────────────────────────────────────────────────────────────────────────────
    st.markdown(
        "<h1 style='text-align: center;'>🌤️ Dashboard Meteo 🌦️</h1>",
        unsafe_allow_html=True
    )

    # ─────────────────────────────────────────────────────────────────────────────
    # CARICAMENTO DATI DAL DATABASE
    # ─────────────────────────────────────────────────────────────────────────────
    engine = get_db_engine()
    temp_daily, temp_hourly, prec_hourly, humidity_hourly, wind_hourly = load_all_data(engine)

    # ─────────────────────────────────────────────────────────────────────────────
    # SIDEBAR: NAVIGAZIONE E SELEZIONE DATA
    # ─────────────────────────────────────────────────────────────────────────────
    st.sidebar.title("Navigazione")
    page = st.sidebar.selectbox(
        "Seleziona sezione",
        [
            "Temperature 🌡️",
            "Precipitazioni 🌧️",
            "Umidità 💧",
            "Vento 🌬️"
        ]
    )

    available_dates = sorted(temp_hourly["Data"].unique(), reverse=True)
    selected_date = st.sidebar.selectbox("Seleziona data", available_dates)

    # ─────────────────────────────────────────────────────────────────────────────
    # TITOLO PAGINA SELEZIONATA
    # ─────────────────────────────────────────────────────────────────────────────
    st.markdown(
        f"<h2 style='text-align: center;'>{page}</h2>",
        unsafe_allow_html=True
    )

    # ─────────────────────────────────────────────────────────────────────────────
    # TEMPERATURA
    # ─────────────────────────────────────────────────────────────────────────────
    if "Temperature" in page:
        filtered_temp = temp_hourly[temp_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌡️ Temperature orarie - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_temp), width=1000)
            st.altair_chart(temperature_hourly_chart(filtered_temp), use_container_width=True)

        with col2:
            st.subheader("📅 Temperature settimanali")
            st.altair_chart(temperature_weekly_chart(temp_hourly), use_container_width=True)

        with col2:
            st.subheader("🌡️ Minime e massime giornaliere")
            st.altair_chart(temperature_daily_min_max_chart(temp_daily), use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # PRECIPITAZIONI
    # ─────────────────────────────────────────────────────────────────────────────
    elif "Precipitazioni" in page:
        filtered_prec = prec_hourly[prec_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌧️ Precipitazioni orarie - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_prec), width=1000)
            st.altair_chart(precipitation_daily_chart(filtered_prec), use_container_width=True)

        with col2:
            st.subheader("📅 Precipitazioni settimanali")
            st.altair_chart(precipitation_weekly_chart(prec_hourly), use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # UMIDITA'
    # ─────────────────────────────────────────────────────────────────────────────
    elif "Umidità" in page:
        filtered_humidity = humidity_hourly[humidity_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"💧 Umidità oraria - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_humidity), width=1000)
            st.altair_chart(humidity_daily_chart(filtered_humidity), use_container_width=True)

        with col2:
            st.subheader("📅 Umidità settimanale")
            st.altair_chart(humidity_weekly_chart(humidity_hourly), use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # VENTO
    # ─────────────────────────────────────────────────────────────────────────────
    elif "Vento" in page:
        filtered_wind = wind_hourly[wind_hourly["Data"] == selected_date]

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.subheader(f"🌬️ Vento orario - {selected_date}")
            st.dataframe(hide_datetime_columns(filtered_wind), width=1000)
            st.altair_chart(wind_daily_chart(filtered_wind), use_container_width=True)

        with col2:
            st.subheader("📅 Vento settimanale")
            st.altair_chart(wind_weekly_chart(wind_hourly), use_container_width=True)

    # ─────────────────────────────────────────────────────────────────────────────
    # ALLERTA METEO
    # ─────────────────────────────────────────────────────────────────────────────
    alerts_df = load_weather_alerts(engine)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if alerts_df.empty:
            st.markdown("## ✅ Allerta Meteo")
            st.info("Nessuna allerta meteo attiva.")
        else:
            st.markdown("## ⚠️ Allerta Meteo")
            st.dataframe(alerts_df, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
