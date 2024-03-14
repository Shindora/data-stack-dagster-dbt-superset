WITH staging_address AS (
    SELECT DISTINCT
        default_address__zip as zip,
        default_address__province as province,
        default_address__country as country
    FROM
        {{ ref('raw_customers') }} 
    UNION
    SELECT DISTINCT
        billing_address__zip as zip,
        billing_address__province as province,
        billing_address__country as country
    FROM
        {{ ref('raw_orders') }}  
    UNION
    SELECT DISTINCT
        shipping_address__zip as zip,
        shipping_address__province as province,
        shipping_address__country as country
    FROM
        {{ ref('raw_orders') }}     
)

SELECT *
FROM staging_address
WHERE
    COALESCE(zip, province, country) IS NOT NULL
