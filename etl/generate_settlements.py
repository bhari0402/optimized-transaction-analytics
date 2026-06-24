import pandas as pd
import random
from datetime import date, timedelta
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

print("Reading merchant transactions...")

query = """
SELECT
merchant_id,
SUM(amount) AS settlement_amount
FROM transactions
GROUP BY merchant_id
"""

df = pd.read_sql(query, engine)

print("Merchants Found:", len(df))

settlements = []

for index, row in df.iterrows():

    settlements.append({
        "settlement_id": f"S{index+1:05}",
        "merchant_id": row["merchant_id"],
        "settlement_amount": round(row["settlement_amount"], 2),
        "settlement_date": date.today() - timedelta(days=random.randint(0, 30)),
        "settlement_status": random.choice(
            ["Completed", "Pending"]
        )
    })

settlement_df = pd.DataFrame(settlements)

print(settlement_df.head())

#loading to Postgresql

settlement_df.to_sql(
    "settlements",
    engine,
    if_exists="append",
    index=False
)
print("settlements loaded succesfully")
