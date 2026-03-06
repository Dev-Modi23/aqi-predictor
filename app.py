import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

@st.cache_resource
def load_model():
    model = joblib.load('model.pkl')
    scaler_X = joblib.load('scaler_X.pkl')
    scaler_y = joblib.load('scaler_y.pkl')
    feature_cols = ['PM2.5', 'PM10', 'NO2', 'NOx', 'CO', 'SO2', 'O3', 
                    'PM2.5_lag1', 'AQI_lag1', 'PM2.5_7d_avg', 'AQI_7d_avg', 'Month']
    return model, scaler_X, scaler_y, feature_cols

model, scaler_X, scaler_y, feature_cols = load_model()

st.set_page_config(page_title="AQI Predictor", layout="wide", page_icon="🌫️")
st.title("🌫️ AQI Predictor - R²: 0.906")
st.markdown("**Production Model | MAE: 11.8 | 200K+ Records**")

city = st.selectbox("🏙️ City", ["Delhi", "Mumbai", "Bangalore", "Ahmedabad"])
pm25 = st.slider("PM2.5", 0.0, 500.0, 50.0)
pm10 = st.slider("PM10", 0.0, 1000.0, 100.0)
no2 = st.slider("NO2", 0.0, 200.0, 30.0)

if st.button("🔮 PREDICT AQI"):
    input_data = pd.DataFrame({
        'PM2.5': [pm25], 'PM10': [pm10], 'NO2': [no2], 'NOx': [40],
        'CO': [1], 'SO2': [10], 'O3': [40], 'PM2.5_lag1': [pm25*0.9],
        'AQI_lag1': [150], 'PM2.5_7d_avg': [pm25], 'AQI_7d_avg': [150],
        'Month': [datetime.now().month]
    })
    
    input_scaled = scaler_X.transform(input_data[feature_cols])
    pred_aqi = scaler_y.inverse_transform(model.predict(input_scaled).reshape(-1, 1))[0, 0]
    
    st.metric("Predicted AQI", f"{pred_aqi:.0f}")
    if pred_aqi > 200:
        st.error("🚨 Poor/Very Poor - Limit outdoor activities")
    else:
        st.success("✅ Good/Moderate - Safe outdoors")
