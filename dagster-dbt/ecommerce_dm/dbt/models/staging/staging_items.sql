select 
    id,
    name,
    price,
    quantity,
    taxable,
    total_discount,
    pre_tax_price

from {{ref('raw_items')}}