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
    page_title="AI Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .glass-card:hover { 
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.1);
    }
    .metric-card { padding: 2rem; }
    .gradient-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 16px;
        padding: 12px 32px;
        font-weight: 600;
        color: white;
        transition: all 0.3s ease;
    }
    .gradient-btn:hover { transform: scale(1.05); }
    .status-scam { background: #fee2e2; color: #dc2626; }
    .status-safe { background: #d1fae5; color: #059669; }
    </style>
""", unsafe_allow_html=True)

# Simulated data
@st.cache_data
def load_sample_data():
    dates = pd.date_range("2026-01-01", periods=180, freq="D")
    np.random.seed(42)
    data = pd.DataFrame({
        'date': np.tile(dates, 10),
        'scans': np.random.poisson(50, 1800),
        'scams_detected': np.random.binomial(50, 0.12, 1800)
    })
    data['detection_rate'] = (data['scams_detected'] / data['scans'] * 100).round(1)
    return data

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem;'>
            <h1 style='font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       font-weight: 700; margin: 0;'>🛡️ AI Scam Detector</h1>
        </div>
    """, unsafe_allow_html=True)
    
    nav_options = {
        "📊 Dashboard": "dashboard",
        "📁 Scan Data": "scan",
        "📋 History": "history", 
        "⚙️ Settings": "settings"
    }
    
    selected = st.selectbox("Navigation", options=list(nav_options.keys()), index=0)
    st.markdown("---")

# Main Dashboard Content
if selected == "📊 Dashboard":
    data = load_sample_data()
    
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2 style='font-size: 2.5rem; font-weight: 700; margin: 0;'>Scam Detection Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-top: 0.5rem;'>Monitor AI-powered scam detection in real-time</p>", unsafe_allow_html=True)
    
    with col2:
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            st.text_input("🔍 Search scans...", placeholder="Search by file, ID, or source...")
        with search_col2:
            st.button("New Scan", key="new_scan", help="Upload file for scam analysis")
    
    # Stats Cards - 4 Column Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown("""
                <div class="glass-card metric-card">
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin: 0 0 0.5rem 0;'>Total Scans</p>
                            <p style='font-size: 2.5rem; font-weight: 700; color: #111827; margin: 0;'>1,847</p>
                        </div>
                        <div style='font-size: 3rem; opacity: 0.7;'>📈</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("""
                <div class="glass-card metric-card">
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin: 0 0 0.5rem 0;'>Scams Detected</p>
                            <p style='font-size: 2.5rem; font-weight: 700; color: #dc2626; margin: 0;'>221</p>
                            <p style='color: #059669; font-size: 0.75rem; font-weight: 500; margin: 0.5rem 0 0 0;'>12.0% rate</p>
                        </div>
                        <div style='font-size: 3rem; opacity: 0.7;'>🛡️</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown("""
                <div class="glass-card metric-card">
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin: 0 0 0.5rem 0;'>Accuracy</p>
                            <p style='font-size: 2.5rem; font-weight: 700; color: #059669; margin: 0;'>98.7%</p>
                        </div>
                        <div style='font-size: 3rem; opacity: 0.7;'>✅</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="glass-card metric-card">
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin: 0 0 0.5rem 0;'>Active Models</p>
                        <p style='font-size: 2.5rem; font-weight: 700; color: #111827; margin: 0;'>5</p>
                    </div>
                    <div style='font-size: 3rem; opacity: 0.7;'>🧠</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem;'>Recent Scans</h3>", unsafe_allow_html=True)
        
        # Sample recent scans table
        recent_scans = pd.DataFrame({
            'ID': ['#1847', '#1846', '#1845', '#1844'],
            'File/Source': ['email_phish.txt', 'sms_offer.html', 'invoice_fake.pdf', 'website_scam.com'],
            'Status': ['Scam', 'Safe', 'Scam', 'Suspicious'],
            'Score': ['92%', '12%', '87%', '65%'],
            'Time': ['2 min ago', '15 min ago', '1 hr ago', '3 hrs ago']
        })
        
        st.dataframe(
            recent_scans,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Safe", "Scam", "Suspicious"],
                    required=True
                ),
                "Score": st.column_config.ProgressColumn(
                    "Confidence",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                )
            },
            use_container_width=True,
            height=400
        )
    
    with col2:
        st.markdown("<h3 style='font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem;'>Detection Trends</h3>", unsafe_allow_html=True)
        
        # Trend chart
        daily_stats = data.groupby(data['date'].dt.date).agg({
            'scans': 'sum',
            'scams_detected': 'sum'
        }).tail(30).reset_index()
        daily_stats['date'] = pd.to_datetime(daily_stats['date'])
        
        fig = px.line(daily_stats, x='date', y='scams_detected', 
                     title="Scams Detected Over Time",
                     labels={'scams_detected': 'Scams Detected', 'date': 'Date'})
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# File Upload Section (Scan Data page)
elif selected == "📁 Scan Data":
    st.markdown("<h2 style='font-size: 2.5rem; font-weight: 700;'>Upload & Scan</h2>", unsafe_allow_html=True)
    
    # File upload with drag & drop styling
    uploaded_file = st.file_uploader(
        "Choose a file or drag and drop",
        type=['txt', 'pdf', 'html', 'docx'],
        help="Supports text files, PDFs, HTML, and Word documents"
    )
    
    if uploaded_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        progress_bar = col2.progress(0)
        status_text = col2.empty()
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            status_text.text(f"Analyzing... {i+1}%")
        
        st.success("✅ Analysis Complete!")
        st.balloons()
        
        # Results
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Scam Probability", "8.2%", "-2.1%")
        with col2:
            st.metric("Risk Level", "LOW", "Safe")
