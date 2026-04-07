# CustomerAnalytics


## 🎯 Objectif
Analyser le churn client et proposer des recommandations produit

## Lien du Dataset trouvé sur KAGGLE
https://www.kaggle.com/datasets/blastchar/telco-customer-churn?resource=download

## Variables clés :
Churn → cible (le plus important)
tenure → durée client
MonthlyCharges → revenu
Contract → type d’abonnement
InternetService → usage
PaymentMethod → comportement paiement

## 📊 Dataset
Telco Customer Churn Dataset

## 🧠 Problème
Pourquoi les clients quittent le service ?

## 🚀 Solution
- Analyse Python
- SQL
- Dashboard Power BI

## 📈 KPIs
- Churn rate
- Revenue
- Engagement

## 🔍 Insights
- Churn élevé sur contrats mensuels

## 🛠 Stack
Python, SQL, Power BI, Streamlit

## ▶️ Lancer le dashboard local
1. Générer les données nettoyées :
python notebooks/scripts/data_cleaning.py

2. Démarrer le dashboard Streamlit :
streamlit run dashboard/app.py