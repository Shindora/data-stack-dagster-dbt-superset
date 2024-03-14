SELECT
    di.id AS item_id,
    di.name AS item_name,
    SUM(fo.total_price_usd) AS total_revenue
FROM
    {{ ref('fact_orders') }} fo
JOIN
    {{ ref('dim_items') }} di ON fo.item_id = di.id
GROUP BY
    di.id, di.name
ORDER BY
    total_revenue DESC