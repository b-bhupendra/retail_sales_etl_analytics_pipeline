WITH MonthlySales AS (
    SELECT order_year_month, SUM(total_revenue) as monthly_revenue FROM df_orders GROUP BY order_year_month
)
SELECT order_year_month, monthly_revenue, LAG(monthly_revenue, 1) OVER (ORDER BY order_year_month) as prev FROM MonthlySales;
