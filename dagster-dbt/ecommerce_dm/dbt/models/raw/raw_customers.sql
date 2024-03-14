SELECT  
    *
FROM 
    {{ source('postgres','raw_customers') }}