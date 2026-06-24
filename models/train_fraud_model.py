import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


#loading dataset

df = pd.read_csv(
    "data/raw_data/paysim.csv",
    nrows=500000
)

# print("Shape:")
# print(df.shape)

# print("\nDuplicate Rows:")
# print(df.duplicated().sum())

# print("\nMissing Values:")
# print(df.isnull().sum())

# print("\nData Types:")
# print(df.dtypes)

# print("\nFraud Distribution:")
# print(df["isFraud"].value_counts())


# Encoding transaction type

encoder = LabelEncoder()
df["type_encoded"] = encoder.fit_transform(
    df["type"]
)

# Features

x= df[
    [
        "type_encoded",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest"
    ]
]

# Target

y = df["isFraud"]

# print("Feature Shape:")
# print(x.shape)

# print("\nTarget Shape:")
# print(y.shape)

# print("\nTransaction Type Mapping:")

# for original, encoded in zip(
#     encoder.classes_,
#     range(len(encoder.classes_))
# ):
#     print(original, "=", encoded)

# train/test split------------------------------------------------

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Rows:", len(x_train))
print("Testing Rows:", len(x_test))

# Model training-----------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Improvement because dataset is imbalance

# model = RandomForestClassifier(
#     n_estimators=200,
#     class_weight="balanced",
#     random_state=42
# )

print("\nTraining model...")

model.fit(x_train, y_train)

print("Model training completed")

# Predictions

y_pred = model.predict(x_test)

#Model evaluation----------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)
