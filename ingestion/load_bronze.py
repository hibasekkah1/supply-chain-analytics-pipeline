import pandas as pd
import psycopg2
from datetime import datetime
import os

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "supply_chain",
    "user": "hiba",
    "password": "hiba1234"
}

CSV_PATH = "data/DataCoSupplyChainDataset.csv"

def create_bronze_schema(cursor):
    cursor.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    cursor.execute("DROP TABLE IF EXISTS bronze.dataco_raw;")
    cursor.execute("""
        CREATE TABLE bronze.dataco_raw (
            row_id                          SERIAL PRIMARY KEY,
            type                            TEXT,
            days_for_shipping_real          TEXT,
            days_for_shipment_scheduled     TEXT,
            benefit_per_order               TEXT,
            sales_per_customer              TEXT,
            delivery_status                 TEXT,
            late_delivery_risk              TEXT,
            category_id                     TEXT,
            category_name                   TEXT,
            customer_city                   TEXT,
            customer_country                TEXT,
            customer_fname                  TEXT,
            customer_id                     TEXT,
            customer_lname                  TEXT,
            customer_segment                TEXT,
            customer_state                  TEXT,
            customer_street                 TEXT,
            customer_zipcode                TEXT,
            department_id                   TEXT,
            department_name                 TEXT,
            market                          TEXT,
            order_city                      TEXT,
            order_country                   TEXT,
            order_customer_id               TEXT,
            order_date_DateOrders           TEXT,
            order_id                        TEXT,
            order_item_cardprod_id          TEXT,
            order_item_discount             TEXT,
            order_item_discount_rate        TEXT,
            order_item_id                   TEXT,
            order_item_product_price        TEXT,
            order_item_profit_ratio         TEXT,
            order_item_quantity             TEXT,
            sales                           TEXT,
            order_item_total                TEXT,
            order_profit_per_order          TEXT,
            order_region                    TEXT,
            order_state                     TEXT,
            order_status                    TEXT,
            order_zipcode                   TEXT,
            product_card_id                 TEXT,
            product_category_id             TEXT,
            product_name                    TEXT,
            product_price                   TEXT,
            product_status                  TEXT,
            shipping_date_DateOrders        TEXT,
            shipping_mode                   TEXT,
            latitude                        TEXT,
            longitude                       TEXT,
            ingested_at                     TIMESTAMP DEFAULT NOW(),
            source_file                     TEXT
        );
    """)

def load_csv_to_bronze():
    print(f"[{datetime.now()}] Lecture du CSV...")
    df = pd.read_csv(
        CSV_PATH,
        encoding="latin-1",
        low_memory=False
    )

    # Nettoyer les noms de colonnes
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace("/", "_")
    )

    # Supprimer colonnes inutiles
    cols_to_drop = ["customer_email", "customer_password", 
                    "product_description", "product_image"]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

    # Ajouter métadonnées
    df["ingested_at"] = datetime.now()
    df["source_file"] = CSV_PATH

    print(f"[{datetime.now()}] {len(df)} lignes chargées.")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        print(f"[{datetime.now()}] Création du schéma Bronze...")
        create_bronze_schema(cursor)
        conn.commit()

        print(f"[{datetime.now()}] Insertion des données par batch...")
        batch_size = 1000
        cols = list(df.columns)
        placeholders = ",".join(["%s"] * len(cols))
        col_names = ",".join(cols)
        insert_query = f"INSERT INTO bronze.dataco_raw ({col_names}) VALUES ({placeholders})"

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            records = [tuple(x if pd.notna(x) else None for x in row) 
                      for row in batch.values]
            cursor.executemany(insert_query, records)
            conn.commit()
            print(f"  → {min(i+batch_size, len(df))}/{len(df)} lignes insérées")

        print(f"[{datetime.now()}] Ingestion Bronze terminée avec succès.")

    except Exception as e:
        conn.rollback()
        print(f"[{datetime.now()}] Erreur : {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_csv_to_bronze()