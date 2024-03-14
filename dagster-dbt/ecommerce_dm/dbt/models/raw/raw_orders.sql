SELECT  
    *
FROM 
    {{ source('postgres','raw_orders') }}