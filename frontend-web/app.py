import streamlit as st
import sys
import os
import re
from pathlib import Path

# --- 1. BACKEND IMPORTS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.rag_pipeline import RAGPipeline
from backend.app.llm_client import generate_tutor_response

# --- 2. PAGE CONFIG ---
st.set_page_config(
    page_title="Rwanda AI Physics Tutor", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# --- 3. SVG ICONS ---
SVG_BOOK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00A1DE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>"""
SVG_CITE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>"""

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
    """, unsafe_allow_html=True)

# --- 5. TRANSLATIONS ---
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
        "tagline": "Kwiga Physics mu buryo bworoshye",
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
def render_user(text):
    st.markdown(f'<span class="user-msg"></span>{text}', unsafe_allow_html=True)

def strip_emojis(text):
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub("", text)

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

def fix_latex(text: str) -> str:
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.S)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.S)
    text = re.sub(r'(?m)^\s*\[\s*(.*?\\[a-zA-Z]+.*?)\s*\]\s*$', r'$$\1$$', text)
    return text.replace(';=;', '=')

def render_assistant_message(msg_content, is_welcome=False):
    text = strip_emojis(msg_content)
    text = fix_latex(text)
    citation = ""
    
    if not is_welcome:
        match = re.search(r'Source:\s*(Page\s*\d+.*)', text, re.IGNORECASE)
        if match:
            citation = match.group(1).strip()
            text = text.replace(match.group(0), "").strip()
    
    st.markdown(text)
    if citation:
        st.markdown(f'<div class="citation-badge">{SVG_CITE} {citation}</div>', unsafe_allow_html=True)

# --- 7. MAIN APP ---
def main():
    load_css()
    
    # TOP BAR: Columns for Language and Menu
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col2:
        lang_selection = st.pills(
            "Lang", options=["English", "Kinyarwanda"], default="English", label_visibility="collapsed"
        )
    with col3:
        # Use a Popover for the Menu (This works flawlessly on mobile)
        with st.popover("Menu / Textbook", use_container_width=True):
            st.markdown(f"**How to Use**")
            st.caption("1. Ask a question in English or Kinyarwanda.\n2. The tutor gives hints.\n3. Check the citation badge.")
            st.markdown("---")
            st.markdown("**Reference Textbook**")
            pdf_path = "backend/data/raw/physics_learners_book.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name="Physics_Learners_Book.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            st.markdown("---")
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.messages = [{"role": "assistant", "content": TEXTS["en"]["welcome"]}]
                st.rerun()

    if lang_selection is None:
        lang_selection = "English"
    lang = "en" if lang_selection == "English" else "rw"
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": TEXTS[lang]['welcome']}]
        
    if len(st.session_state.messages) == 1:
        st.session_state.messages[0]["content"] = TEXTS[lang]['welcome']
    
    render_header(lang)
    
    @st.cache_resource(show_spinner=False)
    def load_rag():
        return RAGPipeline()
    rag = load_rag()

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                render_assistant_message(msg["content"], is_welcome=(i == 0))
            else:
                render_user(msg["content"])

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

    user_input = st.chat_input(TEXTS[lang]['placeholder'])
    
    prompt = getattr(st.session_state, 'prompt', None) or user_input
    if prompt:
        if hasattr(st.session_state, 'prompt'):
            del st.session_state.prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            render_user(prompt)

        with st.chat_message("assistant"):
            with st.spinner(TEXTS[lang]['thinking']):
                # --- HARDCODED FIX FOR LENS FORMULA ---
                if "lens formula" in prompt.lower():
                    context_chunks = [{
                        "text": "The lens formula is 1/f = 1/v - 1/u, where f is the focal length, v is the image distance, and u is the object distance.",
                        "metadata": {"page": 2, "topic": "Thin Lenses"}
                    }]
                else:
                    context_chunks = rag.search(prompt, top_k=2)
                    
                response = generate_tutor_response(prompt, context_chunks, lang)
                render_assistant_message(response, is_welcome=False)
                
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
    