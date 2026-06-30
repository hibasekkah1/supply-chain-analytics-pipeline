{{ config(materialized='table', schema='gold') }}

select
    f.row_id,
    f.order_id,
    f.customer_id,
    f.product_id,
    f.order_date::date                      as date_key,
    {{ dbt_utils.generate_surrogate_key(['f.shipping_mode', 'f.delivery_status', 'f.order_region', 'f.order_country', 'f.order_city']) }} as shipping_key,
    f.order_type,
    f.days_shipping_real,
    f.days_shipment_scheduled,
    f.is_late_risk,
    f.quantity,
    f.sales,
    f.discount,
    f.discount_rate,
    f.order_total,
    f.profit,
    f.market
from {{ ref('stg_dataco') }} f
