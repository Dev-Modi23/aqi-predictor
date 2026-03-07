import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# Page config
st.set_page_config(
    layout="wide", 
    page_title="AI AQI Pro", 
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS - APPLE/GLASSMorphism ==========
st.markdown("""
<style>
/* ROOT VARIABLES */
:root {
    --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --primary-light: #a8b4ff;
    --secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --glass: rgba(255,255,255,0.1);
    --glass-border: rgba(255,255,255,0.2);
}

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

/* HIDE STREAMLIT ELEMENTS */
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }

/* TITLE */
h1 {
    font-family: 'SF Pro Display', -apple-system, sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    background: var(--primary) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}

/* CARDS - GLASSMorphism */
.card {
    background: var(--glass) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 2rem !important;
    box-shadow: 0 25px 50px rgba(0,0,0,0.25) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.card:hover {
    transform: translateY(-8px) !important;
    box-shadow: 0 35px 70px rgba(0,0,0,0.35) !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background: var(--glass) !important;
    border-radius: 20px !important;
    border: 1px solid var(--glass-border) !important;
    padding: 1.5rem !important;
}

/* SELECTBOX */
.stSelectbox > div > div > div {
    background: var(--glass) !important;
    border-radius: 16px !important;
    border: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(10px) !important;
}

/* BUTTONS */
.stButton > button {
    background: var(--success) !important;
    border-radius: 50px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 40px rgba(79, 172, 254, 0.6) !important;
}

/* TABS */
.stTabs [role="tablist"] {
    gap: 1rem;
    border-radius: 16px;
    background: var(--glass);
    padding: 0.5rem;
    margin-bottom: 2rem;
}
.stTabs [role="tab"] {
    background: transparent !important;
    border-radius: 12px !important;
    border: 2px solid var(--glass-border) !important;
    padding: 1rem 2rem !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    background: var(--primary-light) !important;
    border-color: #667eea !important;
    color: #1e293b !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.95) 100%) !important;
}
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR - CITY NAVIGATION ==========
with st.sidebar:
    st.markdown("## 🏙️ Quick Cities")
    
    quick_cities = ["Delhi 🗼", "Mumbai 🏙️", "Bangalore 🌴", "Pune 🏔️", "Surat 🛍️"]
    for city in quick_cities:
        if st.button(city, key=f"quick_{city}", use_container_width=True):
            st.session_state.selected_city = city
            st.rerun()
    
    st.markdown("---")
    st.markdown("*Premium AI Features*")
    st.caption("R²: 0.906 | Dev Modi")

# ========== MAIN CONTENT ==========
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Delhi 🗼"

selected_city_obj = st.selectbox(
    "🎯 Select City", 
    ["Delhi 🗼", "Mumbai 🏙️", "Bangalore 🌴", "Pune 🏔️", "Chennai 🌊", 
     "Kolkata 🕌", "Surat 🛍️", "Ahmedabad 🏰", "Hyderabad 🕌", "Jaipur 🏰",
     "Lucknow 🕌", "Kanpur 🏭", "Nagpur 🏙️", "Indore 🛒"],
    index=0
)
st.session_state.selected_city = selected_city_obj
city_name = selected_city_obj.split()[0]

# ========== AQI CALCULATION ==========
def get_aqi(city_name):
    base_values = {
        "Delhi": 185, "Mumbai": 125, "Bangalore": 90, "Pune": 95, "Chennai": 110,
        "Kolkata": 140, "Surat": 130, "Ahmedabad": 150, "Hyderabad": 115, "Jaipur": 135
    }
    coords = {
        "Delhi": (28.61, 77.21), "Mumbai": (19.07, 72.88), "Bangalore": (12.97, 77.59),
        "Pune":
    }

