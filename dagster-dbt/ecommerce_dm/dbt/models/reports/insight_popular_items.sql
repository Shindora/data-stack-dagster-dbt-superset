{{ config(
  materialized='table',
  unique_key='item_id'
) }}

select
    di.id as item_id,
    di.name as item_name,
    sum(fo.total_tax) as total_tax_generated,
    sum(fo.total_discounts) as total_discounts_given,
    sum(fo.total_price_usd) as total_revenue,
    sum(di.quantity) as total_quantity_ordered
from
    {{ ref('fact_orders') }} fo
join
    {{ ref('dim_items') }} di on fo.item_id = di.id
group by
    di.id, di.name