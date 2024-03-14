{{ config(
  materialized='table',
  unique_key='item_id'
) }}

SELECT
    di.id AS item_id,
    di.name AS item_name,
    SUM(fo.total_price_usd) AS total_sales_usd
FROM
    {{ ref('fact_orders') }} fo
JOIN
    {{ ref('dim_items') }} di ON fo.item_id = di.id
GROUP BY
    di.id, di.name