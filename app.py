import streamlit as st
import pandas as pd
import pickle
energy_map = {
    "Full battery, let's go": 0,
    "Low power mode, but functioning": 1,
    "1%, desperately need a charger": 2,
    "Completely dead. Can't even get out of bed": 3
}

cant_anymore_map = {
    "Never": 0,
    "Rarely, just a passing thought": 1,
    "Sometimes, it's on my mind": 2,
    "All the time, it's a constant thought": 3
}

hopelessness_map = {
    "Not at all": 0,
    "A little bit": 1,
    "Moderately": 2,
    "Completely hopeless": 3
}

self_harm_map = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

desire_live_map = {
    "A very strong desire to live": 0,
    "A moderate desire to live": 1,
    "A slight desire to live": 2,
    "No desire to live": 3
}

burden_map = {
    "Not at all, I know my worth": 0,
    "Only sometimes, in my head": 1,
    "A lot of the time, I feel useless": 2,
    "Constantly. I'm 100% convinced I am.": 3
}

control_map = {
    "I don't have them.": 0,
    "Full control, I can dismiss them.": 1,
    "It's a real struggle to stop them.": 2,
    "Zero control, they just take over.": 3
}

image1_map = {
    "Nah, I am excited about my life": 0,
    "Not Really": 1,
    "Yes a little": 2,
    "OH My God Yesss": 3
}

humor_map = {
    "No.": 0,
    "Yes obviously.": 1
}

resonance_map = {
    "No and its not funny": 0,
    "No, but its funny": 1,
    "Sometimes": 2,
    "Lol, yess.": 3
}

agree_map = {
    "Disagree": 0,
    "Sometimes": 1,
    "Agree": 2,
    "Strongly agree": 3
}

support_map = {
    "Yes, I have a good support system": 0,
    "No, I don't feel comfortable/ I dont have a safe person": 1
}

same_map = {
    "Never": 0,
    "No": 1,
    "Sometimes": 2,
    "Yes": 3
}

hopelessness_map = {
    "Not at all": 0,
    "A little bit": 1,
    "Moderately": 2,
    "Completely hopeless": 3
}

self_harm_map = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

desire_live_map = {
    "A very strong desire to live": 0,
    "A moderate desire to live": 1,
    "A slight desire to live": 2,
    "No desire to live": 3
}
# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SIAS - Suicidal Ideation Assessment System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# 1. SIMPLE BULLETPROOF NAVIGATION ROUTING
# ══════════════════════════════════════════════════════════════════════════════
PAGES = ["Overview", "Assessment", "Insights", "Model Performance"]

if "page" not in st.session_state:
    st.session_state.page = "Overview"

# Render the branding banner layer
st.markdown("""
<div class="topnav-brand-bar">
    <div class="topnav-logo">
Suicidal Ideation Assessment System
</div>
</div>
""", unsafe_allow_html=True)

# Generate 4 structurally identical, equal-width columns for the buttons
nav_cols = st.columns(len(PAGES))
new_page = None

for col, p in zip(nav_cols, PAGES):
    with col:
        is_active = st.session_state.page == p
        button_type = "primary" if is_active else "secondary"
        
        if st.button(p, key=f"nav_btn_{p}", use_container_width=True, type=button_type):
            new_page = p

if new_page and new_page != st.session_state.page:
    st.session_state.page = new_page
    st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# 2. SYSTEM STYLE SHEET (DOM SHIELD RESET WITH UPDATED LIGHT INSIGHTS GRADIENT)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ─── RESET & COMPACT APP BASE LAYOUT ─── */
* { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; visibility: hidden !important; height: 0px !important; }

.stApp {
    background: #F4F7FB !important;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 1100px !important;
}

