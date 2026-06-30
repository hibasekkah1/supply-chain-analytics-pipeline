{{ config(materialized='table', schema='gold') }}

select distinct
    customer_id,
    customer_fname,
    customer_lname,
    customer_segment,
    customer_city,
    customer_state,
    customer_country,
    customer_zipcode
from {{ ref('stg_dataco') }}