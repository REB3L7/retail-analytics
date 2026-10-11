from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from pyiceberg.catalog.sql import SqlCatalog


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CATALOG_PATH = PROJECT_ROOT / "data" / "iceberg" / "catalog.db"
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "iceberg" / "warehouse"
INCOMING_PATH = (
    PROJECT_ROOT
    / "data"
    / "incoming"
    / "orders_incremental_01.parquet"
)


catalog = SqlCatalog(
    "retail",
    uri=f"sqlite:///{CATALOG_PATH}",
    warehouse=f"file://{WAREHOUSE_PATH}",
)

orders_table = catalog.load_table("retail.orders")


incoming_orders = pq.read_table(INCOMING_PATH)

target_schema = pa.schema([
    pa.field("order_id", pa.int64(), nullable=False),
    pa.field("customer_id", pa.int64(), nullable=False),
    pa.field("store_id", pa.int64(), nullable=True),
    pa.field("sales_channel", pa.string(), nullable=False),
    pa.field("order_timestamp", pa.timestamp("us"), nullable=False),
])

incoming_orders = incoming_orders.cast(target_schema)


print(f"Incoming rows: {incoming_orders.num_rows:,}")

print(
    "Order ID range:",
    incoming_orders["order_id"][0].as_py(),
    "→",
    incoming_orders["order_id"][-1].as_py(),
)


orders_table.append(incoming_orders)

print("Incoming orders appended to Iceberg.")