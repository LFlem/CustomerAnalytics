import pandas as pd

df = pd.read_csv("data/processed/clean_telco.csv")

churn_rate = df["Churn"].mean()
print("Churn rate:", churn_rate)

print(df.groupby("Contract")["Churn"].mean())