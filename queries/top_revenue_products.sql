SELECT product_id, SUM(total_revenue) as rev FROM df_orders GROUP BY product_id ORDER BY rev DESC LIMIT 10;
