{{ config(materialized='table', schema='gold') }}

with dates as (
    select distinct order_date::date as date_day
    from {{ ref('stg_dataco') }}
)

select
    date_day                                as date_key,
    extract(year from date_day)             as year,
    extract(quarter from date_day)          as quarter,
    extract(month from date_day)            as month,
    to_char(date_day, 'Month')              as month_name,
    extract(week from date_day)             as week,
    extract(dow from date_day)              as day_of_week,
    to_char(date_day, 'Day')                as day_name
from dates