import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Beautiful Real Estate Dashboard", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu, footer {visibility: hidden;}

    /* Main background */
    .main {
        background-color: #f0f2f6;
    }

    /* Header styles */
    h1, h2, h3 {
        color: #0e1117;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Custom container card */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: black;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏡 Real Estate Data Dashboard</h1>", unsafe_allow_html=True)

st.title('Analytics')

# Load and preprocess
df = pd.read_csv('..datasets/data_viz1.csv')
feature_text = pickle.load(open('..datasets/feature_text.pkl', 'rb'))

numeric_cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
group_df = df.groupby('sector')[numeric_cols].mean().reset_index()

# Section: Geomap with card styling
with st.container():
    st.markdown("""
        <div style="background-color:#ffffff;padding:20px 30px;border-radius:12px;
        box-shadow:0 4px 12px rgba(0, 0, 0, 0.1);margin-bottom:25px;">
        <h3 style="color:#1f77b4;">📍 Sector Price per Sqft Geomap</h3>
    """, unsafe_allow_html=True)

    fig = px.scatter_mapbox(
        group_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size='built_up_area',
        color_continuous_scale=px.colors.sequential.Sunsetdark,
        zoom=10,
        mapbox_style="open-street-map",
        height=600,
        hover_name='sector'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Section: Word Cloud in center
with st.container():
    st.markdown("""
        <div style="background-color:#ffffff;padding:20px 30px;border-radius:12px;
        box-shadow:0 4px 12px rgba(0, 0, 0, 0.1);text-align:center;">
        <h3 style="color:#ff7f0e;">☁️ Common Features Word Cloud</h3>
    """, unsafe_allow_html=True)

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='Set2'
    ).generate(feature_text)

    fig_wc, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_wc)

    st.markdown("</div>", unsafe_allow_html=True)


