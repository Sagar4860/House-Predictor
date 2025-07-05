import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="🏠 House Price Predictor", layout="centered")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6fa;
        }
        .main {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
        }
        h1, h2, h3, h4 {
            text-align: center;
            color: #4a4a4a;
        }
        .stButton>button {
            background-color: #6c63ff;
            color: white;
            font-weight: 500;
            border-radius: 6px;
            padding: 0.6em 1.2em;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #5548d9;
        }
        .stSelectbox>div>div {
            font-weight: 500;
        }
        .css-1y4p8pa {
            padding-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# import pickle
from huggingface_hub import hf_hub_download
import pickle

# Download the model file from Hugging Face
model_path = hf_hub_download(repo_id="sagar4860/house-prediction", filename="pipeline.pkl")

# Load the pickle model
with open(model_path, "rb") as f:
    pipeline = pickle.load(f)

# --- Load Data ---
import os
import pickle

# Define base and dataset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'datasets')

# Load data using full path
with open(os.path.join(DATA_DIR, 'df.pkl'), 'rb') as file:
    df = pickle.load(file)

# --- Header ---
st.markdown("## 🏡 Real Estate Price Estimator")
st.markdown("<p style='text-align:center; font-size:18px; color:gray;'>Fill in the property details to get an accurate price prediction</p>", unsafe_allow_html=True)

# --- Input Form ---
with st.form("prediction_form"):
    st.markdown("### 🔧 Input Property Features")

    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox('🏘️ Property Type', ['flat', 'house'])
        sector = st.selectbox('📍 Sector', sorted(df['sector'].unique()))
        bedrooms = float(st.selectbox('🛏️ Number of Bedrooms', sorted(df['bedRoom'].unique())))
        bathroom = float(st.selectbox('🚿 Number of Bathrooms', sorted(df['bathroom'].unique())))
        balcony = st.selectbox('🌤️ Balconies', sorted(df['balcony'].unique()))
        built_up_area = float(st.number_input('📐 Built Up Area (sqft)', min_value=100.0, value=1000.0))

    with col2:
        property_age = st.selectbox('🏗️ Property Age', sorted(df['agePossession'].unique()))
        servant_room = float(st.selectbox('🧹 Servant Room', [0.0, 1.0]))
        store_room = float(st.selectbox('📦 Store Room', [0.0, 1.0]))
        furnishing_type = st.selectbox('🪑 Furnishing Type', sorted(df['furnishing_type'].unique()))
        luxury_category = st.selectbox('💎 Luxury Category', sorted(df['luxury_category'].unique()))
        floor_category = st.selectbox('🏢 Floor Category', sorted(df['floor_category'].unique()))

    submitted = st.form_submit_button("📈 Predict Price")

# --- Prediction Section ---
if submitted:
    st.markdown("### 📊 Prediction Result")
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)

    try:
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = round(base_price - 0.22, 2)
        high = round(base_price + 0.22, 2)

        st.success(f"💰 The estimated price range is between **₹{low} Cr** and **₹{high} Cr**")
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
