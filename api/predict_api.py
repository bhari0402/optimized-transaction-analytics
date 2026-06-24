import joblib
import pandas as pd

model = joblib.load(
    "models/xgboost_fraud.pkl"
)

def predict_fraud(
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
):

    type_mapping = {
        "CASH_IN": 0,
        "CASH_OUT": 1,
        "DEBIT": 2,
        "PAYMENT": 3,
        "TRANSFER": 4
    }

    type_encoded = type_mapping[
        transaction_type
    ]

    balance_diff_org = (
        oldbalanceOrg
        - newbalanceOrig
    )

    balance_diff_dest = (
        newbalanceDest
        - oldbalanceDest
    )

    features = pd.DataFrame(
        [[
            type_encoded,
            amount,
            oldbalanceOrg,
            newbalanceOrig,
            oldbalanceDest,
            newbalanceDest,
            balance_diff_org,
            balance_diff_dest
        ]],
        columns=[
            "type_encoded",
            "amount",
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
            "balance_diff_org",
            "balance_diff_dest"
        ]
    )

    prediction = model.predict(features)[0]

    probability = model.predict_proba(
        features
    )[0][1]

    if probability >= 0.80:
        risk_level = "HIGH"
    elif probability >= 0.50:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "prediction": int(prediction),
        "fraud_probability": round(float(probability), 4),
        "risk_level": risk_level
    }
