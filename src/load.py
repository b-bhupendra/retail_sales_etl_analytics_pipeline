import os, sqlite3, pandas as pd
from src.extract import extract_data
from src.transform import transform_data

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "retail_sales.db")

def load_to_db(df):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("df_orders", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    df = transform_data(extract_data())
    load_to_db(df)
