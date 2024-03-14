{{ config(
    materialized = 'table',
    unique_key = ['order_sk']
) }}

SELECT 
    {{ dbt_utils.generate_surrogate_key(
            [
                'order_id', 
                'item_id',  
                'customer_id'
            ]
        ) 
    }} as order_sk,
    *
FROM {{ ref("staging_orders") }}


