select
    order_id,
    product_id,
    quantity

from read_parquet('../data/raw/order_items_part_*.parquet')