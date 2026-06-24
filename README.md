# Optimized Transaction Analytics & Fraud Detection Platform

## Overview

The Optimized Transaction Analytics & Fraud Detection Platform is an end-to-end financial analytics solution built using FastAPI, PostgreSQL, Machine Learning, and Docker.

The platform provides:

* Transaction Analytics APIs
* Fraud Detection using XGBoost
* KPI Monitoring
* Settlement Analytics
* Merchant Revenue Analytics
* JWT Authentication
* Dockerized Deployment

This project demonstrates skills in Data Engineering, Backend Development, Machine Learning, and DevOps.

---

## Tech Stack

### Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL

### Machine Learning

* XGBoost
* Scikit-Learn
* Joblib

### Data Processing

* Pandas
* NumPy

### Authentication

* JWT (JSON Web Tokens)

### Visualization

* Dash
* Plotly

### DevOps

* Docker
* Docker Compose

---

## Project Architecture

Transaction Dataset
        │
        ▼
     ETL Pipeline
        │
        ▼
   PostgreSQL Database
        │
        ▼
     FastAPI Backend
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
KPIs  Fraud API Dashboard
```

---

## Features

### Transaction Analytics

* Total Transactions KPI
* Fraud Rate KPI
* Merchant Revenue Analytics
* Settlement Status Analytics

### Fraud Detection

Machine Learning fraud detection service using XGBoost.

Input:

* Transaction Type
* Amount
* Account Balances

Output:

* Fraud Prediction
* Risk Classification

### Authentication

JWT-based authentication system:

* Login Endpoint
* Token Generation
* Token Validation

### Docker Support

The entire application stack is containerized using Docker Compose.

Services:

* FastAPI API
* PostgreSQL Database

---

## API Endpoints

### Health Check

```http
GET /
```

### Total Transactions KPI

```http
GET /api/kpi/transactions
```

### Fraud Rate KPI

```http
GET /api/kpi/fraud-rate
```

### Top Merchants

```http
GET /api/kpi/top-merchants
```

### Settlement Analytics

```http
GET /api/kpi/settlements
```

### Fraud Prediction

```http
POST /predict-fraud
```

### Login

```http
POST /login
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/bhari0402/optimized-transaction-analytics.git
cd optimized-transaction-analytics
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=paymentDB

SECRET_KEY=your_secret_key
```

### Run Application

```bash
uvicorn api.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Docker Setup

Build and start containers:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker ps
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Machine Learning Model

Model: XGBoost Classifier

Purpose:

* Detect fraudulent financial transactions
* Provide fraud prediction through REST APIs

Model artifacts:

* xgboost_fraud.pkl
* random_forest_fraud.pkl

---

## Future Enhancements

* CI/CD Pipeline
* Cloud Deployment (AWS/Azure/GCP)
* Real-Time Fraud Detection
* Kafka Streaming Integration
* Role-Based Access Control
* Monitoring & Logging

---

GitHub:
https://github.com/bhari0402
