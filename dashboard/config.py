# ─────────────────────────────────────────────────────────────────────────────
# IMPORT LIBRERIE
# ─────────────────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# ─────────────────────────────────────────────────────────────────────────────
# CARICAMENTO VARIABILI DA FILE .env
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# CONNESSIONE AL DATABASE POSTGRESQL
# ─────────────────────────────────────────────────────────────────────────────
def get_db_engine():
    # ─────────────────────────────────────────────────────────────────────────────
    # PARAMETRI PER CONNESSIONE AL DATABASE
    # ─────────────────────────────────────────────────────────────────────────────
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    # ─────────────────────────────────────────────────────────────────────────────
    # COSTRUZIONE DELL'ENGINE CON SQLALCHEMY
    # ─────────────────────────────────────────────────────────────────────────────
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # ─────────────────────────────────────────────────────────────────────────────
    # RITORNA UN OGGETTO ENGINE PER CONNETTERSI AL DATABASE
    # ─────────────────────────────────────────────────────────────────────────────
    return engine
