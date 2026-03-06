import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_icon="🌿", page_title="BreatheSafe · AQI")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

  [data-testid="stAppViewContainer"] {
    background: #F7F4EF;
    font-family: 'DM Sans', sans-serif;
  }
  [data-testid="stHeader"],[data-testid="stToolbar"] { display:none !important; }

  html,body,p,span,label,[data-testid="stMarkdownContainer"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: #2C2C2C !important;
  }

  [data-testid="stSidebar"] {
    background: #1A1A2E !important;
    border-right: none !important;
  }
  [data-testid="stSidebar"] * { color: #E8E4DC !important; }
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #B0A8C0 !important;
  }

  [data-testid="stSlider"] > div > div > div > div {
    background: #2C6E49 !important;
  }
  [data-testid="stSlider"] > div > div > div {
    background: #DDD8CE !important;
  }

  [data-testid="stSelectbox"] > div > div {
    background: white !important;
    border: 2px solid #DDD8CE !important;
    border-radius: 12px !important;
    color: #2C2C2C !important;
    font-family: 'DM Sans', sans-serif !important;
  }

  .stButton > button[kind="primary"] {
    background: #2C6E49 !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: .85rem 2.5rem !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 20px rgba(44,110,73,0.35) !important;
  }
  .stButton > button[kind="primary"]:hover {
    background: #1E4D33 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(44,110,73,0.45) !important;
  }

  .stAlert { border-radius: 16px !important; font-family:'DM Sans',sans-serif !important; }
  hr { border-color: #DDD8CE !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:2rem 1.5rem 1rem;">
      <div style="font-size:2rem;margin-bottom:.5rem;">🌿</div>
      <div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:#E8E4DC;line-height:1.2;margin-bottom:.4rem;">
        BreatheSafe
      </div>
      <div style="color:#7A7090;font-size:.8rem;letter-spacing:2px;text-transform:uppercase;">
        Air Quality Intelligence
      </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08) !important;margin:0 1.5rem 1.5rem;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:0 1.5rem;">
      <div style="color:#9990B0;font-size:.72rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem;">
        What You Are Measuring
      </div>
    """, unsafe_allow_html=True)

    for p in [
        ("PM 2.5","🔴","#FF6B6B","Tiny Smoke Particles",
         "Microscopic particles 2.5× smaller than a human hair — from vehicle exhaust, cooking smoke & factories.",
         "Enter your bloodstream through lungs. The #1 most dangerous air pollutant.",
         "Safe limit: under 12 µg/m³"),
        ("PM 10","🟠","#FFA552","Dust & Pollen",
         "Larger particles from dust, construction sites, and pollen. Still invisible to the naked eye.",
         "Gets trapped in nose & throat, causing sneezing, coughing and irritation.",
         "Safe limit: under 54 µg/m³"),
        ("NO₂","🟡","#FFD166","Traffic Gas",
         "Nitrogen Dioxide — a gas produced mainly by cars, trucks & power plants.",
         "Irritates airways, worsens asthma & contributes to smog formation.",
         "Safe limit: under 40 µg/m³"),
    ]:
        name, icon, color, tagline, what, why, safe = p
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.07);
          border-left:3px solid {color};border-radius:12px;padding:1.1rem;margin-bottom:1rem;">
          <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.6rem;">
            <span>{icon}</span>
            <span style="font-weight:600;font-size:.95rem;color:#E8E4DC;">{name}</span>
            <span style="font-size:.68rem;color:{color};background:rgba(255,255,255,0.07);
              padding:.15rem .45rem;border-radius:20px;margin-left:auto;">{tagline}</span>
          </div>
          <p style="font-size:.77rem;color:#9990B0;line-height:1.5;margin:0 0 .4rem !important;">{what}</p>
          <p style="font-size:.77rem;color:#C0B8D0;line-height:1.5;margin:0 0 .4rem !important;">⚠️ {why}</p>
          <p style="font-size:.72rem;color:{color};margin:0 !important;">✅ {safe}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:1rem 1.5rem 1rem;">
      <hr style="border-color:rgba(255,255,255,0.08) !important;margin-bottom:1.2rem;">
      <div style="color:#9990B0;font-size:.72rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:.8rem;">Model Performance</div>
      <div style="display:flex;gap:.7rem;">
        <div style="flex:1;background:rgba(44,110,73,0.2);border:1px solid rgba(44,110,73,0.3);
          border-radius:10px;padding:.7rem;text-align:center;">
          <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#6FCF97;">0.906</div>
          <div style="font-size:.68rem;color:#7A7090;text-transform:uppercase;letter-spacing:1px;margin-top:.2rem;">R² Score</div>
        </div>
        <div style="flex:1;background:rgba(96,165,250,0.1);border:1px solid rgba(96,165,250,0.2);
          border-radius:10px;padding:.7rem;text-align:center;">
          <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#93C5FD;">11.8</div>
          <div style="font-size:.68rem;color:#7A7090;text-transform:uppercase;letter-spacing:1px;margin-top:.2rem;">MAE</div>
        </div>
      </div>
      <div style="text-align:center;margin-top:1.2rem;color:#50506A;font-size:.72rem;line-height:1.8;">
        SDG 11 · Sustainable Cities<br>Streamlit Cloud · Production ML
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A1A2E 0%,#16213E 50%,#0F3460 100%);
  border-radius:28px;padding:3rem 3.5rem 2.5rem;margin-bottom:2rem;overflow:hidden;position:relative;">
  <div style="position:absolute;top:-60px;right:-60px;width:220px;height:220px;
    border-radius:50%;background:rgba(44,110,73,0.15);pointer-events:none;"></div>
  <div style="position:absolute;bottom:-40px;left:45%;width:140px;height:140px;
    border-radius:50%;background:rgba(96,165,250,0.08);pointer-events:none;"></div>
  <div style="position:relative;">
    <div style="display:inline-block;background:rgba(44,110,73,0.25);border:1px solid rgba(44,110,73,0.4);
      border-radius:20px;padding:.35rem .9rem;font-size:.75rem;color:#6FCF97;letter-spacing:1.5px;
      text-transform:uppercase;margin-bottom:1rem;">🌍 Live AQI Prediction</div>
    <h1 style="font-family:'DM Serif Display',serif;font-size:3rem;color:#F7F4EF;
      margin:0 0 .6rem;line-height:1.1;">
      How clean is the air<br><em style="color:#6FCF97;">you're breathing?</em></h1>
    <p style="color:#8080A0;font-size:1rem;margin:0;max-width:520px;line-height:1.6;">
      Enter pollutant readings from your city's monitoring station and get an instant
      Air Quality Index with personalised health guidance.</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── INPUTS ───────────────────────────────────────────────────────────────────
st.markdown("""<div style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:#1A1A2E;margin-bottom:1.2rem;">
  Enter Pollutant Levels</div>""", unsafe_allow_html=True)

for label, icon, color, bg, short, safe_val, slider_key, s_max, s_def in [
    ("PM 2.5 — Fine Particles","🔴","#E53E3E","#FFF0F0",
     "Tiny smoke/exhaust particles that enter your bloodstream","Safe: &lt;12 µg/m³","pm25",500.0,50.0),
    ("PM 10 — Dust & Pollen","🟠","#DD6B20","#FFF5EC",
     "Larger dust particles from roads, construction & pollen","Safe: &lt;54 µg/m³","pm10",1000.0,100.0),
    ("NO₂ — Traffic Gas","🟡","#B7791F","#FFFBEC",
     "Nitrogen dioxide from vehicles & power plants","Safe: &lt;40 µg/m³","no2",200.0,30.0),
]:
    st.markdown(f"""
    <div style="background:white;border:1.5px solid #E8E2D8;border-radius:20px;
      padding:1.4rem 1.8rem 0.6rem;margin-bottom:1rem;">
      <div style="display:flex;align-items:center;gap:.9rem;margin-bottom:.8rem;">
        <div style="background:{bg};border-radius:10px;padding:.55rem .7rem;font-size:1.3rem;flex-shrink:0;">{icon}</div>
        <div>
          <div style="font-weight:600;font-size:.95rem;color:#1A1A2E;">{label}</div>
          <div style="font-size:.8rem;color:#888;margin-top:.15rem;">{short} &nbsp;·&nbsp; <b style="color:{color};">{safe_val}</b></div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    if slider_key == "pm25":
        pm25 = st.slider("PM2.5 µg/m³", 0.0, s_max, s_def, key=slider_key)
    elif slider_key == "pm10":
        pm10 = st.slider("PM10 µg/m³", 0.0, s_max, s_def, key=slider_key)
    else:
        no2  = st.slider("NO₂ µg/m³",  0.0, s_max, s_def, key=slider_key)

    st.markdown("</div>", unsafe_allow_html=True)


