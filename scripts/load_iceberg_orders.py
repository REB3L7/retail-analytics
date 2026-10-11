from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from pyiceberg.catalog.sql import SqlCatalog


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CATALOG_PATH = PROJECT_ROOT / "data" / "iceberg" / "catalog.db"
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "iceberg" / "warehouse"
RAW_PATH = PROJECT_ROOT / "data" / "raw"


catalog = SqlCatalog(
    "retail",
    uri=f"sqlite:///{CATALOG_PATH}",
    warehouse=f"file://{WAREHOUSE_PATH}",
)

orders_table = catalog.load_table("retail.orders")


order_files = sorted(
    RAW_PATH.glob("orders_part_*.parquet")
)

print(f"Found {len(order_files)} historical order files.")


tables = []

for file_path in order_files:
    table = pq.read_table(file_path)

    # Normalize store_id from DOUBLE to nullable INT64.
    store_id = table["store_id"].cast(pa.int64())

    table = table.set_column(
        table.schema.get_field_index("store_id"),
        "store_id",
        store_id,
    )

    tables.append(table)

historical_orders = pa.concat_tables(tables)

target_schema = pa.schema([
    pa.field("order_id", pa.int64(), nullable=False),
    pa.field("customer_id", pa.int64(), nullable=False),
    pa.field("store_id", pa.int64(), nullable=True),
    pa.field("sales_channel", pa.string(), nullable=False),
    pa.field("order_timestamp", pa.timestamp("us"), nullable=False),
])

historical_orders = historical_orders.cast(target_schema)

print(f"Historical rows loaded: {historical_orders.num_rows:,}")


orders_table.append(historical_orders)

print("\nHistorical orders appended to Iceberg.")