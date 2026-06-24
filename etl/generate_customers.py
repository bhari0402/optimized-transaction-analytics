import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine
from urllib.parse import quote_plus

fake = Faker("en_IN")

# Database Connection
DB_USER = "postgres"
DB_PASSWORD = quote_plus("pass@12345six")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "paymentDB"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Reading transaction data...")

df = pd.read_sql(
    "SELECT DISTINCT customer_id FROM transactions",
    engine
)

print("Unique Customers:", len(df))

customers = []

segments = [
    "Standard",
    "Premium",
    "Gold"
]

for customer_id in df["customer_id"]:

    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "age": random.randint(18, 70),
        "city": fake.city(),
        "customer_segment": random.choice(segments),
        "risk_score": round(random.uniform(1, 100), 2)
    })

customer_df = pd.DataFrame(customers)

print(customer_df.head())

# Adding it in pgAdmin PostgreSQL

customer_df.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

print("Customers loaded successfully!")