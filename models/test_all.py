import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier


# LOAD DATA
# -------------------------

df = pd.read_csv(
    "data/raw_data/paysim.csv",
    nrows=100000
)


# FEATURE ENGINEERING
# -------------------------

encoder = LabelEncoder()

df["type_encoded"] = encoder.fit_transform(
    df["type"]
)

df["balance_diff_org"] = (
    df["oldbalanceOrg"]
    - df["newbalanceOrig"]
)

df["balance_diff_dest"] = (
    df["newbalanceDest"]
    - df["oldbalanceDest"]
)


# FEATURES
# -------------------------

X = df[
    [
        "type_encoded",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "balance_diff_org",
        "balance_diff_dest"
    ]
]

y = df["isFraud"]


# TRAIN TEST SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Rows:", len(X_train))
print("Testing Rows:", len(X_test))


# SMOTE
# -------------------------

print("\nApplying SMOTE...")

smote = SMOTE(
    random_state=42
)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("Before SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(y_train_smote.value_counts())


# RANDOM FOREST
# -------------------------

print("\nTraining Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(
    X_train_smote,
    y_train_smote
)

rf_predictions = rf_model.predict(X_test)

print("\nRandom Forest Report")

print(
    classification_report(
        y_test,
        rf_predictions
    )
)

print("\nRandom Forest Confusion Matrix")

print(
    confusion_matrix(
        y_test,
        rf_predictions
    )
)


# SAVE RF MODEL
# -------------------------

joblib.dump(
    rf_model,
    "models/random_forest_fraud.pkl"
)

print(
    "\nRandom Forest Model Saved"
)


# XGBOOST
# -------------------------

print("\nTraining XGBoost...")

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric="logloss"
)

xgb_model.fit(
    X_train_smote,
    y_train_smote
)

xgb_predictions = xgb_model.predict(
    X_test
)

print("\nXGBoost Report")

print(
    classification_report(
        y_test,
        xgb_predictions
    )
)

print("\nXGBoost Confusion Matrix")

print(
    confusion_matrix(
        y_test,
        xgb_predictions
    )
)


# SAVE XGBOOST MODEL
# -------------------------

joblib.dump(
    xgb_model,
    "models/xgboost_fraud.pkl"
)

print(
    "\nXGBoost Model Saved"
)


