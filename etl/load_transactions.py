import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Database Connection
DB_USER = "postgres"
DB_PASSWORD = quote_plus("pass@12345six")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "paymentDB"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Loading dataset...")

# Load first 10,000 rows
df = pd.read_csv(
    "data/raw_data/paysim.csv",
    nrows=10000
)

print(f"Rows Loaded: {len(df)}")

# Rename columns
df = df.rename(columns={
    "step": "transaction_time",
    "type": "transaction_type",
    "nameOrig": "customer_id",
    "nameDest": "merchant_id",
    "oldbalanceOrg": "old_balance_org",
    "newbalanceOrig": "new_balance_org",
    "oldbalanceDest": "old_balance_dest",
    "newbalanceDest": "new_balance_dest",
    "isFraud": "is_fraud",
    "isFlaggedFraud": "is_flagged_fraud"
})

# Select required columns
df = df[
    [
        "customer_id",
        "merchant_id",
        "transaction_type",
        "amount",
        "old_balance_org",
        "new_balance_org",
        "old_balance_dest",
        "new_balance_dest",
        "is_fraud",
        "is_flagged_fraud",
        "transaction_time"
    ]
]

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nLoading data into PostgreSQL")

df.to_sql(
    "transactions",
    engine,
    if_exists="append",
    index=False
)
print("Data loaded successfully")
