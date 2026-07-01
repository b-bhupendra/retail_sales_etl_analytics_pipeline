import pandas as pd
def transform_data(df): df['total_revenue'] = df['Quantity'] * df['List Price']; return df
