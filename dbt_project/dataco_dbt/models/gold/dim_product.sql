{{ config(materialized='table', schema='gold') }}

select distinct
    product_id,
    product_name,
    product_price,
    category_id,
    category_name,
    department_id,
    department_name
from {{ ref('stg_dataco') }}