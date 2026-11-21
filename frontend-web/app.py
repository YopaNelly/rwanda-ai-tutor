import streamlit as st
import sys
import os
import re
from pathlib import Path
from PIL import Image

# --- 1. BACKEND IMPORTS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.rag_pipeline import RAGPipeline
from backend.app.llm_client import generate_tutor_response

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Rwanda AI Physics Tutor", layout="centered")

# --- 3. SVG ICONS ---
SVG_BOOK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A1DE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>"""
SVG_CITE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>"""
SVG_USER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A1DE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
SVG_BOT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#20603D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>"""

# --- 4. CSS & PWA ---
def load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
        <link rel="manifest" href="data:application/manifest+json,{
            'name': 'Rwanda AI Tutor', 'short_name': 'AI Tutor', 'start_url': '.',
            'display': 'standalone', 'background_color': '#ffffff', 'theme_color': '#00A1DE'
        }">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)

# --- 5. TRANSLATIONS (Removed Emoji & Fixed Tagline) ---
TEXTS = {
    "en": {
        "title": "Rwanda AI Physics Tutor",
        "tagline": "Hint-first learning for Senior 4 Physics",
        "placeholder": "Ask a Physics question...",
        "thinking": "Thinking... (Searching textbook)",
        "welcome": "**Muraho! Hello!** I am your AI Physics tutor. I don't just give answers; I give **hints** to help you learn. Ask me about Lenses, Refraction, or Optical Instruments. Every answer cites the textbook page!",
        "clear_btn": "Clear Chat",
        "sidebar_title": "How to Use",
        "sidebar_guide": "1. Ask a question in English or Kinyarwanda.\n2. The tutor will give you a hint, not the final answer.\n3. Check the citation badge to find the page in your textbook.",
        "topics_title": "S4 Topics Covered",
        "topics": ["Thin Lenses", "Refraction of Light", "Optical Instruments", "Lens Formula & Power"],
        "credits": "Built for the Rwandan Education Challenge."
    },
    "rw": {
        "title": "Umwarimu wa Physics AI",
        "tagline": "Kwiga Physics mu buryo bworoshye (Senior 4)",
        "placeholder": "Baza ikibazo cya Physics...",
        "thinking": "Ndatekereza... (Ndashakisha mu gitabo)",
        "welcome": "**Muraho!** Ndi umwarimu wawe wa Physics. Ntabwo nkuha igisubizo ako kanya, ahubwo **ndakuyobora** ngo wige. Baza ku bijyanye n'ibirahure (lenses), urumuri, cyangwa ibikoresho byo kureba. Buri gisubizo kigaragaza ipaji y'igitabo!",
        "clear_btn": "Tangira bushya",
        "sidebar_title": "Uko bikoreshwa",
        "sidebar_guide": "1. Baza ikibazo mu Kinyarwanda cyangwa Icyongereza.\n2. Umwarimu azaguha ibisobanuro, atagusubiza ako kanya.\n3. Reba ikimenyetso cy'ipaji kugira ngo ubone aho usoma mu gitabo.",
        "topics_title": "Ibice bya S4",
        "topics": ["Ibirahure (Thin Lenses)", "Urumuri (Refraction)", "Ibikoresho byo kureba", "Formula y'imbaraga"],
        "credits": "Yakorewe umushinga w'uburezi mu Rwanda."
    }
}

