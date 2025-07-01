import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="🏘️ Apartment Recommender", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        background-color: #f4f6fa;
    }
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    h1, h2 {
        text-align: center;
        color: #4a4a4a;
    }
    .stSelectbox > div {
        font-weight: 500;
    }
    .small-text {
        font-size: 16px;
        color: #555;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'datasets')

with open(os.path.join(DATA_DIR, 'location_df.pkl'), 'rb') as f:
    location_df = pickle.load(f)

with open(os.path.join(DATA_DIR, 'cosine_sim1.pkl'), 'rb') as f:
    cosine_sim1 = pickle.load(f)

with open(os.path.join(DATA_DIR, 'cosine_sim2.pkl'), 'rb') as f:
    cosine_sim2 = pickle.load(f)

with open(os.path.join(DATA_DIR, 'cosine_sim3.pkl'), 'rb') as f:
    cosine_sim3 = pickle.load(f)


# --- Recommendation Function ---
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        '🏢 Property Name': top_properties,
        '🔗 Similarity Score': [round(score, 3) for score in top_scores]
    })

# --- App Header ---
st.markdown("<h2>📍 Location-Based Apartment Search</h2>", unsafe_allow_html=True)

with st.form("search_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_location = st.selectbox("Select a location", sorted(location_df.columns.to_list()))
    with col2:
        radius = st.number_input("Radius (in Kms)", min_value=1.0, max_value=50.0, value=5.0)

    search = st.form_submit_button("🔍 Search Nearby")

if search:
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    if not result_ser.empty:
        st.markdown("### 🏙️ Nearby Apartments")
        for key, value in result_ser.items():
            st.markdown(f"- **{key}** — _{round(value / 1000, 2)} km_")
    else:
        st.warning("No properties found in this radius.")

# --- Recommendations ---
st.markdown("<h2>💡 Recommend Similar Apartments</h2>", unsafe_allow_html=True)

with st.form("recommend_form"):
    selected_appartment = st.selectbox("Choose an apartment", sorted(location_df.index.to_list()))
    recommend = st.form_submit_button("✨ Recommend")

if recommend:
    st.markdown(f"### 🔮 Recommendations based on **{selected_appartment}**")
    recommendation_df = recommend_properties_with_scores(selected_appartment)
    st.dataframe(recommendation_df.style.format({'🔗 Similarity Score': "{:.3f}"}).highlight_max(axis=0))
