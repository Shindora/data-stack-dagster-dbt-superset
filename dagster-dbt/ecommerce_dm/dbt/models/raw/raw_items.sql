SELECT  
    *
FROM 
    {{ source('postgres', 'raw_items') }}
