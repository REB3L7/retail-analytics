from pathlib import Path

from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField,
    LongType,
    StringType,
    TimestampType,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CATALOG_PATH = PROJECT_ROOT / "data" / "iceberg" / "catalog.db"
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "iceberg" / "warehouse"


catalog = SqlCatalog(
    "retail",
    uri=f"sqlite:///{CATALOG_PATH}",
    warehouse=f"file://{WAREHOUSE_PATH}",
)


namespace = "retail"

existing_namespaces = catalog.list_namespaces()

if (namespace,) not in existing_namespaces:
    catalog.create_namespace(namespace)
    print(f"Created namespace: {namespace}")
else:
    print(f"Namespace already exists: {namespace}")


print("Namespaces:", catalog.list_namespaces())

orders_schema = Schema(
    NestedField(
        field_id=1,
        name="order_id",
        field_type=LongType(),
        required=True,
    ),
    NestedField(
        field_id=2,
        name="customer_id",
        field_type=LongType(),
        required=True,
    ),
    NestedField(
        field_id=3,
        name="store_id",
        field_type=LongType(),
        required=False,
    ),
    NestedField(
        field_id=4,
        name="sales_channel",
        field_type=StringType(),
        required=True,
    ),
    NestedField(
        field_id=5,
        name="order_timestamp",
        field_type=TimestampType(),
        required=True,
    ),
)

print("\nOrders Iceberg schema:")
print(orders_schema)

table_name = "retail.orders"

existing_tables = catalog.list_tables("retail")

if ("retail", "orders") not in existing_tables:
    orders_table = catalog.create_table(
        identifier=table_name,
        schema=orders_schema,
    )
    print(f"\nCreated Iceberg table: {table_name}")
else:
    orders_table = catalog.load_table(table_name)
    print(f"\nIceberg table already exists: {table_name}")

print("Tables:", catalog.list_tables("retail"))
print("Table location:", orders_table.location())