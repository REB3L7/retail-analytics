import random
import pandas as pd
from faker import Faker


fake = Faker()

Faker.seed(42)
random.seed(42)


NUM_PRODUCTS = 10_000


categories = [
    "Electronics",
    "Home",
    "Clothing",
    "Beauty",
    "Sports",
    "Toys",
    "Grocery",
]


products = []


for product_id in range(1, NUM_PRODUCTS + 1):

    category = random.choice(categories)

    products.append({
        "product_id": product_id,
        "product_name": f"{category} Product {product_id}",
        "category": category,
        "price": round(random.uniform(2.99, 999.99), 2),
    })


products_df = pd.DataFrame(products)


products_df.to_parquet(
    "data/raw/products.parquet",
    index=False
)


print(f"Generated {len(products_df):,} products.")
print(products_df.head())

# -------------------------
# Generate Stores
# -------------------------

NUM_STORES = 2_000

states = [
    "FL", "TX", "CA", "NY", "GA",
    "NC", "IL", "PA", "OH", "AZ",
    "VA", "TN", "MI", "NJ", "WA"
]

stores = []

for store_id in range(1, NUM_STORES + 1):

    stores.append({
        "store_id": store_id,
        "store_name": f"Store {store_id}",
        "state": random.choice(states),
        "city": fake.city(),
        "opened_date": fake.date_between(
            start_date="-20y",
            end_date="-1y"
        )
    })


stores_df = pd.DataFrame(stores)

stores_df.to_parquet(
    "data/raw/stores.parquet",
    index=False
)

print(f"\nGenerated {len(stores_df):,} stores.")
print(stores_df.head())

# -------------------------
# Generate Customers
# -------------------------

NUM_CUSTOMERS = 100_000

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": f"customer{customer_id}@example.com",
        "state": random.choice(states),
        "loyalty_member": random.choice([True, False]),
        "signup_date": fake.date_between(
            start_date="-8y",
            end_date="today"
        )
    })


customers_df = pd.DataFrame(customers)

customers_df.to_parquet(
    "data/raw/customers.parquet",
    index=False
)

print(f"\nGenerated {len(customers_df):,} customers.")
print(customers_df.head())