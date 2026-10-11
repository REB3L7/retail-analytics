import random
from datetime import datetime, timedelta

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

random.seed(42)

NUM_ORDERS = 1_000_000
BATCH_SIZE = 100_000

NUM_CUSTOMERS = 100_000
NUM_STORES = 2_000
NUM_PRODUCTS = 10_000

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 9, 30)

DATE_RANGE = (END_DATE - START_DATE).days


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def random_date():
    """
    Generate a random timestamp between
    January 1, 2024 and September 30, 2026.
    """

    return START_DATE + timedelta(
        days=random.randint(0, DATE_RANGE),
        seconds=random.randint(0, 86399)
    )


# --------------------------------------------------
# Generate Orders and Order Items
# --------------------------------------------------

for batch_start in range(0, NUM_ORDERS, BATCH_SIZE):

    batch_end = min(
        batch_start + BATCH_SIZE,
        NUM_ORDERS
    )

    orders = []
    order_items = []

    # Generate 100,000 orders per batch
    for order_id in range(batch_start + 1, batch_end + 1):

        # Approximately 70% of orders occur in stores
        # and 30% occur online.
        sales_channel = random.choices(
            ["STORE", "ONLINE"],
            weights=[70, 30],
            k=1
        )[0]

        # Store purchases receive a store ID.
        # Online purchases do not belong to a physical store.
        store_id = (
            random.randint(1, NUM_STORES)
            if sales_channel == "STORE"
            else None
        )

        # Create the order.
        orders.append({
            "order_id": order_id,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "store_id": store_id,
            "sales_channel": sales_channel,
            "order_timestamp": random_date(),
        })

        # --------------------------------------------------
        # Generate Order Items
        # --------------------------------------------------

        # Each order contains between 1 and 5 products.
        num_items = random.randint(1, 5)

        # Select different products for this order.
        selected_products = random.sample(
            range(1, NUM_PRODUCTS + 1),
            num_items
        )

        for product_id in selected_products:

            # Each selected product has a quantity of 1-3.
            order_items.append({
                "order_id": order_id,
                "product_id": product_id,
                "quantity": random.randint(1, 3),
            })

    # --------------------------------------------------
    # Convert Batch to DataFrames
    # --------------------------------------------------

    orders_df = pd.DataFrame(orders)
    order_items_df = pd.DataFrame(order_items)

    # Determine which batch/file we're currently processing.
    file_number = (batch_start // BATCH_SIZE) + 1

    # --------------------------------------------------
    # Save Orders
    # --------------------------------------------------

    orders_file = (
        f"data/raw/orders_part_{file_number:02d}.parquet"
    )

    orders_df.to_parquet(
        orders_file,
        index=False
    )

    # --------------------------------------------------
    # Save Order Items
    # --------------------------------------------------

    order_items_file = (
        f"data/raw/order_items_part_{file_number:02d}.parquet"
    )

    order_items_df.to_parquet(
        order_items_file,
        index=False
    )

    # Show progress after every batch.
    print(
        f"Generated orders {batch_start + 1:,} - {batch_end:,} "
        f"with {len(order_items_df):,} order items"
    )


print("\nFinished generating 1,000,000 orders and their order items.")