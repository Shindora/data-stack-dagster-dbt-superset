SELECT 
    id,
    created_at,
    email,
    {{ dbt_utils.generate_surrogate_key(
            ['COALESCE(default_address__zip, \'\')',
            'COALESCE(default_address__province, \'\')', 
            'COALESCE(default_address__country, \'\')']
    ) }} as default_address_id
FROM {{ ref('raw_customers') }}
