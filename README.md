## Weather ETL Dashboard

Progetto ETL per l’estrazione, trasformazione e caricamento di dati meteorologici in un database PostgreSQL, con visualizzazione tramite una dashboard interattiva sviluppata con Streamlit.

La pipeline salva anche i dati trasformati in file CSV per ogni tipologia di informazione raccolta.

La raccolta dei dati è automatizzata tramite una DAG schedulata in Apache Airflow. Tutto il sistema è containerizzato con Docker Compose.

---

## Contenuti

- [Descrizione](#descrizione)  
- [Prerequisiti](#prerequisiti)  
- [Setup e configurazione](#setup-e-configurazione)  
- [Avvio del progetto](#avvio-del-progetto)  
- [Accesso e utilizzo](#accesso-e-utilizzo)  
  - [Accesso alla dashboard](#accesso-alla-dashboard)  
  - [Accesso all’interfaccia Airflow](#accesso-allinterfaccia-airflow)  
  - [Verifica dati nel database](#verifica-dati-nel-database)  
- [Output della pipeline](#output-della-pipeline)  
- [Credenziali](#credenziali)  
- [Pulizia dell’ambiente](#pulizia-dellambiente)  

---

## Descrizione

Questo progetto implementa una pipeline ETL completa per raccogliere dati meteorologici, elaborarli e salvarli in un database PostgreSQL.

La raccolta è automatizzata tramite una DAG definita in Apache Airflow, schedulata per l’esecuzione quotidiana a mezzanotte (ora locale).

I dati vengono successivamente visualizzati in una dashboard interattiva realizzata con Streamlit, e salvati anche in formato CSV nella cartella data/, per analisi o uso esterno.

L’intero sistema è containerizzato e gestito tramite Docker Compose, per facilitare l’installazione e l’esecuzione.

---

## Prerequisiti

- Docker (versione 20.x o superiore)  
- Docker Compose integrato (`docker compose`) o CLI standalone (`docker-compose` versione 1.29.x o superiore)

---

## Setup e configurazione

1. Clona il repository:

    ```bash
    git clone https://github.com/simo-ansel/weather_etl_dashboard.git
    cd weather_etl_dashboard
    ```

2. (Opzionale) Modifica `requirements.txt` per aggiungere o aggiornare dipendenze Python.

3. Crea un file `.env` nella root del progetto con le variabili d’ambiente per la connessione al database, la località geografica, il fuso orario e la schedulazione della DAG.
   Esempio di contenuto:

    ```
    # Credenziali per il DB PostgreSQL
    DB_NAME=airflow
    DB_USER=airflow
    DB_PASS=airflow
    DB_HOST=postgres
    DB_PORT=5432

    # Coordinate geografiche per dati API
    LAT=41.8919             # latitudine
    LON=12.5113             # longitudine

    TIMEZONE=Europe/Rome    # Timezone DAG e API

    SCHEDULE=0 0 * * *      # Orario di esecuzione DAG (orario UTC, non del timezone)
    ```

> **Nota:** puoi modificare queste variabili per adattare il progetto al tuo ambiente, posizione geografica, fuso orario e frequenza di esecuzione desiderata.

4. (Opzionale) Se preferisci, puoi modificare direttamente il file della DAG (`dags/weather_etl.py`) per cambiare `schedule_interval`, ma l’uso della variabile `SCHEDULE` nel `.env` è consigliato per una gestione più flessibile.

5. Preparazione della cartella data

    Prima di avviare i container, crea la cartella data e assegna i permessi corretti:

    ```bash
    mkdir -p data
    sudo chown -R 50000:50000 data
    ```

> **Nota:** L’UID 50000 è quello con cui gira Airflow nel container. Questa operazione serve solo la prima volta per permettere ai container di scrivere correttamente nella cartella.

---

## Avvio del progetto

Avvia tutti i container con:

```bash
docker compose up
```

Questo comando avvierà:

- Il database PostgreSQL

- L’interfaccia web di Airflow, disponibile su http://localhost:8080

- La dashboard Streamlit, disponibile su http://localhost:8501

La DAG weather_etl è preconfigurata per eseguire l’estrazione dei dati ogni giorno a mezzanotte ora locale. Puoi anche avviarla manualmente dall’interfaccia di Airflow.

Il database verrà popolato automaticamente con i dati meteo raccolti.

---

## Accesso e utilizzo

## Accesso alla dashboard

La dashboard interattiva è accessibile all’indirizzo: http://localhost:8501

Visualizza dati in tempo reale su:

- Temperature (orarie, giornaliere, settimanali)

- Precipitazioni

- Umidità

- Vento

- Allerte meteo

## Accesso all’interfaccia Airflow

L’interfaccia web di Airflow è raggiungibile su: http://localhost:8080

Puoi:

- Monitorare lo stato delle DAG

- Eseguire manualmente la DAG weather_etl

- Visualizzare log e dettagli dei task

## Verifica dati nel database

Per connetterti al database PostgreSQL ed eseguire query SQL, puoi entrare nel container del DB:

```bash
docker exec -it weatheretl_db_1 psql -U airflow -d airflow
```

Esempio di query:

```sql
SELECT * FROM temperature_hourly LIMIT 10;
```

---

## Output della pipeline

Oltre al caricamento dei dati meteorologici nel database PostgreSQL e alla visualizzazione tramite la dashboard Streamlit, la pipeline ETL genera anche file CSV con i dati estratti e trasformati.

Questi file CSV vengono salvati nella cartella data all’interno del progetto.
La cartella viene creata automaticamente dal codice se non esiste.

---

## Credenziali

Airflow UI

- Username: admin

- Password: admin

Database PostgreSQL

Usa le credenziali specificate nel file .env (di default):

- Host: postgres

- Porta: 5432

- Nome del Database: airflow

- Username: airflow

- Password: airflow

---

## Pulizia dell’ambiente

Per fermare e rimuovere container, network e volumi associati:

```bash
docker compose down -v
```

Per liberare spazio eliminando immagini Docker inutilizzate:

```bash
docker image prune -a
```

Attenzione: il comando sopra eliminerà tutte le immagini non collegate a container attivi.

---

## Grazie per aver usato Weather ETL Dashboard!
