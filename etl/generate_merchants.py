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

print("Reading merchant data...")

df = pd.read_sql(
    "SELECT DISTINCT merchant_id FROM transactions",
    engine
)

print("Unique Merchants:", len(df))

categories = [
    "Ecommerce",
    "Retail",
    "Travel",
    "Food",
    "Healthcare",
    "Entertainment"
]

risk_levels = [
    "Low",
    "Medium",
    "High"
]

merchants = []

for merchant_id in df["merchant_id"]:

    merchants.append({
        "merchant_id": merchant_id,
        "merchant_name": fake.company(),
        "merchant_category": random.choice(categories),
        "city": fake.city(),
        "risk_level": random.choice(risk_levels)
    })

merchant_df = pd.DataFrame(merchants)

print(merchant_df.head())

#loading data into PostgreSQL

merchant_df.to_sql(
    "merchants",
    engine,
    if_exists="append",
    index=False
)
print("merchants loaded succcesfully")
