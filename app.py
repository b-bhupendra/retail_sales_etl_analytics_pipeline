import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Retail Sales ETL", layout="wide")
st.title("🛍️ Retail Sales End-to-End ETL & Analytics Pipeline")

DB_PATH = "data/retail_sales.db"
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM df_orders", conn)
    conn.close()
    st.metric("Total Revenue", f"${df['total_revenue'].sum():,.2f}")
    st.dataframe(df.head(20))