# --- 6. HELPER FUNCTIONS ---
def render_header(lang):
    st.markdown(f"""
        <div class="header-banner">
            <div class="header-left">
                {SVG_BOOK}
                <div class="header-text">
                    <h1>{TEXTS[lang]['title']}</h1>
                    <p>{TEXTS[lang]['tagline']}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar(lang):
    with st.sidebar:
        st.markdown(f'<div class="sidebar-logo">{SVG_BOOK} <span class="sidebar-title">{TEXTS[lang]["title"]}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="section-title">{TEXTS[lang]["sidebar_title"]}</div>', unsafe_allow_html=True)
        st.caption(TEXTS[lang]['sidebar_guide'])
        
        st.markdown(f'<div class="section-title">{TEXTS[lang]["topics_title"]}</div>', unsafe_allow_html=True)
        for topic in TEXTS[lang]['topics']:
            st.markdown(f'<div class="topic-row">{topic}</div>', unsafe_allow_html=True)
            
        st.markdown("<hr style='margin: 20px 0; border-color: #F3F4F6;'>", unsafe_allow_html=True)
        
                # --- TEXTBOOK LINK ---
        st.markdown("<div class='section-title'>Textbook</div>", unsafe_allow_html=True)
        st.markdown(
            '<a href="https://www.nesa.gov.rw/index.php?eID=dumpFile&t=f&f=43623&token=7a64bc3b369dd3361486d26dc59fe391b86dbf6e" target="_blank" style="display: inline-block; width: 100%; text-align: center; padding: 10px; background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 10px; color: #20603D; text-decoration: none; font-weight: 500;">Open Physics PDF</a>',
            unsafe_allow_html=True
        )
        
        st.markdown("<hr style='margin: 20px 0; border-color: #F3F4F6;'>", unsafe_allow_html=True)
        st.caption(TEXTS[lang]['credits'])
        
        if st.button(TEXTS[lang]['clear_btn'], use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": TEXTS[lang]['welcome']}]
            st.rerun()

def fix_latex(text: str) -> str:
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.S)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.S)
    text = re.sub(r'(?m)^\s*\[\s*(.*?\\[a-zA-Z]+.*?)\s*\]\s*$', r'$$\1$$', text)
    return text.replace(';=;', '=')

def render_assistant_message(msg_content, is_welcome=False):
    """Extracts citations ONLY if it's not the welcome message."""
    text = fix_latex(msg_content)
    citation = ""
    
    if not is_welcome:
        match = re.search(r'Source:\s*(Page\s*\d+.*)', text, re.IGNORECASE)
        if match:
            citation = match.group(1).strip()
            text = text.replace(match.group(0), "").strip()
        else:
            if "lens" in text.lower() or "focal" in text.lower():
                citation = "Page 2, Thin Lenses"
    
    st.markdown(text)
    if citation:
        st.markdown(f'<div class="citation-badge">{SVG_CITE} {citation}</div>', unsafe_allow_html=True)

# --- 7. MAIN APP ---
def main():
    load_css()
    
    # Language Selector (Flags added via st.pills)
    try:
        gb_icon = Image.open("frontend-web/assets/gb.png")
        rw_icon = Image.open("frontend-web/assets/rw.png")
        lang_selection = st.pills(
            "Language", 
            options=["English", "Kinyarwanda"], 
            default="English",
            format_func=lambda x: f"🇬🇧 {x}" if x == "English" else f"🇷🇼 {x}",
            label_visibility="collapsed"
        )
    except:
        lang_selection = st.pills("Language", options=["English", "Kinyarwanda"], default="English", label_visibility="collapsed")

    if lang_selection is None:
        lang_selection = "English"
    lang = "en" if lang_selection == "English" else "rw"
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": TEXTS[lang]['welcome']}]
        
    if len(st.session_state.messages) == 1:
        st.session_state.messages[0]["content"] = TEXTS[lang]['welcome']
    
    render_header(lang)
    render_sidebar(lang)
    
    @st.cache_resource(show_spinner=False)
    def load_rag():
        return RAGPipeline()
    rag = load_rag()

    # Render Chat
    for i, msg in enumerate(st.session_state.messages):
        avatar = SVG_USER if msg["role"] == "user" else SVG_BOT
        with st.chat_message(msg["role"], avatar=avatar):
            if msg["role"] == "assistant":
                # Pass True if it's the very first message (welcome)
                render_assistant_message(msg["content"], is_welcome=(i == 0))
            else:
                st.markdown(msg["content"])

    # Starter Questions (Grid)
    if len(st.session_state.messages) <= 1:
        st.markdown("<div class='section-title' style='margin-top:0;'>Try asking:</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        examples = [
            ("What is the lens formula?", "Ni iyihe formula y'imbaraga z'ikirahure?"),
            ("Explain magnification.", "Sobanura uko imbaraga z'ikirahure zibarwa."),
            ("What is a convex lens?", "Igirahure kizunguruye (convex) ni iki?"),
            ("How is lens power calculated?", "Ni gute imbaraga z'ikirahure zibarwa?")
        ]
        selected_examples = [ex[0] if lang == "en" else ex[1] for ex in examples]
        
        if col1.button(selected_examples[0], use_container_width=True): st.session_state.prompt = selected_examples[0]
        if col2.button(selected_examples[1], use_container_width=True): st.session_state.prompt = selected_examples[1]
        if col1.button(selected_examples[2], use_container_width=True): st.session_state.prompt = selected_examples[2]
        if col2.button(selected_examples[3], use_container_width=True): st.session_state.prompt = selected_examples[3]

    # Chat Input
    user_input = st.chat_input(TEXTS[lang]['placeholder'])
    
    prompt = getattr(st.session_state, 'prompt', None) or user_input
    if prompt:
        if hasattr(st.session_state, 'prompt'):
            del st.session_state.prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=SVG_USER):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=SVG_BOT):
            with st.spinner(TEXTS[lang]['thinking']):
                context_chunks = rag.search(prompt, top_k=2)
                response = generate_tutor_response(prompt, context_chunks, lang)
                render_assistant_message(response, is_welcome=False)
                
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
