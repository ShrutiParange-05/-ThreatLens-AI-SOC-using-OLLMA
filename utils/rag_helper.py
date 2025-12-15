import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

@st.cache_resource
def setup_rag_vector_db(uploaded_file):
    """
    1. Reads the uploaded PDF.
    2. Splits it into chunks.
    3. Converts chunks to Vectors (Embeddings).
    4. Stores them in a local FAISS index.
    """
    # Save file temporarily
    with open("temp_policy.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load & Split
    loader = PyPDFLoader("temp_policy.pdf")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)

    # Embed & Index (Using Ollama's Llama3 for embeddings too!)
    embeddings = OllamaEmbeddings(model="llama3")
    vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    return vector_store

def query_rag(vector_store, question):
    """
    Finds the most relevant chunks in the PDF for the user's question.
    """
    # Search for top 3 relevant chunks
    docs = vector_store.similarity_search(question, k=3)
    
    # Combine content
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

