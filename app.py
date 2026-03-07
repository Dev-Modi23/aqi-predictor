import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="AI AQI Predictor",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main { background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #f3e8ff 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover { 
        transform: translateY(-8px);
        box-shadow: 0 35px 70px rgba(0,0,0,0.15);
    }
    .metric-card { padding: 2.5rem; }
    .gradient-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
        border: none;
        border-radius: 20px;
        padding: 14px 36px;
        font-weight: 600;
        color: white;
        transition: all 0.3s ease;
        font-size: 1.05rem;
    }
    .gradient-btn:hover { transform: scale(1.05); box-shadow: 0 15px 30px rgba(59,130,246,0.4); }
    .aqi-good { background: #dcfce7; color: #166534; }
    .aqi-moderate { background: #fef3c7; color: #92400e; }
    .aqi-unhealthy { background: #fee2e2; color: #dc2626; }
    </style>
""", unsafe_allow_html=True)

# Simulated AQI prediction data
@st.cache_data
def load_aqi_data():
    dates = pd.date_range("2026-01-01", periods=180, freq="D")
    np.random.seed(42)
    data = pd.DataFrame({
        'date': np.tile(dates, 10),
        'aqi_readings': np.random.normal(85, 25, 1800).clip(10, 300),
        'pm25': np.random.normal(35, 15, 1800).clip(5, 150),
        'pm10': np.random.normal(65, 25, 1800).clip(10, 250),
        'temperature': np.random.normal(28, 8, 1800).clip(10, 45),
        'humidity': np.random.normal(65, 20, 1800).clip(20, 95),
        'city': np.random.choice(['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Surat'], 1800)
    })
    data['predicted_aqi'] = data['aqi_readings'] + np.random.normal(0, 8, 1800)
    data['prediction_accuracy'] = (1 - abs(data['predicted_aqi'] - data['aqi_readings']) / data['aqi_readings']).round(3)
    return data

# Sidebar - Model Controls & City Filter
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem;'>
            <h1 style='font-size: 2.2rem; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-weight: 800; margin: 0;'>🌫️ AI AQI Predictor</h1>
            <p style='color: #6b7280; font-size: 1rem;'>Powered by Machine Learning</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    nav_options = {
        "📊 Dashboard": "dashboard",
        "🔮 Predict AQI": "predict", 
        "📈 History": "history",
        "⚙️ Models": "models"
    }
    selected_page = st.selectbox("Navigate", options=list(nav_options.keys()), index=0)
    
    st.markdown("---")
    st.markdown("<h3 style='color: #374151; font-weight: 600;'>Filters</h3>", unsafe_allow_html=True)
    city_filter = st.multiselect("Cities", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Surat"], default=["Delhi", "Surat"])
    
    st.markdown("---")
    if st.button("🌍 Refresh Data", key="refresh"):
        st.cache_data.clear()
        st.rerun()

# MAIN DASHBOARD
if selected_page == "📊 Dashboard":
    data = load_aqi_data()
    filtered_data = data[data['city'].isin(city_filter)]
    
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2 style='font-size: 2.8rem; font-weight: 800; margin: 0; color: #1f2937;'>AQI Prediction Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6b7280; font-size: 1.2rem; margin-top: 0.75rem;'>Real-time monitoring & ML-powered predictions for {}</p>".format(", ".join(city_filter)), unsafe_allow_html=True)
    
    with col2:
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            st.text_input("🔍 Search predictions...", placeholder="Search by city or date...")
        with search_col2:
            st.markdown('<button class="gradient-btn">Predict Now</button>', unsafe_allow_html=True)
    
    # KPI Cards - 4 Column Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="glass-card metric-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='color: #6b7280; font-size: 0.95rem; font-weight: 500; margin: 0 0 1rem 0;'>Current Avg AQI</p>
                        <p style='font-size: 2.8rem; font-weight: 800; color: #1f2937; margin: 0;'>{filtered_data['aqi_readings'].mean():.0f}</p>
                    </div>
                    <div style='font-size: 3.5rem; opacity: 0.8;'>🌫️</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="glass-card metric-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='color: #6b7280; font-size: 0.95rem; font-weight: 500; margin: 0 0 1rem 0;'>PM2.5 (µg/m³)</p>
                        <p style='font-size: 2.8rem; font-weight: 800; color: #059669; margin: 0;'>{filtered_data['pm25'].mean():.1f}</p>
                    </div>
                    <div style='font-size: 3.5rem; opacity: 0.8;'>⚫</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="glass-card metric-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='color: #6b7280; font-size: 0.95rem; font-weight: 500; margin: 0 0 1rem 0;'>Prediction Accuracy</p>
                        <p style='font-size: 2.8rem; font-weight: 800; color: #10b981; margin: 0;'>97.3%</p>
                    </div>
                    <div style='font-size: 3.5rem; opacity: 0.8;'>🎯</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="glass-card metric-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='color: #6b7280; font-size: 0.95rem; font-weight: 500; margin: 0 0 1rem 0;'>Active Cities</p>
                        <p style='font-size: 2.8rem; font-weight: 800; color: #1f2937; margin: 0;'>{len(city_filter)}</p>
                    </div>
                    <div style='font-size: 3.5rem; opacity: 0.8;'>🏙️</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Main Content Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='font-size: 1.6rem; font-weight: 700; margin-bottom: 2rem; color: #1f2937;'>Recent Predictions</h3>", unsafe_allow_html=True)
        
        recent_data = filtered_data.tail(10)[['city', 'aqi_readings', 'predicted_aqi', 'pm25', 'prediction_accuracy']].round(1)
        recent_data.columns = ['City', 'Actual AQI', 'Predicted AQI', 'PM2.5', 'Accuracy']
        
        st.dataframe(
            recent_data,
            column_config={
                "Predicted AQI": st.column_config.ProgressColumn("Predicted AQI", format="%d"),
                "Accuracy": st.column_config.ProgressColumn("Accuracy", format="%.1f%%", min_value=0, max_value=1)
            },
            use_container_width=True,
            height=450,
            hide_index=True
        )
    
    with col2:
        st.markdown("<h3 style='font-size: 1.6rem; font-weight: 700; margin-bottom: 2rem; color: #1f2937;'>AQI Trends (30 days)</h3>", unsafe_allow_html=True)
        
        trend_data = filtered_data.groupby(filtered_data['date'].dt.date).agg({
            'aqi_readings': 'mean',
            'predicted_aqi': 'mean'
        }).tail(30).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend_data['date'], y=trend_data['aqi_readings'], 
                                name='Actual AQI', line=dict(color='#3b82f6', width=3)))
        fig.add_trace(go.Scatter(x=trend_data['date'], y=trend_data['predicted_aqi'], 
                                name='Predicted AQI', line=dict(color='#10b981', width=3, dash='dash')))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=450,
            showlegend=True,
            legend=dict(y=0.99, x=0.01)
        )
        st.plotly_chart(fig, use_container_width=True)

# PREDICTION PAGE
elif selected_page == "🔮 Predict AQI":
    st.markdown("<h2 style='font-size: 2.8rem; font-weight: 800; color: #1f2937;'>Predict AQI</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4 style='color: #374151; font-weight: 600;'>🌍 Location & Weather</h4>", unsafe_allow_html=True)
        city = st.selectbox("City", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Surat"])
        temp = st.slider("Temperature (°C)", 10.0, 45.0, 28.0)
        humidity = st.slider("Humidity (%)", 20.0, 95.0, 65.0)
        
    with col2:
        st.markdown("<h4 style='color: #374151; font-weight: 600;'>🌪️ Pollutants</h4>", unsafe_allow_html=True)
        pm25 = st.slider("PM2.5 (µg/m³)", 5.0, 150.0, 35.0)
        pm10 = st.slider("PM10 (µg/m³)", 10.0, 250.0, 65.0)
        
        model = st.selectbox("ML Model", ["Random Forest", "XGBoost", "LSTM", "LightGBM"])
    
    if st.button("🚀 Predict AQI", key="predict", help="Run ML prediction"):
        with st.spinner("Running prediction..."):
            time.sleep(2)
            
        # Mock ML prediction (replace with your model!)
        predicted_aqi = 78 + 0.8*pm25*0.3 + 0.4*pm10*0.1 + 0.2*(temp-25)*0.05 + np.random.normal(0, 5)
        predicted_aqi = max(10, min(300, round(predicted_aqi)))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Predicted AQI", f"{predicted_aqi:.0f}", "↑ 2.3%")
        with col2:
            st.metric("Risk Level", "Moderate" if predicted_aqi < 100 else "Unhealthy")
        with col3:
            st.metric("Confidence", "96.8%", "+0.4%")
            
        st.balloons()

# Run with: streamlit run aqi_predictor.py
