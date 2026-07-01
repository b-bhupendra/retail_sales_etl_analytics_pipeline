import pandas as pd

def transform_data(df):
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
    df_clean['order_year_month'] = df_clean['order_date'].dt.strftime('%Y-%m')
    
    df_clean['discount_amount'] = (df_clean['list_price'] * (df_clean['discount_percent'] / 100.0))
    df_clean['selling_price'] = df_clean['list_price'] - df_clean['discount_amount']
    
    df_clean['total_revenue'] = round(df_clean['quantity'] * df_clean['selling_price'], 2)
    df_clean['total_cost'] = round(df_clean['quantity'] * df_clean['cost_price'], 2)
    df_clean['net_profit'] = round(df_clean['total_revenue'] - df_clean['total_cost'], 2)
    df_clean['profit_margin_pct'] = round((df_clean['net_profit'] / df_clean['total_revenue']) * 100, 2)
    
    return df_clean
