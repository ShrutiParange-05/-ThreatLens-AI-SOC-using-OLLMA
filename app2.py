import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components.dashboard import render_dashboard
from components.logs import render_log_feed
from components.chat import render_chat
# Import Red Team module (Ensure components/red_team.py exists!)
try:
    from components.red_team import render_red_team
except ImportError:
    def render_red_team():
        st.error("Red Team module not found. Please create components/red_team.py")

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ThreatLens SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL CSS (Cyberpunk/Dark Theme) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #00ff41 !important; font-family: 'Courier New', monospace; }
    div[data-testid="metric-container"] {
        background-color: #1a1c24;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
        color: #fff;
    }
    div.stButton > button {
        background-color: #1a1c24;
        color: #00ff41;
        border: 1px solid #00ff41;
    }
    div.stButton > button:hover {
        background-color: #00ff41;
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("ThreatLens")
    st.caption("SOC Command Center v2.1")
    st.markdown("---")
    
    st.success("🟢 System Online")
    
    # Live Mode Toggle
    is_live = st.toggle("🔴 Live Data Feed", value=False)
    
    if is_live:
        st.caption("⚠️ Refreshes every 5s")
        st_autorefresh(interval=5000, key="data_refresh")

    st.markdown("---")
    st.markdown("### 📡 Live Sensors")
    st.checkbox("Network Traffic", value=True)
    st.checkbox("Endpoint Logs", value=True)
    st.checkbox("Global Threat Map", value=True)

# --- 4. MAIN LAYOUT (TABS ONLY) ---
st.title("🛡️ ThreatLens: Command Center")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔴 Red Team Simulator", "🤖 AI Analyst"])

# TAB 1: Dashboard & Logs
with tab1:
    render_dashboard()
    st.markdown("---")
    render_log_feed()

# TAB 2: Red Team Attack Sim
with tab2:
    render_red_team()

# TAB 3: AI Chat & RAG
with tab3:
    render_chat()