# ✅ Pass the figure to st.pyplo
# --- Area vs Price Section ---
with st.container():
    st.markdown("""
        <div style="background-color:#f8f9fa;padding:20px 30px;border-radius:12px;
        box-shadow:0 4px 12px rgba(0, 0, 0, 0.05);margin-bottom:30px;">
        <h3 style="color:#28a745;text-align:center;">📈 Area vs Price Scatter Plot</h3>
    """, unsafe_allow_html=True)

    property_type = st.selectbox('Select Property Type', ['flat', 'house'])

    filtered_df = df[df['property_type'] == property_type]

    fig1 = px.scatter(
        filtered_df,
        x="built_up_area",
        y="price",
        color="bedRoom",
        title=f"Area vs Price for {property_type.title()}s",
        color_continuous_scale="Viridis",
        hover_data=['sector', 'society']
    )
    fig1.update_layout(height=500)

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- BHK Distribution Pie Chart ---
with st.container():
    st.markdown("""
        <div style="background-color:#f1f3f5;padding:20px 30px;border-radius:12px;
        box-shadow:0 4px 10px rgba(0, 0, 0, 0.05);margin-bottom:30px;">
        <h3 style="color:#17a2b8;text-align:center;">🏘️ BHK Distribution by Sector</h3>
    """, unsafe_allow_html=True)

    sector_options = df['sector'].unique().tolist()
    sector_options.insert(0, 'overall')

    selected_sector = st.selectbox('Select Sector', sector_options)

    if selected_sector == 'overall':
        fig2 = px.pie(
            df,
            names='bedRoom',
            title='Overall BHK Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
    else:
        filtered = df[df['sector'] == selected_sector]
        fig2 = px.pie(
            filtered,
            names='bedRoom',
            title=f'BHK Distribution in Sector {selected_sector}',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Side-by-Side BHK Price Comparison ---
with st.container():
    st.markdown("""
        <div style="background-color:#fff3cd;padding:20px 30px;border-radius:12px;
        box-shadow:0 4px 10px rgba(0, 0, 0, 0.05);margin-bottom:30px;">
        <h3 style="color:#856404;text-align:center;">💰 BHK Price Comparison</h3>
    """, unsafe_allow_html=True)

    fig3 = px.box(
        df[df['bedRoom'] <= 4],
        x='bedRoom',
        y='price',
        title='Price Distribution across BHK Types (≤ 4 BHK)',
        color='bedRoom',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig3.update_layout(xaxis_title='BHK', yaxis_title='Price')

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# --- Import Setup ---
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown("<h2 style='text-align:center;color:#6c63ff;'>📊 Real Estate Insights Dashboard</h2>", unsafe_allow_html=True)

# Assuming df is already loaded and preprocessed
# --- Distribution Plot ---
with st.container():
    st.markdown("""
    <div style="background-color:#e9f7ef;padding:20px 30px;border-radius:12px;margin-top:25px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    <h4 style="color:#2c3e50;text-align:center;">🏡 Price Distribution for Property Types</h4>
    """, unsafe_allow_html=True)

    fig_dist = plt.figure(figsize=(10, 4))
    sns.histplot(df[df['property_type'] == 'house']['price'], label='House', color='blue', kde=True)
    sns.histplot(df[df['property_type'] == 'flat']['price'], label='Flat', color='green', kde=True)
    plt.legend()
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    st.pyplot(fig_dist)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Heatmap ---
with st.container():
    st.markdown("""
    <div style="background-color:#fbeee6;padding:20px 30px;border-radius:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    <h4 style="color:#d35400;text-align:center;">🔥 Correlation Heatmap</h4>
    """, unsafe_allow_html=True)

    numeric_df = df.select_dtypes(include=['number'])
    fig_corr, ax3 = plt.subplots(figsize=(12, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
    st.pyplot(fig_corr)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Furnishing Type Pie Chart ---
with st.container():
    st.markdown("""
    <div style="background-color:#eaf2f8;padding:20px 30px;border-radius:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    <h4 style="color:#1f618d;text-align:center;">🛋️ Furnishing Type Distribution</h4>
    """, unsafe_allow_html=True)

    furnishing_counts = df['furnishing_type'].value_counts()
    fig5 = px.pie(names=furnishing_counts.index, values=furnishing_counts.values, 
                  title="Furnishing Type Distribution",
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Radar Chart ---
with st.container():
    st.markdown("""
    <div style="background-color:#f9ebea;padding:20px 30px;border-radius:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);">
    <h4 style="color:#c0392b;text-align:center;">📡 Property Radar Snapshot</h4>
    """, unsafe_allow_html=True)

    row = df.iloc[0]
    features = ['bedRoom', 'bathroom', 'balcony', 'luxury_score']
    values = [row[feat] for feat in features]

    fig_radar = px.line_polar(r=values, theta=features, line_close=True,
                              title=f"Radar Chart for {row['society']}, {row['sector']}")
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Treemap ---
with st.container():
    avg_area_df = df.groupby(['sector', 'society'], as_index=False).agg({
        'built_up_area': 'mean',
        'price': 'mean'
    })
    fig_tree = px.treemap(
        avg_area_df,
        path=['sector', 'society'],
        values='built_up_area',
        color='price',
        color_continuous_scale='RdYlGn',
        title="🏙️ Treemap: Avg Built-up Area & Price"
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# --- Age vs Price Boxplot ---
with st.container():
    st.markdown("<h4 style='text-align:center;color:#6c3483;'>🏗️ Age of Property vs Price</h4>", unsafe_allow_html=True)
    fig_age = px.box(df, x='agePossession', y='price', color='property_type',
                     title='Property Age vs Price Distribution')
    st.plotly_chart(fig_age, use_container_width=True)

# --- Luxury Score Scatter Plot ---
with st.container():
    st.markdown("<h4 style='text-align:center;color:#117864;'>💎 Luxury Score vs Price per Sqft</h4>", unsafe_allow_html=True)
    fig_lux = px.scatter(df, x='luxury_score', y='price_per_sqft', color='property_type',
                         size='built_up_area', hover_data=['society', 'sector'])
    st.plotly_chart(fig_lux, use_container_width=True)

# --- Sector-wise Summary Table ---
with st.container():
    st.markdown("<h4 style='text-align:center;color:#2e4053;'>📍 Sector Summary Stats</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    selected_sector = col1.selectbox("Sector", df['sector'].unique())
    selected_type = col2.selectbox("Property Type", df['property_type'].unique())

    filtered = df[(df['sector'] == selected_sector) & (df['property_type'] == selected_type)]
    if not filtered.empty:
        st.dataframe(filtered.describe()[['price', 'price_per_sqft', 'built_up_area', 'luxury_score']])
    else:
        st.warning("No data available for the selected filters.")

# --- Furnishing Type vs Price Boxplot ---
with st.container():
    st.markdown("<h4 style='text-align:center;color:#a04000;'>🧾 Price by Furnishing Type</h4>", unsafe_allow_html=True)
    fig_furn = px.box(df, x='furnishing_type', y='price', color='furnishing_type',
                      title="Price Variation by Furnishing Type")
    st.plotly_chart(fig_furn, use_container_width=True)
