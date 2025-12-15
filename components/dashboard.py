import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from utils.data_gen import get_attack_stats
from utils.vuln_scanner import get_latest_cves

def render_dashboard():
    """Renders the advanced SOC Dashboard with Live Metrics."""
    
    # --- 1. REALISTIC THREAT DATA (Weighted Simulation) ---
    # Based on major threat intelligence sources
    threat_actors = [
        {"country": "China", "code": "CN", "lat": 35.8617, "lon": 104.1954, "weight": 30, "type": "State-Sponsored Espionage"},
        {"country": "Russia", "code": "RU", "lat": 61.5240, "lon": 105.3188, "weight": 25, "type": "Ransomware / DDoS"},
        {"country": "North Korea", "code": "KP", "lat": 40.3399, "lon": 127.5101, "weight": 15, "type": "Crypto Theft / APT"},
        {"country": "Iran", "code": "IR", "lat": 32.4279, "lon": 53.6880, "weight": 10, "type": "Critical Infra Sabotage"},
        {"country": "Brazil", "code": "BR", "lat": -14.2350, "lon": -51.9253, "weight": 10, "type": "Banking Trojans"},
        {"country": "USA", "code": "US", "lat": 37.0902, "lon": -95.7129, "weight": 5, "type": "Botnet C2 Nodes"},
        {"country": "India", "code": "IN", "lat": 20.5937, "lon": 78.9629, "weight": 5, "type": "Phishing / Scams"}
    ]

    # Initialize State (Runs once per session)
    if "top_threat" not in st.session_state:
        # Weighted choice: China/Russia appear more often than others
        st.session_state.top_threat = random.choices(
            threat_actors, 
            weights=[t['weight'] for t in threat_actors],
            k=1
        )[0]
    
    top_threat = st.session_state.top_threat

    # --- 2. KEY METRICS ROW ---
    st.markdown("### 📡 Global Threat Intelligence")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Global Threat Level", value="CRITICAL", delta="High Activity", delta_color="inverse")
    with col2:
        st.metric(label="Top Attacker Source", value=f"{top_threat['country']}", delta=top_threat['type'], delta_color="off")
    with col3:
        st.metric(label="Active Incidents", value=random.randint(12, 45), delta="+3 this hour")
    with col4:
        st.metric(label="Blocked Requests", value=f"{random.randint(10, 50)}k", delta="Traffic Spike")

    if st.button("🔄 Refresh Intelligence", key="dashboard_refresh_btn"):
        del st.session_state.top_threat
        st.rerun()
    # --- 3. GEO-MAP & ATTACK VECTORS (Side-by-Side) ---
    col_map, col_stats = st.columns([2, 1])
    
    with col_map:
        st.subheader(f"🗺️ Live Attack Feed: {top_threat['country']}")
        
        # GENERATE MAP DATA
        # 70% of attacks come from the "Top Threat" country, 30% are random noise
        map_data = []
        for _ in range(100):
            if random.random() < 0.7:
                # Attack from the top threat country (with slight jitter)
                lat = top_threat['lat'] + np.random.normal(0, 5)
                lon = top_threat['lon'] + np.random.normal(0, 5)
                mtype = top_threat['type']
            else:
                # Random global noise
                lat = random.uniform(-60, 80)
                lon = random.uniform(-180, 180)
                mtype = "Botnet Traffic"
            
            map_data.append({"lat": lat, "lon": lon, "type": mtype, "attacks": random.randint(10, 100)})
        
        df_map = pd.DataFrame(map_data)

        # RENDER PLOTLY MAP (User Friendly)
        fig = px.scatter_geo(
            df_map,
            lat='lat', lon='lon', 
            size='attacks',  # Bubbles change size
            hover_name='type',
            projection="natural earth",
            color='type',
            color_discrete_sequence=["#ff0000", "#00ff41", "#0088ff"], # Red, Green, Blue
            title=f"Live Threat Source: {top_threat['country']}"
        )
        
        # Dark Mode Layout
        fig.update_layout(
            geo=dict(
                bgcolor='rgba(0,0,0,0)', 
                showland=True, landcolor="#1a1c24",
                showocean=True, oceancolor="#0e1117",
                showlakes=False,
                showcoastlines=False
            ),
            margin={"r":0,"t":30,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            font_color="white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        st.subheader("🎯 Top Attack Vectors")
        vectors = pd.DataFrame({
            'Type': ['SQL Injection', 'DDoS', 'Phishing', 'Malware', 'Brute Force'],
            'Count': [450, 300, 210, 150, 90]
        })
        st.dataframe(
            vectors, 
            column_config={
                "Count": st.column_config.ProgressColumn(
                    "Volume",
                    format="%d",
                    min_value=0,
                    max_value=500,
                ),
            },
            hide_index=True,
            use_container_width=True
        )

    # --- 4. TRAFFIC TREND (Line Chart) ---
    st.subheader("📊 Network Anomaly Detection (24h)")
    chart_data = get_attack_stats()
    st.line_chart(
        chart_data.set_index('Hour'), 
        color="#00ff41",  # Hacker Green color
        height=250       
    )

    # --- 5. REAL-TIME VULNERABILITY FEED ---
    st.subheader("🚨 Global Vulnerability Feed (Live CVEs)")
    cves = get_latest_cves()
    
    if cves:
        for i, cve in enumerate(cves):
            cve_id = cve.get('id', f"CVE-Unknown-{i}")
            score = cve.get('score', 'N/A')
            
            with st.expander(f"🔴 {cve_id} (CVSS: {score})"):
                st.write(cve.get('summary', 'No details available.'))
                
                # Unique key for button
                if st.button(f"Analyze {cve_id}", key=f"analyze_{i}"):
                    st.session_state.auto_prompt = f"Analyze vulnerability {cve_id}: {cve.get('summary')}"
    else:
        st.info("⚠️ Vulnerability Feed Offline")
