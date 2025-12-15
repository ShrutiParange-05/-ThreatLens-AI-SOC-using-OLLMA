import streamlit as st
from utils.data_gen import get_dummy_logs

def render_log_feed():
    """Renders the scrolling log feed and interaction buttons."""
    
    st.subheader("📟 Real-Time Log Ingestion")
    
    logs = get_dummy_logs()
    
    # Create a visual box for logs
    log_html = "<div style='height: 150px; overflow-y: scroll; background-color: #000; color: #00ff41; padding: 10px; font-family: monospace; border: 1px solid #333;'>"
    for log in logs:
        log_html += f"<div>{log}</div>"
    log_html += "</div>"
    
    st.markdown(log_html, unsafe_allow_html=True)
    
    st.caption("Select a critical log to generate an incident report:")
    
    # Create buttons for specific incidents
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 Analyze SQL Injection"):
            st.session_state.auto_prompt = "Analyze this log: '[12:02:10] CRIT: SQL Injection attempt on /login'. Create an Incident Report."
    
    with col2:
        if st.button("🦠 Analyze Malware Alert"):
            st.session_state.auto_prompt = "Analyze this log: '[12:05:01] CRIT: Malware signature 'Emotet' detected'. Recommend remediation steps."
