{{
config(
materialized = 'table',
unique_key = 'address_id'
)
}}


SELECT 
    {{ dbt_utils.generate_surrogate_key(
            [
                'COALESCE(zip, \'\')',
                'COALESCE(province, \'\')', 
                'COALESCE(country, \'\')'
            ]
    ) }} as address_id,
    zip,
    province,
    country
FROM 
    {{ ref('staging_address') }}
