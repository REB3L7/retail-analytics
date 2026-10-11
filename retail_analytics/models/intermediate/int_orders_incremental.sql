{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

with historical_orders as (

    select
        order_id,
        customer_id,
        store_id,
        sales_channel,
        order_timestamp

    from read_parquet('../data/raw/orders_part_*.parquet')

),

incoming_orders as (

    select
        order_id,
        customer_id,
        store_id,
        sales_channel,
        order_timestamp

    from read_parquet('../data/incoming/orders_incremental_*.parquet')

),

all_orders as (

    select * from historical_orders

    union all

    select * from incoming_orders

)

select *
from all_orders

{% if is_incremental() %}

where order_id > (
    select coalesce(max(order_id), 0)
    from {{ this }}
)

{% endif %}