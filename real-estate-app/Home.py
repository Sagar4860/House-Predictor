import streamlit as st

st.set_page_config(
    page_title="🏠 Real Estate App",
    page_icon="🏡",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f9fafc;
        padding: 20px;
    }
    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-top: 30px;
        padding:20px;
    }
    .description {
        font-size: 18px !important;
        color: #dcdcdc;
        text-align: center;
        margin-bottom: 20px;
    }
    .small-img {
        
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 30%;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding:20px;
    }
    </style>
    <div style="background-color:#6c63ff; padding:20px; border-radius:12px;">
        <p class='big-font'>🏠 Welcome to the Real Estate Price Intelligence Dashboard</p>
        <p class='description'>Navigate through the sidebar to predict house prices, explore visualizations, and analyze insights.</p>
    </div>
""", unsafe_allow_html=True)

# --- Image with fixed size ---
st.markdown(
    '<img src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914" class="small-img">',
    unsafe_allow_html=True
)

st.markdown("### 📌 Features:")
st.markdown("""
- 📈 **Price Predictor**: Get an estimated price based on property features.
- 📊 **Visualization**: Explore property trends, price distribution, maps, and radar charts.
- 🔍 **Insights**: Understand patterns across sectors and property types.
""")
