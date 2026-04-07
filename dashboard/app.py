from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Customer Analytics Dashboard", page_icon="📊", layout="wide")

DATA_PATH = Path("data/processed/clean_telco.csv")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if df["Churn"].dtype == object:
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtres")

    contracts = st.sidebar.multiselect(
        "Contract", sorted(df["Contract"].dropna().unique().tolist())
    )
    internet_services = st.sidebar.multiselect(
        "InternetService", sorted(df["InternetService"].dropna().unique().tolist())
    )
    payment_methods = st.sidebar.multiselect(
        "PaymentMethod", sorted(df["PaymentMethod"].dropna().unique().tolist())
    )

    tenure_min, tenure_max = int(df["tenure"].min()), int(df["tenure"].max())
    tenure_range = st.sidebar.slider(
        "Tenure (mois)", min_value=tenure_min, max_value=tenure_max, value=(tenure_min, tenure_max)
    )

    filtered = df.copy()

    if contracts:
        filtered = filtered[filtered["Contract"].isin(contracts)]
    if internet_services:
        filtered = filtered[filtered["InternetService"].isin(internet_services)]
    if payment_methods:
        filtered = filtered[filtered["PaymentMethod"].isin(payment_methods)]

    filtered = filtered[
        (filtered["tenure"] >= tenure_range[0]) & (filtered["tenure"] <= tenure_range[1])
    ]

    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    total_customers = len(df)
    churn_rate = df["Churn"].mean()
    monthly_revenue = df["MonthlyCharges"].sum()
    avg_tenure = df["tenure"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clients", f"{total_customers:,}")
    c2.metric("Churn rate", f"{churn_rate:.1%}")
    c3.metric("Revenue mensuel (proxy)", f"${monthly_revenue:,.0f}")
    c4.metric("Tenure moyen", f"{avg_tenure:.1f} mois")


def render_charts(df: pd.DataFrame) -> None:
    st.subheader("Analyse churn")

    left, right = st.columns(2)

    with left:
        churn_by_contract = (
            df.groupby("Contract", as_index=False)["Churn"].mean().sort_values("Churn", ascending=False)
        )
        st.markdown("Churn par type de contrat")
        st.bar_chart(churn_by_contract, x="Contract", y="Churn")

    with right:
        churn_by_payment = (
            df.groupby("PaymentMethod", as_index=False)["Churn"]
            .mean()
            .sort_values("Churn", ascending=False)
        )
        st.markdown("Churn par mode de paiement")
        st.bar_chart(churn_by_payment, x="PaymentMethod", y="Churn")

    st.markdown("Distribution de tenure selon churn")
    tenure_churn = (
        df.groupby(["tenure", "Churn"], as_index=False)
        .size()
        .pivot(index="tenure", columns="Churn", values="size")
        .fillna(0)
    )
    tenure_churn.columns = ["No Churn", "Churn"] if len(tenure_churn.columns) == 2 else tenure_churn.columns
    st.line_chart(tenure_churn)


def render_actionable_insights(df: pd.DataFrame) -> None:
    st.subheader("Insights actionnables")

    churn_rate = df["Churn"].mean()
    month_to_month_rate = df[df["Contract"] == "Month-to-month"]["Churn"].mean()

    if churn_rate > 0.25:
        st.warning("Churn global élevé: prioriser un plan de rétention.")
    else:
        st.success("Churn global sous contrôle.")

    if pd.notna(month_to_month_rate) and month_to_month_rate > 0.35:
        st.error(
            f"Contrats Month-to-month à risque ({month_to_month_rate:.1%}). "
            "Action: migration vers engagements 12/24 mois + incentives."
        )

    st.dataframe(
        df.groupby("Contract", as_index=False)
        .agg(churn_rate=("Churn", "mean"), customers=("customerID", "count"))
        .sort_values("churn_rate", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    st.title("Customer Analytics Dashboard")
    st.caption("Suivi engagement, churn et aide à la décision produit")

    if not DATA_PATH.exists():
        st.error(
            "Fichier data/processed/clean_telco.csv introuvable. "
            "Lancez d'abord le script notebooks/scripts/data_cleaning.py"
        )
        st.stop()

    data = load_data(DATA_PATH)
    filtered = apply_filters(data)

    if filtered.empty:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        st.stop()

    render_kpis(filtered)
    st.divider()
    render_charts(filtered)
    st.divider()
    render_actionable_insights(filtered)


if __name__ == "__main__":
    main()
