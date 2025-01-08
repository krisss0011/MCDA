import streamlit as st
import requests
import pandas as pd
import numpy as np
from pyDecision.algorithm import ahp_method  # Use your provided AHP library

API_URL = "http://127.0.0.1:8000/api"

def fetch_criteria():
    response = requests.get(f"{API_URL}/default-criteria/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch criteria. Status code: {response.status_code}")
        return []

def fetch_companies():
    response = requests.get(f"{API_URL}/companies/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch companies. Status code: {response.status_code}")
        return []

st.title("AHP Investment Decision Visualization")

st.sidebar.header("Adjust Criteria Weights")
criteria = fetch_criteria()
if not criteria:
    st.stop()

weights = []
for criterion in criteria:
    weight = st.sidebar.slider(
        f"{criterion['name']} Weight",
        min_value=0.0,
        max_value=1.0,
        value=criterion["default_weight"],
        step=0.01,
    )
    weights.append(weight)

# Normalize weights
weights = np.array(weights)
normalized_weights = weights / weights.sum()
st.sidebar.markdown("### Normalized Weights:")
st.sidebar.write(normalized_weights)

if st.button("Run Analysis"):
    st.header("Criteria and Weights")
    for i, criterion in enumerate(criteria):
        st.write(f"{criterion['name']}: {normalized_weights[i]:.2f}")

    st.header("Top Ranked Companies")
    companies = fetch_companies()
    if not companies:
        st.stop()

    # Prepare dataset
    dataset = []
    for company in companies:
        row = [company[criterion["field"]] for criterion in criteria]
        dataset.append(row)

    dataset = np.array(dataset)

    # Create pairwise comparison matrix
    comparison_matrix = np.outer(normalized_weights, 1 / normalized_weights)

    # Calculate AHP weights and consistency ratio
    ahp_weights, consistency_ratio = ahp_method(comparison_matrix, wd="geometric")
    if consistency_ratio > 0.1:
        st.warning(f"Consistency ratio is high ({consistency_ratio:.2f}). Please review the weight adjustments.")

    # Calculate AHP scores
    scores = np.dot(dataset, ahp_weights)
    results_df = pd.DataFrame({
        "Company": [company["name"] for company in companies],
        "Score": scores
    }).sort_values(by="Score", ascending=False)

    st.table(results_df)

    # Bar chart for visualization
    st.bar_chart(results_df.set_index("Company")["Score"])
