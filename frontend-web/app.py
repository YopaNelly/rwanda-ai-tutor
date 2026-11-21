import streamlit as st
import sys
import os

# Add the backend to path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.rag_pipeline import RAGPipeline
from backend.app.llm_client import generate_tutor_response

# Page config
st.set_page_config(page_title="Rwanda AI Physics Tutor", page_icon="📚")
st.title("📚 Rwanda AI Physics Tutor")
st.caption("Senior 4 Physics | Hint-first tutoring with citations")

# Initialize RAG pipeline (cached so it only loads once)
@st.cache_resource
def load_rag():
    return RAGPipeline()

rag = load_rag()

# Language toggle
lang = st.radio("Choose Language / Hitamo Ururimi:", ("English", "Kinyarwanda"), horizontal=True)
lang_code = "en" if lang == "English" else "rw"

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a Physics question (e.g., What is the lens formula?)"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get RAG context
    with st.spinner("Searching textbook..."):
        context_chunks = rag.search(prompt, top_k=2)
    
    # Get LLM response
    with st.spinner("Tutor is thinking..."):
        response = generate_tutor_response(prompt, context_chunks, lang_code)
    
    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
