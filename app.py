import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
from src.load import run_pipeline, DB_PATH

st.set_page_config(page_title="Retail Sales ETL Analytics", page_icon="🛍️", layout="wide")

if not os.path.exists(DB_PATH):
    run_pipeline()

@st.cache_data
def load_db_table(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🛍️ Retail Sales End-to-End ETL & Analytics Pipeline")

df_orders = load_db_table("SELECT * FROM df_orders")

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Revenue", f"${df_orders['total_revenue'].sum():,.2f}")
k2.metric("📈 Net Profit", f"${df_orders['net_profit'].sum():,.2f}")
k3.metric("📊 Avg Profit Margin", f"{df_orders['profit_margin_pct'].mean():.2f}%")
k4.metric("📦 Total Orders", f"{len(df_orders):,}")

st.divider()

t1, t2, t3, t4 = st.tabs(["📈 Sales & Profit Overview", "🏆 Top Products", "📅 MoM Growth", "🔍 Data Explorer"])

with t1:
    col1, col2 = st.columns(2)
    with col1:
        cat_df = df_orders.groupby("category")[["total_revenue", "net_profit"]].sum().reset_index()
        fig_cat = px.bar(cat_df, x="category", y=["total_revenue", "net_profit"], barmode="group", title="Revenue & Profit by Category")
        st.plotly_chart(fig_cat, use_container_width=True)
    with col2:
        fig_pie = px.pie(cat_df, names="category", values="total_revenue", title="Revenue Share by Category", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

with t2:
    st.subheader("Top 10 Revenue-Generating Products")
    top_prod_query = """
    SELECT product_id, category, sub_category, SUM(quantity) AS total_units_sold, ROUND(SUM(total_revenue), 2) AS total_revenue
    FROM df_orders GROUP BY product_id, category, sub_category ORDER BY total_revenue DESC LIMIT 10;
    """
    df_top = load_db_table(top_prod_query)
    fig_top = px.bar(df_top, x="product_id", y="total_revenue", color="category", hover_data=["sub_category", "total_units_sold"], title="Top 10 Products by Revenue")
    st.plotly_chart(fig_top, use_container_width=True)
    st.dataframe(df_top, use_container_width=True)

with t3:
    st.subheader("Month-over-Month (MoM) Growth Analysis")
    mom_query = """
    WITH MonthlySales AS (
        SELECT order_year_month, ROUND(SUM(total_revenue), 2) AS monthly_revenue, ROUND(SUM(net_profit), 2) AS monthly_profit FROM df_orders GROUP BY order_year_month
    ),
    MonthlyGrowth AS (
        SELECT order_year_month, monthly_revenue, LAG(monthly_revenue, 1, monthly_revenue) OVER (ORDER BY order_year_month ASC) AS prev_month_revenue, monthly_profit FROM MonthlySales
    )
    SELECT order_year_month, monthly_revenue, prev_month_revenue, CASE WHEN prev_month_revenue = 0 THEN 0.0 ELSE ROUND(((monthly_revenue - prev_month_revenue) / prev_month_revenue) * 100.0, 2) END AS mom_growth_pct, monthly_profit FROM MonthlyGrowth ORDER BY order_year_month ASC;
    """
    df_mom = load_db_table(mom_query)
    fig_mom = px.line(df_mom, x="order_year_month", y="monthly_revenue", markers=True, title="Monthly Revenue Trend ($)")
    st.plotly_chart(fig_mom, use_container_width=True)
    st.dataframe(df_mom, use_container_width=True)

with t4:
    st.subheader("Raw Orders Dataset")
    st.dataframe(df_orders, use_container_width=True)
