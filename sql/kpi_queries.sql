-- KPI 1: Total Transactions

SELECT
COUNT(*) AS total_transactions
FROM transactions;
--10000--
----------------------------------------------

-- KPI 2: Total Transaction Amount

SELECT
ROUND(SUM(amount)::numeric,2) AS total_transaction_amount
FROM transactions;

--1035466899.49--
-------------------------------------------------

-- KPI 3: Fraud Transactions

SELECT
COUNT(*) AS fraud_transactions
FROM transactions
WHERE is_fraud = 1;

--68--
--------------------------------------------------

-- KPI 4: Fraud Rate

SELECT
ROUND(
(
COUNT(*) FILTER (WHERE is_fraud = 1)::numeric
/
COUNT(*)
) * 100,
4
) AS fraud_rate_percentage
FROM transactions;

-- 0.6800 --
--------------------------------------------

-- KPI 5: Transaction Type Distribution

SELECT
transaction_type,
COUNT(*) AS total_transactions
FROM transactions
GROUP BY transaction_type
ORDER BY total_transactions DESC;

--"PAYMENT"	5465
--"CASH_IN"	1949
--"CASH_OUT"	1321
--"TRANSFER"	921
--"DEBIT"	344
---------------------------------------------

-- KPI 6: Top 10 Merchants by Revenue

SELECT
merchant_id,
ROUND(SUM(amount)::numeric,2) AS revenue
FROM transactions
GROUP BY merchant_id
ORDER BY revenue DESC
LIMIT 10;

--"C1590550415"	29579451.08
--"C985934102"	18888987.93
--"C1286084959"	17981492.66
--"C1883840933"	17361451.11
--"C766681183"	16818661.43
--"C665576141"	16393352.81
--"C1789550256"	16219263.01
--"C451111351"	16118094.39
--"C97730845"	14418568.98
--"C1262822392"	13842476.03
-----------------------------------------------------

-- KPI 7: Settlement Status

SELECT
settlement_status,
COUNT(*) AS total_settlements
FROM settlements
GROUP BY settlement_status;

--"Pending"	3132
--"Completed"	3265