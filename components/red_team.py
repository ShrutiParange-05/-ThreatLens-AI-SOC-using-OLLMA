import streamlit as st
import time
import random

def render_red_team():
    st.markdown("## 🔴 Red Team Operations Console")
    st.markdown("Execute adversarial simulations to validate SOC detection logic.")
    
    # --- 1. ATTACK CONTROL PANEL ---
    st.markdown("### ⚡ Active Operations")
    
    col1, col2, col3 = st.columns(3)

    # CARD 1: WEB EXPLOITS
    with col1:
        with st.container(border=True):
            st.markdown("### 🌐 Web Exploits")
            st.caption("Target: Web Application Firewall")
            
            st.markdown("**Vector:** `SQL Injection`")
            if st.button("🚀 Inject SQL Payload", key="btn_sqli", use_container_width=True):
                simulate_terminal("Injecting 'UNION SELECT * FROM users'...", "CRITICAL", "SQL Injection")

            st.markdown("**Vector:** `XSS Scripting`")
            if st.button("💉 Inject XSS Payload", key="btn_xss", use_container_width=True):
                simulate_terminal("Injecting '<script>alert(1)</script>'...", "HIGH", "Cross-Site Scripting")

    # CARD 2: NETWORK FLOODS
    with col2:
        with st.container(border=True):
            st.markdown("### 📡 Network Stress")
            st.caption("Target: Load Balancer")
            
            st.markdown("**Vector:** `DDoS SYN Flood`")
            if st.button("🌊 Start SYN Flood", key="btn_ddos", use_container_width=True):
                simulate_terminal("Flooding Port 443 with SYN Packets...", "CRITICAL", "DDoS Flood")
            
            st.markdown("**Vector:** `Port Scan`")
            if st.button("🔍 Run Nmap Scan", key="btn_nmap", use_container_width=True):
                simulate_terminal("Scanning ports 1-65535...", "MEDIUM", "Port Scan")

    # CARD 3: ENDPOINT ATTACKS
    with col3:
        with st.container(border=True):
            st.markdown("### 💀 Endpoint Breaches")
            st.caption("Target: Windows Server 2019")
            
            st.markdown("**Vector:** `Ransomware`")
            if st.button("🔒 Execute WannaCry", key="btn_ransom", use_container_width=True):
                simulate_terminal("Encrypting C:\\System32\\...", "CRITICAL", "Ransomware")
            
            st.markdown("**Vector:** `Privilege Escalation`")
            if st.button("⬆️ Escalation Attack", key="btn_root", use_container_width=True):
                simulate_terminal("Attempting Sudo bypass...", "HIGH", "Privilege Escalation")

    # --- 2. LIVE TERMINAL OUTPUT (Visual Feedback) ---
    st.markdown("---")
    st.subheader("🖥️ Command & Control (C2) Terminal")
    
    if "terminal_logs" not in st.session_state:
        st.session_state.terminal_logs = [">_ System Ready. Waiting for commands..."]

    # Display the terminal window
    terminal_box = st.container(border=True)
    with terminal_box:
        # Show last 5 lines formatted like code
        log_text = "\n".join(st.session_state.terminal_logs[-5:])
        st.code(log_text, language="bash")


def simulate_terminal(command_msg, severity, attack_type):
    """
    1. Updates the fake terminal.
    2. Injects the log into the main dashboard.
    3. Auto-Triggers AI Analyst.
    """
    # A. Visual Feedback (Terminal)
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.terminal_logs.append(f"[{timestamp}] EXEC: {command_msg}")
    st.session_state.terminal_logs.append(f"[{timestamp}] STATUS: Payload Delivered successfully.")
    
    # B. Actual Log Injection (The Logic)
    # Include payload details for better AI analysis
    full_message = f"{attack_type} detected. Payload: {command_msg}"
    
    log_entry = {
        "timestamp": timestamp,
        "severity": severity,
        "message": full_message,
        "source": f"192.168.1.{random.randint(100, 200)}"
    }
    
    if "logs" not in st.session_state:
        st.session_state.logs = []
    
    st.session_state.logs.insert(0, log_entry)

    # --- C. AUTO-TRIGGER AI ANALYSIS ---
    # This sends the prompt to the Chat component automatically
    st.session_state.auto_prompt = f"Analyze this Red Team simulation log: '{full_message}'. Identify the attack vector, assess the severity, and suggest firewall rules to block it."
    
    # D. UI Feedback
    st.toast(f"☠️ Attack Launched: {attack_type}. Switch to 'AI Analyst' tab!", icon="🤖")
    
    # Force refresh to show new terminal logs
    st.rerun()
