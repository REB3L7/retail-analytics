select
    customer_id,
    name,
    email,
    state,
    loyalty_member,
    signup_date

from read_parquet('../data/raw/customers.parquet')