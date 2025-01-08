import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from pyDecision.algorithm import waspas_method

API_URL = "http://127.0.0.1:8000/api"
CALCULATION_URL = f"{API_URL}/calculation/?method=waspas"

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

def calculate_wsm(weights):
    params = {"method": "waspas", "weights": ",".join(map(str, weights))}
    response = requests.get(CALCULATION_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch WSM results. Status code: {response.status_code}")
        return {}

st.title("Investment Decision Visualization")

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

normalized_weights = [w / sum(weights) for w in weights]
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

    dataset = []
    for company in companies:
        row = [company[criterion["field"]] for criterion in criteria]
        dataset.append(row)

    dataset = np.array(dataset)
    weights = np.array(normalized_weights)

    lambda_value = 0.5 
    wsm, wpm, waspas_scores = waspas_method(dataset, ["max"] * len(criteria), weights, lambda_value, graph=False)

    results_df = pd.DataFrame({
        "Company": [company["name"] for company in companies],
        "Score": waspas_scores
    }).sort_values(by="Score", ascending=False)

    st.table(results_df)

    st.bar_chart(results_df.set_index("Company")["Score"])