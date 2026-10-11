select
    order_id,
    customer_id,
    store_id,
    sales_channel,
    order_timestamp

from read_parquet('../data/raw/orders_part_*.parquet')