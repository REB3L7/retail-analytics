select
    product_id,
    product_name,
    category,
    price

from read_parquet('../data/raw/products.parquet')