from fastapi import FastAPI
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from api.predict_api import predict_fraud
from api.security.auth import create_access_token
from pydantic import BaseModel
#
from fastapi import Header, HTTPException
from api.security.auth import verify_token


app = FastAPI(
    title="Optimized Transaction Analytics API",
    version="1.0"
)

DB_USER = "postgres"
DB_PASSWORD = quote_plus("pass@12345six")
# DB_HOST = "localhost"       # changed it due to docker it reads as api container
DB_HOST = "host.docker.internal"
DB_PORT = "5432"
DB_NAME = "paymentDB"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

#authantication function
def authorize_user(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token Missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return payload

@app.get("/")
def home():
    return {
        "message": "API Running Successfully"
    }

#for total transactions kpi
@app.get("/api/kpi/transactions")
def total_transactions():

    query = """
    SELECT COUNT(*) AS total_transactions
    FROM transactions
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        count = result.scalar()

    return {
        "total_transactions": count
    }

#for fraud rate kpi
@app.get("/api/kpi/fraud-rate")
def fraud_rate():

    query = """
    SELECT
    ROUND(
    (
    COUNT(*) FILTER (WHERE is_fraud = 1)::numeric
    /
    COUNT(*)
    ) * 100,
    4
    ) AS fraud_rate
    FROM transactions
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rate = result.scalar()

    return {
        "fraud_rate_percentage": float(rate)
    }

#for top_merchants kpi
@app.get("/api/kpi/top-merchants")
def top_merchants():

    query = """
    SELECT
        merchant_id,
        ROUND(SUM(amount)::numeric,2) AS revenue
    FROM transactions
    GROUP BY merchant_id
    ORDER BY revenue DESC
    LIMIT 10
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))

        merchants = []

        for row in result:
            merchants.append({
                "merchant_id": row[0],
                "revenue": float(row[1])
            })

    return merchants

# for settlement status
@app.get("/api/kpi/settlements")
def settlement_status():

    query = """
    SELECT
        settlement_status,
        COUNT(*) AS total
    FROM settlements
    GROUP BY settlement_status
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))

        data = []

        for row in result:
            data.append({
                "settlement_status": row[0],
                "count": row[1]
            })

    return data

class FraudRequest(BaseModel):
    transaction_type: str
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float


@app.post("/predict-fraud")
def fraud_prediction(data: FraudRequest):

    result = predict_fraud(
        transaction_type=data.transaction_type,
        amount=data.amount,
        oldbalanceOrg=data.oldbalanceOrg,
        newbalanceOrig=data.newbalanceOrig,
        oldbalanceDest=data.oldbalanceDest,
        newbalanceDest=data.newbalanceDest
    )

    return result

#another test module for authantication
# @app.post("/predict-fraud")
# def fraud_prediction(
#     data: FraudRequest,
#     authorization: str = Header(None)
# ):

#     authorize_user(
#         authorization
#     )

#     result = predict_fraud(
#         transaction_type=data.transaction_type,
#         amount=data.amount,
#         oldbalanceOrg=data.oldbalanceOrg,
#         newbalanceOrig=data.newbalanceOrig,
#         oldbalanceDest=data.oldbalanceDest,
#         newbalanceDest=data.newbalanceDest
#     )

#     return result

# adding login request model

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: LoginRequest):

    if (
        user.username == "admin"
        and
        user.password == "admin123"
    ):

        token = create_access_token(
            {"sub": user.username}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    return {
        "message": "Invalid Credentials"
    }

