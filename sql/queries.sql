-- Churn global
SELECT AVG(Churn) as churn_rate FROM customers;

-- Churn par contrat
SELECT Contract, AVG(Churn)
FROM customers
GROUP BY Contract;

-- Revenu moyen
SELECT AVG(MonthlyCharges) FROM customers;