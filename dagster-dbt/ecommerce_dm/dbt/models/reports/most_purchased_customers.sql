{{ config(
  materialized='table',
  unique_key='customer_id'
) }}

SELECT
    dc.id AS customer_id,
    COUNT(fo.order_id) AS total_purchases,
    SUM(fo.total_price_usd) AS total_spent
FROM
    {{ ref('dim_customers') }} dc
LEFT JOIN
    {{ ref('fact_orders') }} fo ON dc.id = fo.customer_id
GROUP BY
    dc.id
ORDER BY
    total_purchases DESC