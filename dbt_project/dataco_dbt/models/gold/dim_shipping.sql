{{ config(materialized='table', schema='gold') }}

select distinct
    {{ dbt_utils.generate_surrogate_key(['shipping_mode', 'delivery_status', 'order_region', 'order_country', 'order_city']) }} as shipping_key,
    shipping_mode,
    delivery_status,
    order_region,
    order_state,
    order_country,
    order_city
from {{ ref('stg_dataco') }}