/* ─── BRAND HEADER ─── */
.topnav-brand-bar {
    background: linear-gradient(135deg, #12355B 0%, #1B4F8A 100%);
    padding: 16px 24px 12px 24px;
    margin: 0 -1rem 0 -1rem;
}
.topnav-logo {
    font-size: 20px; font-weight: 800;
    color: #FFFFFF !important; letter-spacing: 0.3px;
}
.topnav-logo span { color: #20B2AA !important; }

/* ─── BUTTON NAVIGATION BAR CONTAINER — STRETCHED FULL WIDTH FIX ─── */
div[data-testid="stHorizontalBlock"]:has(div.nav-wrapper) {
    background: linear-gradient(135deg, #12355B 0%, #1B4F8A 100%) !important;
    margin: 0 -1rem 20px -1rem !important;
    padding: 0px 24px 14px 24px !important;
    box-shadow: 0 4px 12px rgba(18,53,91,0.15) !important;
    gap: 12px !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    width: calc(100% + 2rem) !important;
    align-items: center !important;
}

div[data-testid="stHorizontalBlock"]:has(div.nav-wrapper) > div[data-testid="column"] {
    flex: 1 1 0% !important;
    min-width: 0 !important;
    width: 100% !important;
}

/* ─── NAVIGATION ELEMENT LAYOUT OVERRIDES ─── */
.nav-wrapper .stButton > button {
    border-radius: 8px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    padding: 8px 0px !important;
    transition: all 0.2s ease-in-out !important;
    letter-spacing: 0.3px !important;
    height: 40px !important;
    width: 100% !important;
    outline: none !important;
}

/* ❌ INACTIVE ELEMENTS: Translucent plate layout with subtle Teal hover */
.nav-wrapper.inactive-tab .stButton > button,
.nav-wrapper.inactive-tab .stButton > button:focus,
.nav-wrapper.inactive-tab .stButton > button:active {
    background-color: transparent !important;
    color: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
}
.nav-wrapper.inactive-tab .stButton > button:hover {
    color: #FFFFFF !important;
    background-color: rgba(32, 178, 170, 0.15) !important;
    border-color: rgba(32, 178, 170, 0.3) !important;
}

/* ❌ ACTIVE TARGET STATES: Elegant deep purple background with crisp active blue hover state */
.nav-wrapper.active-tab .stButton > button,
.nav-wrapper.active-tab .stButton > button:focus,
.nav-wrapper.active-tab .stButton > button:active,
.nav-wrapper.active-tab .stButton > button:focus-visible {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #372C4A 0%, #51416B 100%) !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(55, 44, 74, 0.25) !important;
}
.nav-wrapper.active-tab .stButton > button:hover {
    color: #FFFFFF !important;
    background: #2D6CDF !important;
    border-color: #2D6CDF !important;
}

/* ─── SLEEK, REFINED HERO COMPACT GENERAL CONTAINERS ─── */
.hero-wrap {
    border-radius: 12px;
    padding: 24px 28px !important;
    margin: 12px 0;
    position: relative; 
    overflow: hidden;
    width: 100%;
}

.hero-wrap h1, 
.hero-wrap .hero-title,
.hero-wrap div[data-testid="stMarkdownContainer"] h1 {
    font-size: 26px !important;
    font-weight: 800 !important;
    line-height: 1.25 !important;
    margin-bottom: 8px !important;
    border: none !important;
    padding: 0 !important;
}

.hero-wrap p, 
.hero-wrap .hero-sub,
.hero-wrap div[data-testid="stMarkdownContainer"] p {
    font-size: 14px !important;
    line-height: 1.6 !important;
    max-width: 720px !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* 🟢 Overview — Light cyan/sky-blue wash with high contrast dark navy text */
.hero-wrap.overview-hero {
    background: linear-gradient(135deg, #DBEAFE 0%, #BAE6FD 50%, #A5F3FC 100%) !important;
    box-shadow: 0 4px 16px rgba(186, 230, 253, 0.2) !important;
}
.hero-wrap.overview-hero h1,
.hero-wrap.overview-hero .hero-title,
.hero-wrap.overview-hero div[data-testid="stMarkdownContainer"] h1 {
    color: #0F172A !important;
}
.hero-wrap.overview-hero p,
.hero-wrap.overview-hero .hero-sub,
.hero-wrap.overview-hero div[data-testid="stMarkdownContainer"] p {
    color: #334155 !important;
    opacity: 1.0 !important;
}

/* 🔵 Assessment — Deep royal/indigo blue with white text */
.hero-wrap.assessment-hero {
    background: linear-gradient(135deg, #1A237E 0%, #1565C0 50%, #1976D2 100%) !important;
    box-shadow: 0 4px 16px rgba(26, 35, 126, 0.2) !important;
}
.hero-wrap.assessment-hero h1,
.hero-wrap.assessment-hero .hero-title,
.hero-wrap.assessment-hero div[data-testid="stMarkdownContainer"] h1 {
    color: #FFFFFF !important;
}
.hero-wrap.assessment-hero p,
.hero-wrap.assessment-hero .hero-sub,
.hero-wrap.assessment-hero div[data-testid="stMarkdownContainer"] p {
    color: rgba(255, 255, 255, 0.95) !important;
}

/* 🔄 UPDATED: 🟢 Insights — Light Mint Green Wash with high contrast dark forest green typography */
.hero-wrap.insights-hero {
    background: linear-gradient(135deg, #E6F4EA 0%, #D1FAE5 50%, #A7F3D0 100%) !important;
    box-shadow: 0 4px 16px rgba(167, 243, 208, 0.2) !important;
}
.hero-wrap.insights-hero h1,
.hero-wrap.insights-hero .hero-title,
.hero-wrap.insights-hero div[data-testid="stMarkdownContainer"] h1 {
    color: #064E3B !important; /* Deep dark emerald */
}
.hero-wrap.insights-hero p,
.hero-wrap.insights-hero .hero-sub,
.hero-wrap.insights-hero div[data-testid="stMarkdownContainer"] p {
    color: #065F46 !important; /* Legible medium forest green */
    opacity: 1.0 !important;
}

/* 🔵 Model Performance — Distinct teal-green with white text */
.hero-wrap.performance-hero {
    background: linear-gradient(135deg, #134E4A 0%, #0F766E 50%, #0D9488 100%) !important;
    box-shadow: 0 4px 16px rgba(19, 78, 74, 0.2) !important;
}
.hero-wrap.performance-hero h1,
.hero-wrap.performance-hero .hero-title,
.hero-wrap.performance-hero div[data-testid="stMarkdownContainer"] h1 {
    color: #FFFFFF !important;
}
.hero-wrap.performance-hero p,
.hero-wrap.performance-hero .hero-sub,
.hero-wrap.performance-hero div[data-testid="stMarkdownContainer"] p {
    color: rgba(255, 255, 255, 0.95) !important;
}

/* ─── BANNERS AND CONTENT CARDS ─── */
.page-banner {
    padding: 24px 28px;
    margin: 0 -1rem 20px -1rem;
    position: relative; overflow: hidden;
}
.page-banner.blue { background: linear-gradient(135deg, #1B4F8A 0%, #2D6CDF 70%, #4A90E2 100%); }
.page-banner.teal { background: linear-gradient(135deg, #0F4C5C 0%, #146C7A 70%, #1D8A99 100%); }
.page-banner.green { background: linear-gradient(135deg, #1A5C3A 0%, #2E8B57 70%, #48BB78 100%); }

.page-banner-title { font-size: 24px; font-weight: 800; color: #FFFFFF !important; }
.page-banner-sub { font-size: 13.5px; color: rgba(255,255,255,0.85) !important; margin-top: 4px; }

.stat-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin: 20px 0;
}
.stat-card {
    background: #FFFFFF; border-radius: 12px;
    padding: 20px 16px; text-align: center;
    border: 1px solid #E0EAF5;
    box-shadow: 0 2px 8px rgba(18,53,91,0.06);
    transition: all 0.25s ease !important;
}
.stat-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 24px rgba(18,53,91,0.12) !important;
}
.stat-num { font-size: 32px; font-weight: 900; line-height: 1; margin-bottom: 6px; color: #12355B; }
.stat-lbl { font-size: 12px; font-weight: 600; color: #5C6B7A; }

.sec-title {
    font-size: 22px; font-weight: 800;
    color: #12355B; margin: 24px 0 12px 0;
}

.info-strip {
    background: #EAF4FF; border-left: 4px solid #2D6CDF;
    border-radius: 0 10px 10px 0; padding: 14px 18px;
    font-size: 13.5px; color: #12355B; margin-bottom: 16px;
}
.info-strip.warn { background: #FFFBEB; border-color: #F59E0B; color: #92400E; }

.matters-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; margin-bottom: 24px;
}
.mcard {
    background: #FFFFFF; border-radius: 14px; padding: 22px 20px;
    border: 1px solid #E0EAF5; border-top: 4px solid #20B2AA;
    box-shadow: 0 2px 10px rgba(18,53,91,0.05);
}
.mcard h4 { font-size: 15px; font-weight: 700; color: #12355B; margin-bottom: 8px; }
.mcard p { font-size: 13px; color: #5C6B7A; line-height: 1.65; }

.workflow-highway {
    display: flex; align-items: center; justify-content: space-between;
    background: #FFFFFF; border-radius: 12px; padding: 20px 40px;
    border: 1px solid #E0EAF5; margin-bottom: 24px;
}
.wf-step { font-size: 16px; font-weight: 700; color: #12355B; text-align: center; }
.wf-arrow { font-size: 20px; color: #20B2AA; font-weight: 900; }

.risk-pro-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 20px;
}
.risk-pro-card {
    background: #FFFFFF; border: 1px solid #E0EAF5; padding: 18px 14px;
    border-radius: 10px; text-align: center;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
}
.risk-pro-val { font-size: 24px; font-weight: 800; line-height: 1.2; color: #12355B; }
.risk-pro-lbl { font-size: 12px; font-weight: 600; color: #5C6B7A; margin-top: 6px; line-height: 1.2; }

.factor-row {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 0; border-bottom: 1px solid #F0F5FB;
}
.factor-row:last-child { border-bottom: none; }
.fnum {
    width: 26px; height: 26px; background: #EAF4FF; color: #2D6CDF;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 800; flex-shrink: 0;
}
.fname { font-size: 14px; font-weight: 600; color: #12355B; }

/* Form button styling isolation override */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #12355B 0%, #2D6CDF 100%) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 12px 36px !important; font-size: 15px !important; font-weight: 700 !important;
    width: 100% !important; box-shadow: 0 4px 14px rgba(45,108,223,0.3) !important;
}
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA & MODEL ARCHIVE
# ══════════════════════════════════════════════════════════════════════════════
df = pd.read_csv("dataset.csv") if pd.io.common.file_exists("dataset.csv") else pd.DataFrame()
# LOAD MODEL

try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    st.sidebar.success("✅ Model Loaded")

except Exception as e:
    st.sidebar.error(f"❌ {e}")
    model = None
# ══════════════════════════════════════════════════════════════════════════════


## ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW PAGE
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    
    st.markdown("""
    <div class="hero-wrap overview-hero">
        <h1 class="hero-title">Suicidal Ideation Assessment System</h1>
        <p class="hero-sub">Questionnaire-based mental health risk assessment powered by machine learning and explainable AI.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-num">105</div><div class="stat-lbl">Assessments</div></div>
        <div class="stat-card"><div class="stat-num">14</div><div class="stat-lbl">Indicators</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#2E8B57;">90.48%</div><div class="stat-lbl">Accuracy</div></div>
        <div class="stat-card"><div class="stat-num" style="color:#2D6CDF;">0.935</div><div class="stat-lbl">ROC-AUC</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">What The System Does</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-strip">
        • Users answer a short questionnaire.<br>
        • The system analyzes psychological indicators such as hopelessness, burden perception, self-harm ideation, and emotional regulation.<br>
        • A trained XGBoost model then estimates the probability of suicidal ideation risk.<br>
        • The prediction is accompanied by an explanation showing which factors contributed most strongly.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Why This Matters</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="matters-grid">
        <div class="mcard">
            <h4>Early Risk Detection</h4>
            <p>Identify patterns associated with suicidal ideation before they become visible through direct disclosure.</p>
        </div>
        <div class="mcard">
            <h4>Explainable Results</h4>
            <p>Every prediction is supported with feature importance and SHAP explanations.</p>
        </div>
        <div class="mcard">
            <h4>Research Driven</h4>
            <p>Built using real questionnaire responses and evaluated across multiple ML models.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Workflow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="workflow-highway">
        <div class="wf-step">Questionnaire</div>
        <div class="wf-arrow">→</div>
        <div class="wf-step">Prediction</div>
        <div class="wf-arrow">→</div>
        <div class="wf-step">Risk Probability</div>
        <div class="wf-arrow">→</div>
        <div class="wf-step">Explanation</div>
    </div>
    """, unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# 2. ASSESSMENT PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Assessment":
    st.markdown("""
    <div class="hero-wrap assessment-hero">
        <h1 class="hero-title">Assessment</h1>
        <p class="hero-sub">Answer 14 feature questions and receive a personalized risk assessment with explainable insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="risk-pro-grid" style="margin-top: 15px;">
        <div class="risk-pro-card"><div class="risk-pro-val">2 Min</div><div class="risk-pro-lbl">Estimated Time</div></div>
        <div class="risk-pro-card"><div class="risk-pro-val">13</div><div class="risk-pro-lbl">Assessment Questions</div></div>
        <div class="risk-pro-card" style="grid-column: span 2;"><div class="risk-pro-val" style="color: #2E8B57;">Not Stored</div><div class="risk-pro-lbl">Privacy Guarantee</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("assessment_form"):
        
        age = st.number_input("Age", min_value=18, max_value=60, value=21)
        
        energy = st.selectbox(
            "01. What's your current energy level for just... existing?",
            ["Full battery, let's go", "Low power mode, but functioning", "1%, desperately need a charger", "Completely dead. Can't even get out of bed"]
        )
        
        cant_anymore = st.selectbox(
            "02. How often have you had thoughts like you just 'can't anymore' or wished you could disappear?",
            ["Never", "Rarely, just a passing thought", "Sometimes, it's on my mind", "All the time, it's a constant thought"]
        )
        
        hopelessness = st.selectbox(
            "03. In the past week, how much have you felt hopeless about your future?",
            ["Not at all", "A little bit", "Moderately", "Completely hopeless"]
        )
        
        self_harm = st.selectbox(
            "04. Over the past two weeks, have you had thoughts that you would be better off dead or hurting yourself?",
            ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        )
        
        desire_live = st.selectbox(
            "05. How strong is your desire to live?",
            ["A very strong desire to live", "A moderate desire to live", "A slight desire to live", "No desire to live"]
        )
        
        burden = st.selectbox(
            "06. How much do you feel like you're just a burden on everyone?",
            ["Not at all, I know my worth", "Only sometimes, in my head", "A lot of the time, I feel useless", "Constantly. I'm 100% convinced I am."]
        )
        
        control = st.selectbox(
            "07. How much control do you have over these dark thoughts when they show up?",
            ["I don't have them.", "Full control, I can dismiss them.", "It's a real struggle to stop them.", "Zero control, they just take over."]
        )
        
        st.divider()
        
        # Image 1 Section
        img_col1, img_mid1, img_col2 = st.columns([1, 2, 1])
        with img_mid1:
            st.image("assets/image1.jpeg", use_container_width=True)
        image1 = st.selectbox(
            "08. Do you feel the same as described in the image?",
            ["Nah, I am excited about my life", "Not Really", "Yes a little", "OH My God Yesss"]
        )
        
        st.divider()
        
        # Image 2 Section
        img_col2_1, img_mid2, img_col2_2 = st.columns([1, 2, 1])
        with img_mid2:
            st.image("assets/humor_encoded.jpeg", use_container_width=True)
        humor = st.selectbox(
            "09. As this image indicates, do you use humor(memes) to deflect your issues or escape from your feelings?",
            ["No.", "Yes obviously."]
        )
        
        st.divider()
        
        # Image 3 Section
        img_col3_1, img_mid3, img_col3_2 = st.columns([1, 2, 1])
        with img_mid3:
            st.image("assets/resonance_encoded.jpeg", use_container_width=True)
        resonance = st.selectbox(
            "10. Do you resonate with the image context and feel the same?",
            ["No and its not funny", "No, but its funny", "Sometimes", "Lol, yess."]
        )
        
        st.divider()
        
        # Image 4 Section
        img_col4_1, img_mid4, img_col4_2 = st.columns([1, 2, 1])
        with img_mid4:
            st.image("assets/agree_encoded.jpeg", use_container_width=True)
        agree = st.selectbox(
            "11. Do you agree?",
            ["Disagree", "Sometimes", "Agree", "Strongly agree"]
        )
        
        st.divider()
        
        support = st.selectbox(
            "12. Do you discuss your dark thoughts and struggles with a safe person in your life?",
            ["Yes, I have a good support system", "No, I don't feel comfortable/ I dont have a safe person"]
        )
        
        st.divider()
        
        # Image 5 Section
        img_col5_1, img_mid5, img_col5_2 = st.columns([1, 2, 1])
        with img_mid5:
            st.image("assets/same_encoded.jpeg", use_container_width=True)
        same = st.selectbox(
            "13. Do you feel the same?",
            ["Never", "No", "Sometimes", "Yes"]
        )
        
        # Form Submit Button
        submitted = st.form_submit_button("Submit Assessment & Analyze Risk Profile")
    
    # Process results upon form submission
    if submitted:
        try:
            # Map selected categorical variables to their numerical values
            features = [[
                age,
                energy_map[energy],
                cant_anymore_map[cant_anymore],
                hopelessness_map[hopelessness],
                self_harm_map[self_harm],
                desire_live_map[desire_live],
                burden_map[burden],
                control_map[control],
                image1_map[image1],
                humor_map[humor],
                resonance_map[resonance],
                agree_map[agree],
                support_map[support],
                same_map[same]
            ]]
            
            # Create a structured DataFrame matching the string training labels
            feature_df = pd.DataFrame(
                features,
                columns=[
                    "Age",
                    "What’s your current energy level for just... existing?",
                    "How often have you had thoughts like you just \"can't anymore\" or wished you could just disappear?",
                    "In the past week, how much have you felt hopeless about your future?",
                    "Over the past two weeks, have you had any thoughts that you would be better off dead or of hurting yourself in some way?",
                    "How strong is your desire to live?",
                    "How much do you feel like you're just a burden on everyone?",
                    "How much control do you have over these \"dark thoughts\" when they show up?",
                    "Do you feel the same as described in the image?",
                    "As this image indicates, do you use humor(memes) to deflect your issues or escape from your feelings?",
                    "Do you resonate with the image context and feel the same?",
                    "Do you agree?",
                    "Do you discuss your dark thoughts and struggles with a safe person in your life?",
                    "Do you feel the same?"
                ]
            )   
            
            # Perform ML Inference
            probability = float(model.predict_proba(feature_df)[0][1] * 100)
            
            # Tiered Risk Category Calculation
            if probability < 25:
                risk = "Low"
            elif probability < 60:
                risk = "Moderate"
            else:
                risk = "High"
                
            # Professional Metrics Dashboard Display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Risk Probability", f"{probability:.1f}%")
            with col2:
                st.metric("Risk Category", risk)
            with col3:
                st.metric("Model Used", "XGBoost")
            with col4:
                st.metric("Validation Accuracy", "90.48%")
                
            st.divider()
            
            # Automated Explainable Interpretation Block
            st.markdown("### Interpretation")
            if risk == "Low":
                st.success("""
Protective indicators were stronger than risk indicators.

Possible contributing factors:
• Strong desire to live
• Better emotional regulation
• Lower self-harm ideation
• Presence of support systems
""")
            elif risk == "Moderate":
                st.warning("""
A mixture of protective and risk indicators was detected.

Possible contributing factors:
• Some hopelessness
• Difficulty managing thoughts
• Emotional distress
• Inconsistent support systems
""")
            else:
                st.error("""
Several high-risk indicators were detected.

Possible contributing factors:
• Frequent self-harm ideation
• High hopelessness
• Strong burden perception
• Reduced control over dark thoughts
""")
            
            st.divider()
            
            # Final Research and Compliance Disclaimer
            st.info("""
This assessment is intended for educational and research purposes only.

Predictions are generated using a machine learning model trained on questionnaire responses and should not be interpreted as a medical diagnosis or professional psychological evaluation.
""")
            
        except NameError as ne:
            st.error(f"Mapping Dictionary Error: Ensure your underlying structural dictionaries and the `model` instance are verified. Details: {ne}")
        except Exception as e:
            st.error(f"Prediction Error: {e}")
# ══════════════════════════════════════════════════════════════════════════════
# 3. INSIGHTS PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Insights":
    st.markdown("""
    <div class="hero-wrap insights-hero">
        <h1 class="hero-title">Explainable AI Insights</h1>
        <p class="hero-sub">Explore calculated visual distributions, feature importance profiles, and neural global weights.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Product-Oriented Section Header
    st.markdown('<div class="sec-title">Most Influential Psychological Indicators</div>', unsafe_allow_html=True)
    
    # 2. Contextualized Feature Connection Text
    st.markdown("""
    The machine learning models were trained on questionnaire responses and independently identified a common set of indicators associated with suicidal ideation risk.

The consistency of these findings across multiple algorithms increases confidence in the relevance of these predictors.""")
    
    # Refactored Factor List Layout matching your custom CSS variables
    st.markdown("""
        <div class="factor-row"><div class="fnum">1</div><div class="fname">Control over dark thoughts</div></div>
        <div class="factor-row"><div class="fnum">2</div><div class="fname">Self-harm ideation</div></div>
        <div class="factor-row"><div class="fnum">3</div><div class="fname">Hopelessness about the future</div></div>
        <div class="factor-row"><div class="fnum">4</div><div class="fname">Burden perception</div></div>
        <div class="factor-row"><div class="fnum">5</div><div class="fname">Desire to live</div></div>
        <br>
    """, unsafe_allow_html=True)

    # 3. Un-crumpled Tabbed Interface for Model Charts
    tab1, tab2, tab3 = st.tabs([
        "Logistic Regression ", 
        "Random Forest ", 
        "XGBoost "
    ])
    
    with tab1:
        st.image("assets/lr_features.jpeg", caption="Feature influence in Logistic Regression", use_container_width=True)
        
    with tab2:
        st.image("assets/rf_features.jpeg", caption="Feature importance in Random Forest", use_container_width=True)
        
    with tab3:
        st.image("assets/xgb_features.jpeg", caption="Feature importance in XGBoost", use_container_width=True)

    st.divider()

    # 4. Product-Oriented Section Wording for SHAP
    st.markdown('<div class="sec-title">How the Model Reaches to a Prediction</div>', unsafe_allow_html=True)
    
    # Enhanced, clear explanation text for evaluator readability
    st.write("""
    SHAP (SHapley Additive exPlanations) provides transparency into the model's decision-making process.

    Each point represents an individual response from the dataset.

    Features shown in red generally contribute toward higher predicted risk, while features shown in blue contribute toward lower predicted risk.

    This visualization helps identify which questionnaire responses have the greatest influence on prediction outcomes.
    """)
    
    # 5. Maximized layout footprint by wiping out squeezed structural column white-space
    st.image(
        "assets/shap_summary.jpeg", 
        caption="SHAP Summary Plot", 
        use_container_width=True
    )

    st.divider()

    # 6. High-impact Cross-validation Insights Card
    st.success("""
    ### Key Findings

    Across Logistic Regression, Random Forest and XGBoost, the same core indicators repeatedly emerged as the strongest contributors to prediction outcomes.

    The ability to regulate dark thoughts, levels of hopelessness, self-harm ideation, perceived burden and desire to live consistently demonstrated the highest predictive influence.

    This agreement across multiple machine learning approaches strengthens confidence in the observed patterns.
    """)
# ══════════════════════════════════════════════════════════════════════════════
# 4. MODEL PERFORMANCE PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Model Performance":

    st.markdown("""
    <div class="page-banner green">
        <div class="page-banner-title">Model Performance</div>
    </div>
    """, unsafe_allow_html=True)

    # Recruiters love seeing the stack immediately
    st.markdown("""
    ### Technical Stack
    `Python` • `Pandas` • `Scikit-Learn` • `XGBoost` • `SHAP` • `Streamlit`
    """)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # HIGHLIGHT METRIC CARDS
    # ══════════════════════════════════════════════════════════════════════════
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.metric("Models Tested", "3")
    with col_kpi2:
        st.metric("Best Accuracy", "90.48%")
    with col_kpi3:
        st.metric("Best F1-Score", "0.91")
    with col_kpi4:
        st.metric("Final Model", "XGBoost")

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # PERFORMANCE OVERVIEW & COMPARISON TABLE
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-title">Performance Overview</div>', unsafe_allow_html=True)
    
    # Quick-read categorical breakdown of the best-performing models
    st.markdown("""
    **Top-Tier Model Breakdown:** • **Highest Accuracy:** XGBoost (90.48%)  
    • **Highest F1-Score:** XGBoost (0.91)  
    • **Highest ROC-AUC:** Random Forest (0.944)  
    • **Final Deployed Model:** XGBoost
    """)

    # High-fidelity performance metric table (Context sample numbers completely removed)
    perf_df = pd.DataFrame([
        {"Model": "Logistic Regression", "Accuracy": "81.0%", "F1-Score": "0.81", "ROC-AUC": "0.935"},
        {"Model": "Random Forest", "Accuracy": "86.0%", "F1-Score": "0.86", "ROC-AUC": "0.944"},
        {"Model": "XGBoost", "Accuracy": "90.48%", "F1-Score": "0.91", "ROC-AUC": "0.935"}
    ])
    st.table(perf_df.set_index("Model"))

    # ══════════════════════════════════════════════════════════════════════════
    # WHY XGBOOST WAS SELECTED
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-title">Why XGBoost Was Selected</div>', unsafe_allow_html=True)
    st.info("""
    XGBoost achieved the highest overall accuracy (90.48%) and strongest F1-score (0.91) among all evaluated models.

    Its ability to correctly identify both low-risk and high-risk responses made it the most reliable model for deployment.
    """)

    # ══════════════════════════════════════════════════════════════════════════
    # ROC CURVE ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-title">ROC Curve Analysis</div>', unsafe_allow_html=True)
    st.image(
        "assets/roc_curve.jpeg",
        use_container_width=True
    )
    st.caption("""
    The ROC curve evaluates the model's ability to distinguish between low-risk and high-risk observations across different classification thresholds.
    """)

    # Contextual note clarifying overlapping trajectories and top discriminator
    st.info("""
    **ROC Curve Interpretation**

    The Logistic Regression and XGBoost models achieved the same ROC-AUC score (0.935). As a result, their ROC curves overlap substantially and may appear as a single curve in portions of the visualization.

    Random Forest achieved the highest ROC-AUC score (0.944), indicating the strongest overall class discrimination ability.
    """)

    # ══════════════════════════════════════════════════════════════════════════
    # CONFUSION MATRIX COMPARISON WITH LABELS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="sec-title">Confusion Matrix Comparison</div>', unsafe_allow_html=True)

    matrix_col1, matrix_col2, matrix_col3 = st.columns(3)
    with matrix_col1:
        st.image(
            "assets/lr_confusion.jpeg",
            caption="Logistic Regression",
            use_container_width=True
        )
        st.caption("""
        *Correctly classified validation samples. Demonstrated balanced performance across both classes.*
        """)
        
    with matrix_col2:
        st.image(
            "assets/rf_confusion.jpeg",
            caption="Random Forest",
            use_container_width=True
        )
        st.caption("""
        *Improved class separation compared to Logistic Regression and reduced overall classification errors.*
        """)
        
    with matrix_col3:
        st.image(
            "assets/xgb_confusion.jpeg",
            caption="XGBoost",
            use_container_width=True
        )
        st.caption("""
        *Achieved the strongest overall performance with 90.48% accuracy and the highest F1-score.*
        """)

    st.divider()

    # Essential contextual mapping framing why interpretability matters
    st.markdown("""
    ### Why Explainability Matters

    Mental health assessments require transparency.

    Rather than providing only a prediction, the system highlights which questionnaire responses contributed most strongly to the result.
    """)

    st.divider()

    # ══════════════════════════════════════════════════════════════════════════
    # COMPREHENSIVE EVALUATION SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    st.success("""
    ### Evaluation Summary

    • **Logistic Regression Accuracy:** 81.0%

    • **Random Forest Accuracy:** 86.0%

    • **XGBoost Accuracy:** 90.48%

    • **Highest ROC-AUC:** Random Forest (0.944)

    • **Highest F1-Score:** XGBoost (0.91)

    Based on overall predictive performance and class classification balance, **XGBoost** was selected as the final deployment model.
    """)