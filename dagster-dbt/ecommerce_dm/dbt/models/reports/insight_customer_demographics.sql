{{ config(
  materialized='table',
  unique_key='customer_id'
) }}

SELECT
    dc.id AS customer_id,
    dc.default_address_id,
    da.zip,
    da.province,
    da.country
FROM
    {{ ref('dim_customers') }} dc
LEFT JOIN
    {{ ref('dim_address') }} da ON dc.default_address_id = da.address_id