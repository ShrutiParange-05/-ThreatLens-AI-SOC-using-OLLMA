import streamlit as st
from langchain_ollama import ChatOllama

# We use cache_resource to keep the connection alive
@st.cache_resource
def load_model():
    """
    Initializes the Ollama model with the settings that worked in the diagnostic test.
    """
    return ChatOllama(
        model="llama3", 
        temperature=0.3,
        # IMPORTANT: This must match your working test script
        base_url="http://127.0.0.1:11434"
    )
