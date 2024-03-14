{{
config(
materialized = 'table',
unique_key = 'id'
)
}}

select *
from {{ref("staging_customers")}}