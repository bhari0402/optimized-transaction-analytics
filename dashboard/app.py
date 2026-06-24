import dash
from dash import dcc
import plotly.express as px
import pandas as pd
from dash import html
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dash import Input, Output, State
import requests  


# PostgreSQL Connection

DB_USER = "postgres"
DB_PASSWORD = quote_plus("pass@12345six")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "paymentDB"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Read KPIs

with engine.connect() as conn:

    total_transactions = conn.execute(
        text("SELECT COUNT(*) FROM transactions")
    ).scalar()

    fraud_rate = conn.execute(
        text("""
        SELECT ROUND(
            (
                COUNT(*) FILTER (WHERE is_fraud = 1)::numeric
                /
                COUNT(*)
            ) * 100,
            4
        )
        FROM transactions
        """)
    ).scalar()

    transaction_df = pd.read_sql(
    """
    SELECT
        transaction_type,
        COUNT(*) AS total_transactions
    FROM transactions
    GROUP BY transaction_type
    ORDER BY total_transactions DESC
    """,
    engine
)
    transaction_chart = px.bar(
    transaction_df,
    x="transaction_type",
    y="total_transactions",
    title="Transaction Type Distribution"
)
    top_merchants_df = pd.read_sql(
    """
    SELECT
        merchant_id,
        ROUND(SUM(amount)::numeric,2) AS revenue
    FROM transactions
    GROUP BY merchant_id
    ORDER BY revenue DESC
    LIMIT 10
    """,
    engine
)
    top_merchants_chart = px.bar(
    top_merchants_df,
    x="merchant_id",
    y="revenue",
    title="Top 10 Merchants by Revenue"
)
    settlement_df = pd.read_sql(
    """
    SELECT
        settlement_status,
        COUNT(*) AS total_settlements
    FROM settlements
    GROUP BY settlement_status
    """,
    engine
)
    settlement_chart = px.pie(
    settlement_df,
    names="settlement_status",
    values="total_settlements",
    title="Settlement Status Distribution"
)
    total_revenue = conn.execute(
    text("""
    SELECT ROUND(SUM(amount)::numeric,2)
    FROM transactions
    """)
)   .scalar()

    total_customers = conn.execute(
    text("""
    SELECT COUNT(*)
    FROM customers
    """)
)   .scalar()

    total_merchants = conn.execute(
    text("""
    SELECT COUNT(*)
    FROM merchants
    """)
).scalar()

# Dash App

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1(
        "Optimized Transaction Analytics Dashboard"
    ),

    
# basic ------------------> replacing it to enhanced version
    #html.Div([

    # html.H3(f"Transactions: {total_transactions}"),

    # html.H3(f"Revenue: ₹{total_revenue}"),

    # html.H3(f"Customers: {total_customers}"),

    # html.H3(f"Merchants: {total_merchants}"),

    # html.H3( f"Fraud Rate: {fraud_rate}%"),

    # advance version----------------------------
html.Div([

    html.Div([
        html.H4("Transactions"),
        html.H2(f"{total_transactions}")
    ], style={
        "border":"1px solid lightgray",
        "padding":"20px",
        "margin":"10px",
        "display":"inline-block",
        "width":"18%"
    }),

    html.Div([
        html.H4("Revenue"),
        html.H2(f"₹{total_revenue}")
    ], style={
        "border":"1px solid lightgray",
        "padding":"20px",
        "margin":"10px",
        "display":"inline-block",
        "width":"18%"
    }),

    html.Div([
        html.H4("Customers"),
        html.H2(f"{total_customers}")
    ], style={
        "border":"1px solid lightgray",
        "padding":"20px",
        "margin":"10px",
        "display":"inline-block",
        "width":"18%"
    }),

    html.Div([
        html.H4("Merchants"),
        html.H2(f"{total_merchants}")
    ], style={
        "border":"1px solid lightgray",
        "padding":"20px",
        "margin":"10px",
        "display":"inline-block",
        "width":"18%"
    }),

    html.Div([
        html.H4("Fraud Rate"),
        html.H2(f"{fraud_rate}%")
    ], style={
        "border":"1px solid lightgray",
        "padding":"20px",
        "margin":"10px",
        "display":"inline-block",
        "width":"18%"
    })

]),        
    dcc.Graph(
        figure=transaction_chart
    ),
    
    dcc.Graph(
    figure=top_merchants_chart
    ),
    
    dcc.Graph(
    figure=settlement_chart
    ),

#adding input /// used Genai for this 
    html.Hr(),

    html.H2("Fraud Prediction Simulator"),

    dcc.Dropdown(
    id="transaction_type",
    options=[
        {"label": "TRANSFER", "value": "TRANSFER"},
        {"label": "CASH_OUT", "value": "CASH_OUT"},
        {"label": "PAYMENT", "value": "PAYMENT"},
        {"label": "CASH_IN", "value": "CASH_IN"},
        {"label": "DEBIT", "value": "DEBIT"}
    ],
    value="TRANSFER"
    ),

    dcc.Input(
    id="amount",
    type="number",
    placeholder="Amount"
    ),

    dcc.Input(
    id="oldbalanceOrg",
    type="number",
    placeholder="Old Balance Org"
    ),

    dcc.Input(
    id="newbalanceOrig",
    type="number",
    placeholder="New Balance Org"
    ),

    dcc.Input(
    id="oldbalanceDest",
    type="number",
    placeholder="Old Balance Dest"
    ),

    dcc.Input(
    id="newbalanceDest",
    type="number",
    placeholder="New Balance Dest"
    ),

    html.Br(),
    html.Br(),

    html.Button(
    "Predict Fraud",
    id="predict_button"
    ),

    html.Br(),
    html.Br(),

    html.Div(id="prediction_result")
])
 

# #adding callback  ///

@app.callback(
    Output(
        "prediction_result",
        "children"
    ),
    Input(
        "predict_button",
        "n_clicks"
    ),
    State(
        "transaction_type",
        "value"
    ),
    State(
        "amount",
        "value"
    ),
    State(
        "oldbalanceOrg",
        "value"
    ),
    State(
        "newbalanceOrig",
        "value"
    ),
    State(
        "oldbalanceDest",
        "value"
    ),
    State(
        "newbalanceDest",
        "value"
    )
)
def predict_dashboard(
    n_clicks,
    transaction_type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
):

    if not n_clicks:
        return ""

    response = requests.post(
        "http://127.0.0.1:8000/predict-fraud",
        json={
            "transaction_type": transaction_type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest
        }
    )

    result = response.json()

    return html.Div([

        html.H3(
            f"Prediction: {result['prediction']}"
        ),

        html.H3(
            f"Fraud Probability: {result['fraud_probability']}"
        ),

        html.H3(
            f"Risk Level: {result['risk_level']}"
        )

    ])

if __name__ == "__main__":
    app.run(debug=True)
