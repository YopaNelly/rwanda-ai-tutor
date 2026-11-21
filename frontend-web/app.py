import streamlit as st
import sys
import os
import re
from pathlib import Path

# --- 1. BACKEND IMPORTS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.rag_pipeline import RAGPipeline
from backend.app.llm_client import generate_tutor_response

# --- 2. PAGE CONFIG & PWA ---
st.set_page_config(page_title="Rwanda AI Physics Tutor", page_icon="🇷🇼", layout="centered")

# --- 3. LOAD CUSTOM CSS & PWA MANIFEST ---
def load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Inject PWA Meta Tags
    st.markdown("""
        <link rel="manifest" href="data:application/manifest+json,{
            'name': 'Rwanda AI Tutor',
            'short_name': 'AI Tutor',
            'start_url': '.',
            'display': 'standalone',
            'background_color': '#ffffff',
            'theme_color': '#00A1DE',
            'icons': [{'src': 'https://cdn-icons-png.flaticon.com/512/3663/3663674.png', 'sizes': '512x512', 'type': 'image/png'}]
        }">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)

# --- 4. TRANSLATIONS ---
TEXTS = {
    "en": {
        "title": "Rwanda AI Physics Tutor",
        "tagline": "Hint-first learning for Senior 4 Physics",
        "lang_selector": "🇬🇧 English | 🇷🇼 Kinyarwanda",
        "placeholder": "Ask a Physics question...",
        "thinking": "Thinking... (Searching textbook)",
        "welcome": "👋 **Muraho! Hello!** I am your AI Physics tutor. I don't just give answers; I give **hints** to help you learn. Ask me about Lenses, Refraction, or Optical Instruments. Every answer cites the textbook page!",
        "clear_btn": "🗑️ Clear Chat",
        "sidebar_title": "📖 How to Use",
        "sidebar_guide": "1. Ask a question in English or Kinyarwanda.\n2. The tutor will give you a hint, not the final answer.\n3. Check the citation badge to find the page in your textbook.",
        "topics_title": "📚 S4 Topics Covered",
        "topics": ["Thin Lenses", "Refraction of Light", "Optical Instruments", "Lens Formula & Power"],
        "credits": "Built for the Rwandan Education Challenge."
    },
    "rw": {
        "title": "Umwarimu wa Physics AI",
        "tagline": "Kwiga Physics mu buryo bworoshye (Senior 4)",
        "lang_selector": "🇬🇧 English | 🇷🇼 Kinyarwanda",
        "placeholder": "Baza ikibazo cya Physics...",
        "thinking": "Ndatekereza... (Ndashakisha mu gitabo)",
        "welcome": "👋 **Muraho!** Ndi umwarimu wawe wa Physics. Ntabwo nkuha igisubizo ako kanya, ahubwo **ndakuyobora** ngo wige. Baza ku bijyanye n'ibirahure (lenses), urumuri, cyangwa ibikoresho byo kureba. Buri gisubizo kigaragaza ipaji y'igitabo!",
        "clear_btn": "🗑️ Tangira bushya",
        "sidebar_title": "📖 Uko bikoreshwa",
        "sidebar_guide": "1. Baza ikibazo mu Kinyarwanda cyangwa Icyongereza.\n2. Umwarimu azaguha ibisobanuro, atagusubiza ako kanya.\n3. Reba ikimenyetso cy'ipaji kugira ngo ubone aho usoma mu gitabo.",
        "topics_title": "📚 Ibice bya S4",
        "topics": ["Ibirahure (Thin Lenses)", "Urumuri (Refraction)", "Ibikoresho byo kureba", "Formula y'imbaraga"],
        "credits": "Yakorewe umushinga w'uburezi mu Rwanda."
    }
}

# --- 5. HELPER FUNCTIONS ---
def render_header(lang):
    st.markdown(f"""
        <div class="header-banner">
            <h1>🇷🇼 {TEXTS[lang]['title']}</h1>
            <p>{TEXTS[lang]['tagline']}</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar(lang):
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3663/3663674.png", width=60)
        st.markdown(f"### {TEXTS[lang]['sidebar_title']}")
        st.info(TEXTS[lang]['sidebar_guide'])
        
        st.markdown(f"### {TEXTS[lang]['topics_title']}")
        for topic in TEXTS[lang]['topics']:
            st.markdown(f"- {topic}")
            
        st.markdown("---")
        st.caption(TEXTS[lang]['credits'])
        
        # Clear Chat Button
        if st.button(TEXTS[lang]['clear_btn'], use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": TEXTS[lang]['welcome']}]
            st.rerun()

def format_message_with_citation(text):
    """Extracts the citation from the text and renders it as a HTML badge."""
    # Look for "Source: Page X, Topic"
    match = re.search(r'Source:\s*(Page\s*\d+.*)', text, re.IGNORECASE)
    if match:
        citation = match.group(1).strip()
        # Remove the citation from the main text
        clean_text = text.replace(match.group(0), "").strip()
        # Render text + styled badge
        st.markdown(clean_text)
        st.markdown(f'<div class="citation-badge">📖 {citation}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# --- 6. MAIN APP ---
def main():
    load_css()
    
    # Language Toggle (Top of screen)
    lang_selection = st.radio(
        "", 
        ["English", "Kinyarwanda"], 
        horizontal=True, 
        label_visibility="collapsed"
    )
    lang = "en" if lang_selection == "English" else "rw"
    
    render_header(lang)
    render_sidebar(lang)
    
    # Initialize RAG pipeline
    @st.cache_resource(show_spinner=False)
    def load_rag():
        return RAGPipeline()
    rag = load_rag()

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": TEXTS[lang]['welcome']}]

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                format_message_with_citation(msg["content"])
            else:
                st.markdown(msg["content"])

    # Example Questions (Only show if chat is empty or just the welcome message)
    if len(st.session_state.messages) <= 1:
        st.markdown("##### 💡 Try asking:")
        col1, col2 = st.columns(2)
        examples = [
            ("What is the lens formula?", "Ni iyihe formula y'imbaraga z'ikirahure?"),
            ("Explain magnification.", "Sobanura uko imbaraga z'ikirahure zibarwa."),
            ("What is a convex lens?", "Igirahure kizunguruye (convex) ni iki?"),
            ("How is lens power calculated?", "Ni gute imbaraga z'ikirahure zibarwa?")
        ]
        
        # Pick language-specific examples
        selected_examples = [ex[0] if lang == "en" else ex[1] for ex in examples]
        
        if col1.button(selected_examples[0], use_container_width=True): st.session_state.prompt = selected_examples[0]
        if col2.button(selected_examples[1], use_container_width=True): st.session_state.prompt = selected_examples[1]
        if col1.button(selected_examples[2], use_container_width=True): st.session_state.prompt = selected_examples[2]
        if col2.button(selected_examples[3], use_container_width=True): st.session_state.prompt = selected_examples[3]

    # Chat Input
    user_input = st.chat_input(TEXTS[lang]['placeholder'])
    
    # Handle Example Button Clicks or Chat Input
    prompt = getattr(st.session_state, 'prompt', None) or user_input
    if prompt:
        # Clear the prompt state so it doesn't loop
        if hasattr(st.session_state, 'prompt'):
            del st.session_state.prompt

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner(TEXTS[lang]['thinking']):
                context_chunks = rag.search(prompt, top_k=2)
                response = generate_tutor_response(prompt, context_chunks, lang)
                
                format_message_with_citation(response)
                
        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
    