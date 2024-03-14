SELECT
    o.id AS order_id,
    o.customer_id,
    i.id as item_id,
    o.created_at,
    o.total_price_usd,
    o.total_tax,
    o.total_discounts,
    o.cancelled_at,
    {{ dbt_utils.generate_surrogate_key(
            [
                'COALESCE(o.billing_address__zip, \'\')',
                'COALESCE(o.billing_address__province, \'\')', 
                'COALESCE(o.billing_address__country, \'\')'
            ]
    ) }} as billing_address_id,
    {{ dbt_utils.generate_surrogate_key(
            [
                'COALESCE(o.shipping_address__zip, \'\')',
                'COALESCE(o.shipping_address__province, \'\')', 
                'COALESCE(o.shipping_address__country, \'\')'
            ]
    ) }} as shipping_address_id

FROM
    {{ ref('raw_orders') }} o
JOIN
    {{ ref('raw_items') }} i ON o.id = i.order_id
