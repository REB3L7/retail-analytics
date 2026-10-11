select
    store_id,
    store_name,
    state,
    city,
    opened_date

from read_parquet('../data/raw/stores.parquet')