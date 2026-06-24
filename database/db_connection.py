from sqlalchemy import create_engine
from urllib.parse import quote_plus
DB_USER = "postgres"
DB_PASSWORD = quote_plus("pass@12345six")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "paymentDB"

try:
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    conn = engine.connect()

    print("Database Connected Successfully!")

    conn.close()

except Exception as e:
    print("Connection Failed")
    print(e)