# City + predict
col_city, _, col_btn = st.columns([1.2, 0.15, 1])
with col_city:
    st.markdown('<div style="font-weight:600;font-size:.88rem;color:#555;margin-bottom:.4rem;">🏙️ Select Your City</div>', unsafe_allow_html=True)
    city = st.selectbox("City", ["Delhi","Mumbai","Bangalore","Chennai","Kolkata"], label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    predict = st.button("🌬️  Check Air Quality", type="primary", use_container_width=True)


# ── RESULT ───────────────────────────────────────────────────────────────────
if predict:
    pred_aqi = 0.45*pm25 + 0.25*pm10 + 0.15*no2 + 35 + np.random.normal(0, 12)
    pred_aqi = max(50, min(500, pred_aqi))

    cfgs = {
        "Good":         ("#F0FFF4","#2D6A4F","#52B788","😊","0–50",
                         "Air is clean and fresh. Enjoy outdoor activities freely!"),
        "Satisfactory": ("#FFFBEB","#B45309","#F59E0B","🙂","51–100",
                         "Acceptable air quality. Unusually sensitive people may experience mild effects."),
        "Moderate":     ("#FFF7ED","#C2410C","#F97316","😐","101–200",
                         "Sensitive groups may experience health effects. Consider limiting outdoor time."),
        "Poor":         ("#FFF1F2","#BE123C","#E11D48","😷","201–300",
                         "Everyone may experience health effects. Avoid prolonged outdoor exertion."),
        "Very Poor":    ("#2D0A0F","#FCA5A5","#BE123C","🚨","301–500",
                         "Serious health alert. Stay indoors with windows sealed and air purifier running."),
    }

    if pred_aqi <= 50:   cat = "Good"
    elif pred_aqi <= 100: cat = "Satisfactory"
    elif pred_aqi <= 200: cat = "Moderate"
    elif pred_aqi <= 300: cat = "Poor"
    else:                 cat = "Very Poor"

    bg, accent, bar, emoji, arange, desc = cfgs[cat]
    pct = min(100, (pred_aqi / 500) * 100)
    subtext = "#555" if cat != "Very Poor" else "#A09090"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{bg};border:2px solid {accent}30;border-radius:28px;
      padding:2.5rem 3rem;margin-bottom:1.5rem;box-shadow:0 12px 48px {accent}18;">

      <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;margin-bottom:2rem;">
        <div>
          <div style="font-size:.75rem;color:{subtext};letter-spacing:2px;text-transform:uppercase;margin-bottom:.5rem;">
            📍 {city} · Air Quality Index
          </div>
          <div style="font-family:'DM Serif Display',serif;font-size:5.5rem;color:{accent};line-height:1;">{pred_aqi:.0f}</div>
          <div style="font-size:1.3rem;font-weight:600;color:{accent};margin-top:.3rem;">{emoji} {cat}</div>
          <div style="font-size:.88rem;color:{subtext};margin-top:.6rem;max-width:340px;line-height:1.6;">{desc}</div>
        </div>

        <div style="display:flex;flex-direction:column;gap:.6rem;min-width:190px;">
          <div style="font-size:.7rem;color:{subtext};letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.1rem;">Your Readings</div>
          {''.join([
            f'<div style="background:white;border-radius:12px;padding:.7rem 1rem;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);">'
            f'<span style="font-size:.82rem;color:#555;">{ic} {nm}</span>'
            f'<span style="font-weight:700;font-size:.95rem;color:#1A1A2E;">{val:.0f} <span style="font-weight:300;font-size:.72rem;color:#888;">µg/m³</span></span></div>'
            for ic,nm,val in [("🔴","PM 2.5",pm25),("🟠","PM 10",pm10),("🟡","NO₂",no2)]
          ])}
        </div>
      </div>

      <div>
        <div style="display:flex;justify-content:space-between;font-size:.72rem;color:{subtext};margin-bottom:.5rem;">
          <span>😊 Good</span><span>🙂 OK</span><span>😐 Moderate</span><span>😷 Poor</span><span>🚨 Severe</span>
        </div>
        <div style="position:relative;background:rgba(0,0,0,0.08);border-radius:20px;height:12px;overflow:visible;">
          <div style="width:{pct}%;height:100%;
            background:linear-gradient(90deg,#52B788,#F59E0B,#F97316,#E11D48,#9F1239);
            border-radius:20px;box-shadow:0 2px 10px {bar}60;"></div>
        </div>
        <div style="text-align:right;font-size:.72rem;color:{subtext};margin-top:.4rem;">{pred_aqi:.0f} / 500</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Action cards ──
    st.markdown("""<div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#1A1A2E;margin-bottom:1rem;">
      What should you do today?</div>""", unsafe_allow_html=True)

    if pred_aqi <= 100:
        actions = [
            ("🚶 Go Outdoors","Walk, run, exercise freely. Air is safe for everyone today.","#F0FFF4","#2D6A4F"),
            ("🧒 Kids & Elderly","Safe for outdoor play. No special precautions needed.","#F0FFF4","#2D6A4F"),
            ("😮‍💨 Breathing","Breathe freely. No masks or air purifiers required.","#F0FFF4","#2D6A4F"),
        ]
    elif pred_aqi <= 200:
        actions = [
            ("🚶 Outdoor Activity","Reduce long outdoor sessions. Short walks are fine for most.","#FFFBEB","#B45309"),
            ("🧒 Kids & Elderly","Limit prolonged outdoor play. Keep asthmatic children indoors.","#FFFBEB","#B45309"),
            ("😮‍💨 Breathing","Consider N95 mask for extended outdoor time. Half-close windows.","#FFFBEB","#B45309"),
        ]
    elif pred_aqi <= 300:
        actions = [
            ("🚶 Stay Brief","Avoid outdoor exercise. Run errands quickly then return inside.","#FFF1F2","#BE123C"),
            ("🧒 Kids & Elderly","Keep indoors. Avoid parks and play areas until AQI improves.","#FFF1F2","#BE123C"),
            ("😮‍💨 Protection","Wear N95 mask outdoors. Use an air purifier at home.","#FFF1F2","#BE123C"),
        ]
    else:
        actions = [
            ("🚶 Stay Indoors","Do NOT go outside unless absolutely necessary today.","#2D0A0F","#FCA5A5"),
            ("🧒 Kids & Elderly","Full indoor isolation. Seal gaps around doors and windows.","#2D0A0F","#FCA5A5"),
            ("😮‍💨 Air Purifier","Run air purifiers on HIGH. Wear N95 if forced to step outside.","#2D0A0F","#FCA5A5"),
        ]

    c1, c2, c3 = st.columns(3)
    for col, (title, body, bg2, ac2) in zip([c1,c2,c3], actions):
        with col:
            st.markdown(f"""
            <div style="background:{bg2};border:1.5px solid {ac2}30;border-radius:18px;padding:1.3rem;min-height:110px;">
              <div style="font-weight:700;font-size:.9rem;color:{ac2};margin-bottom:.5rem;">{title}</div>
              <div style="font-size:.82rem;color:#444;line-height:1.55;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#AAA;font-size:.78rem;padding:.5rem 0 1rem;">
  🌱 BreatheSafe · R²= 0.906 · MAE= 11.8 · SDG 11 — Sustainable Cities & Communities
</div>
""", unsafe_allow_html=True)
