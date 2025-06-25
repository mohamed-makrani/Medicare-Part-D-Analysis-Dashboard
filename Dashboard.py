import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("Cleaned_Dataset.csv")

# Compute metrics
top_generic_claims = data.groupby('Gnrc_Name')['Tot_Clms'].sum().sort_values(ascending=False).head(5).reset_index()
top_brand_claims = data.groupby('Brnd_Name')['Tot_Clms'].sum().sort_values(ascending=False).head(5).reset_index()
top_generic_cost = data.groupby('Gnrc_Name')['Tot_Drug_Cst'].sum().sort_values(ascending=False).head(5).reset_index()
correlation = data[['Tot_Clms','Tot_Drug_Cst']].corr().iloc[0,1]

# KPI metrics
total_claims = data["Tot_Clms"].sum()
total_cost = data["Tot_Drug_Cst"].sum()
top_claimed_generic = top_generic_claims["Gnrc_Name"][0]
top_claimed_count = top_generic_claims["Tot_Clms"][0]
top_costly_generic = top_generic_cost["Gnrc_Name"][0]
top_cost_value = top_generic_cost["Tot_Drug_Cst"][0]

# Streamlit app layout
st.set_page_config(page_title="Medicare Part D Dashboard", layout="wide")
st.title("💊 Medicare Part D Prescription Analysis Dashboard")
st.markdown("""
This interactive dashboard explores:
- Prescription claim counts (Generic & Brand).
- Cost distribution across top medications.
- Relationship between usage and total cost.
""")

# KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Claims", f"{total_claims:,}")
kpi2.metric("Total Cost", f"${total_cost/1e9:.2f}B")
kpi3.metric("Top Claimed Generic", f"{top_claimed_generic} ({top_claimed_count:,})")
kpi4.metric("Top Costly Generic", f"{top_costly_generic} (${top_cost_value/1e9:.2f}B)")

st.markdown("---")

# Charts
st.subheader("Top 5 Generic Drugs by Claims")
fig1 = px.bar(top_generic_claims, x="Gnrc_Name", y="Tot_Clms",
              title="Top 5 Generic Drugs by Claims",
              labels={'Gnrc_Name': 'Generic Name','Tot_Clms': 'Total Claims'},
              color='Gnrc_Name')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Top 5 Brand Name Drugs by Claims")
fig2 = px.bar(top_brand_claims, x="Brnd_Name", y="Tot_Clms",
              title="Top 5 Brand Name Drugs by Claims",
              labels={'Brnd_Name': 'Brand Name','Tot_Clms': 'Total Claims'},
              color='Brnd_Name')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top 5 Generic Drugs by Cost")
top_generic_cost["Cost (Billions)"] = top_generic_cost["Tot_Drug_Cst"]/1e9
fig3 = px.bar(top_generic_cost, x="Gnrc_Name", y="Cost (Billions)",
              title="Top 5 Generic Drugs by Cost",
              labels={'Gnrc_Name': 'Generic Name','Cost (Billions)': 'Cost (Billions $)'},
              color='Gnrc_Name')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Correlation
st.subheader(f"Correlation Between Total Claims and Cost: {correlation:.2f}")

st.markdown("""
✅ This relatively low-to-moderate correlation suggests that cost is NOT directly proportional to the number of claims.  
✅ High-cost medications with lower claim counts (e.g., Apixaban, Semaglutide) drive significant expense.
""")

st.markdown("""
---
**Future Directions:**
- Incorporate regional and patient-level analytics.
- Evaluate clinical outcomes associated with high-cost medications.
- Identify opportunities for cost optimization and targeted negotiations.
""")
