def generate_insights(churn_rate):
    if churn_rate > 0.25:
        return "⚠️ Churn élevé — cibler contrats mensuels"
    return "Churn sous contrôle"

print(generate_insights(0.27))