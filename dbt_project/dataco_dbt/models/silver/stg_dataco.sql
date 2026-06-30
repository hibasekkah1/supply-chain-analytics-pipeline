{{
  config(
    materialized='table',
    schema='silver'
  )
}}

with source as (
    select * from {{ source('bronze', 'dataco_raw') }}
),

cleaned as (
    select
        row_id,
        type                                            as order_type,
        days_for_shipping_real::numeric                 as days_shipping_real,
        days_for_shipment_scheduled::numeric             as days_shipment_scheduled,
        benefit_per_order::numeric                       as benefit_per_order,
        sales_per_customer::numeric                      as sales_per_customer,
        delivery_status,
        case when late_delivery_risk = '1' then true else false end as is_late_risk,
        category_id::integer                             as category_id,
        category_name,
        customer_city,
        customer_country,
        customer_id::integer                             as customer_id,
        customer_fname,
        customer_lname,
        customer_segment,
        customer_state,
        customer_zipcode,
        department_id::integer                           as department_id,
        department_name,
        market,
        order_city,
        order_country,
        order_customer_id::integer                       as order_customer_id,
        to_timestamp(order_date_dateOrders, 'MM/DD/YYYY HH24:MI')    as order_date,
        order_id::integer                                as order_id,
        order_item_cardprod_id::integer                  as product_id,
        order_item_discount::numeric                     as discount,
        order_item_discount_rate::numeric                as discount_rate,
        order_item_quantity::numeric                     as quantity,
        sales::numeric                                   as sales,
        order_item_total::numeric                        as order_total,
        order_profit_per_order::numeric                  as profit,
        order_region,
        order_state,
        order_status,
        product_name,
        product_price::numeric                           as product_price,
        to_timestamp(shipping_date_dateOrders, 'MM/DD/YYYY HH24:MI') as shipping_date,
        shipping_mode
    from source
    where order_id is not null
)

select * from cleaned