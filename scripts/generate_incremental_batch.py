import random
from datetime import datetime, timedelta

import pandas as pd


random.seed(100)

START_ORDER_ID = 1_000_001
NUM_NEW_ORDERS = 100_000

NUM_CUSTOMERS = 100_000
NUM_STORES = 2_000
NUM_PRODUCTS = 10_000

START_DATE = datetime(2026, 10, 1)
END_DATE = datetime(2026, 10, 7)

DATE_RANGE = (END_DATE - START_DATE).days


def random_date():
    return START_DATE + timedelta(
        days=random.randint(0, DATE_RANGE),
        seconds=random.randint(0, 86399)
    )


orders = []
order_items = []

for order_id in range(
    START_ORDER_ID,
    START_ORDER_ID + NUM_NEW_ORDERS
):

    sales_channel = random.choices(
        ["STORE", "ONLINE"],
        weights=[70, 30],
        k=1
    )[0]

    store_id = (
        random.randint(1, NUM_STORES)
        if sales_channel == "STORE"
        else None
    )

    orders.append({
        "order_id": order_id,
        "customer_id": random.randint(1, NUM_CUSTOMERS),
        "store_id": store_id,
        "sales_channel": sales_channel,
        "order_timestamp": random_date(),
    })

    num_items = random.randint(1, 5)

    selected_products = random.sample(
        range(1, NUM_PRODUCTS + 1),
        num_items
    )

    for product_id in selected_products:
        order_items.append({
            "order_id": order_id,
            "product_id": product_id,
            "quantity": random.randint(1, 3),
        })


orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

orders_df.to_parquet(
    "data/incoming/orders_incremental_01.parquet",
    index=False
)

order_items_df.to_parquet(
    "data/incoming/order_items_incremental_01.parquet",
    index=False
)

print(f"Generated {len(orders_df):,} new orders.")
print(f"Generated {len(order_items_df):,} new order items.")
print(
    f"Order IDs: {orders_df['order_id'].min():,} "
    f"- {orders_df['order_id'].max():,}"
)
print(
    f"Dates: {orders_df['order_timestamp'].min()} "
    f"- {orders_df['order_timestamp'].max()}"
)