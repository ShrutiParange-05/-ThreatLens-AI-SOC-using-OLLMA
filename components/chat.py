import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils.llm_helper import load_model
from utils.pdf_gen import create_pdf
from utils.privacy_guard import PrivacyGuard
from utils.rag_helper import setup_rag_vector_db, query_rag

def render_chat():
    st.markdown("---")
    st.subheader("🤖 AI Security Analyst (Secure & Context-Aware)")

    llm = load_model()
    guard = PrivacyGuard()

    # --- 1. SIDEBAR: KNOWLEDGE BASE ---
    with st.sidebar:
        st.markdown("### 🧠 Analyst Brain")
        privacy_mode = st.toggle("🔒 PII Redaction Mode", value=True)
        st.markdown("---")
        st.markdown("**📚 Knowledge Base**")
        uploaded_file = st.file_uploader("Upload Policy PDF", type="pdf", key="rag_upload")
        
        vector_db = None
        if uploaded_file:
            with st.spinner("Processing Knowledge Base..."):
                if "vector_db" not in st.session_state or st.session_state.get("current_file") != uploaded_file.name:
                    st.session_state.vector_db = setup_rag_vector_db(uploaded_file)
                    st.session_state.current_file = uploaded_file.name
                vector_db = st.session_state.vector_db
            st.success("✅ Knowledge Base Active")
            
            # FILE ANALYSIS BUTTON
            if st.button("📄 Analyze Uploaded File", key="btn_analyze_file"):
                st.session_state.auto_prompt = (
                    f"I have uploaded a document named '{uploaded_file.name}'. "
                    "Please analyze its contents, summarize the key security findings, "
                    "and highlight any critical incidents or policies mentioned."
                )

    # --- 2. INITIALIZE HISTORY ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are CyberSentinel, an expert SOC Analyst. Be concise.")
        ]

    # --- 3. RENDER HISTORY ---
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🛡️"):
                st.markdown(msg.content)

    # --- 4. DETERMINE PROMPT SOURCE ---
    prompt_text = None
    if "auto_prompt" in st.session_state and st.session_state.auto_prompt:
        prompt_text = st.session_state.auto_prompt
        del st.session_state.auto_prompt 
    else:
        prompt_text = st.chat_input("Ask about logs, vulnerabilities, or policies...")

    # --- 5. PROCESS INPUT (The Core Loop) ---
    if prompt_text:
        # A. Display User Message
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt_text)
        st.session_state.messages.append(HumanMessage(content=prompt_text))

        # B. Prepare Context (RAG + Privacy)
        final_prompt = prompt_text
        secrets_found = []

        if privacy_mode:
            final_prompt, secrets_found = guard.sanitize(final_prompt)
            if secrets_found:
                with st.expander("⚠️ Privacy Guard Active"):
                    st.write("**Redacted:**", secrets_found)

        if vector_db:
            context = query_rag(vector_db, final_prompt)
            if context:
                final_prompt = f"""
                [CONTEXT FROM UPLOADED DOCUMENT]
                {context}
                
                [USER QUESTION]
                {final_prompt}
                
                Answer strictly based on the context above.
                """

        # C. Generate AI Response
        with st.chat_message("assistant", avatar="🛡️"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # --- NEW: STATUS INDICATOR (Thinking Accordion) ---
                with st.status("🤖 AI Processing...", expanded=True) as status:
                    st.write("🔍 Analyzing Request...")
                    if privacy_mode: st.write("🔒 Checking Privacy Rules...")
                    if vector_db: st.write("📚 Retrieving Context...")
                    
                    # Temporary swap for RAG context
                    st.session_state.messages[-1] = HumanMessage(content=final_prompt)
                    
                    # CALL LLM
                    response = llm.invoke(st.session_state.messages)
                    full_response = response.content
                    
                    # Restore original message
                    st.session_state.messages[-1] = HumanMessage(content=prompt_text)

                    # Privacy Check on Output
                    if privacy_mode:
                        leaks = guard.check_for_leaks(full_response, secrets_found)
                        if leaks:
                            full_response = "🚨 BLOCKED: AI attempted to leak redacted info."
                    
                    status.update(label="✅ Analysis Complete", state="complete", expanded=False)

                # D. Show Output
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(AIMessage(content=full_response))
                
                # --- NEW: AUTO-SCROLL SCRIPT ---
                st.markdown(
                    """<script>
                    var elements = window.parent.document.querySelectorAll('.stChatMessage');
                    elements[elements.length - 1].scrollIntoView({behavior: 'smooth', block: 'end'});
                    </script>""",
                    unsafe_allow_html=True
                )
                
                # PDF Download Button
                if len(full_response) > 50:
                    pdf_data = create_pdf(prompt_text, full_response)
                    st.download_button(
                        label="📄 Download Report",
                        data=pdf_data,
                        file_name="Incident_Report.pdf",
                        mime="application/pdf",
                        key=f"pdf_{len(st.session_state.messages)}"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
