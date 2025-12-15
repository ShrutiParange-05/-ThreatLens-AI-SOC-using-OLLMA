# 🛡️ ThreatLens: AI-Powered SOC Analyst Platform

**ThreatLens** is a local, privacy-first Security Operations Center (SOC) dashboard. It integrates real-time threat monitoring with a **Local LLM (Llama 3)** to simulate, detect, and analyze cyberattacks without data leaving the secure environment.


## 🚀 Key Features

### 1. 🧠 Autonomous AI Analyst
- **Local LLM Integration:** Uses **Ollama (Llama 3)** for offline analysis.
- **RAG (Retrieval-Augmented Generation):** Upload security policies (PDF) for context-aware answers.
- **Privacy Guard:** Middleware layer that redacts PII (IPs, Emails) *before* inference.

### 2. 🔴 Red Team Simulator (BAS)
- **Breach & Attack Simulation:** Launch simulated attacks (SQL Injection, DDoS, Ransomware) directly from the UI.
- **Auto-Detection:** The AI Analyst automatically triggers to investigate simulated breaches.

### 3. 📊 Live Threat Intelligence
- **3D Attack Map:** Visualizes threat origins using weighted geopolitical data.
- **Real-time Logs:** Monitors network traffic and endpoint security events.

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **AI/ML:** LangChain, Ollama, FAISS (Vector DB)
- **Visualization:** PyDeck, Plotly
- **Reporting:** FPDF (Automated Incident Reports)

## ⚙️ Installation

1. **Prerequisites:**
   - Install [Ollama](https://ollama.com/)
   - Pull the model: `ollama pull llama3`

2. **Clone the Repo:**
https://github.com/ShrutiParange-05/-ThreatLens-AI-SOC-using-OLLMA
