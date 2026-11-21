# Rwanda AI Physics Tutor (Senior 4)

An AI-powered, bilingual (English/Kinyarwanda) tutor for Senior 4 Physics, built for the Rwandan education system. Features strict RAG grounding, page citations, and hint-first pedagogy.

##  Features

- **Hint-First Pedagogy:** Refuses to give final answers, promoting critical thinking.
- **Bilingual:** Ask in Kinyarwanda, get an explanation in Kinyarwanda citing English content.
- **Strict Grounding:** Answers *only* from the provided textbook context and cites the page number.
- **Mobile Ready:** Built as a Progressive Web App (PWA) that can be installed on any Android phone.
- **Anti-Cheating:** Refuses jailbreak attempts and off-topic questions.

##  Architecture

1. **Data:** JSON chunks with `subject`, `topic`, `page` metadata.
2. **Embeddings:** `bge-m3` (multilingual) via `fastembed-cloud` (no local PyTorch required).
3. **Vector DB:** FAISS (local, CPU-friendly).
4. **LLM:** Groq API (`openai/gpt-oss-20b`) for sub-second latency.
5. **Frontend:** Streamlit + PWA.

##  Quick Start (30 Minutes)

### 1. Clone the repository

```bash
git clone https://github.com/YopaNelly/rwanda-ai-tutor.git
cd rwanda-ai-tutor
```

### 2. Set up the environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API keys

Create a `backend/.env` file and add:

```env
GROQ_API_KEY=gsk_your_actual_groq_key_here
```

### 4. Run the app

```bash
streamlit run frontend-web/app.py
```

### 5. Test the RAG pipeline (optional)

```bash
python -m backend.app.rag_pipeline
python backend/tests/red_team.py
```

##  Repository Structure

- `backend/app/`: RAG pipeline, embeddings, and LLM client.
- `backend/data/`: The digitized Physics corpus.
- `backend/prompts/`: The system prompt enforcing hint-first pedagogy.
- `frontend-web/`: The Streamlit application code.
- `evidence/`: Red-team logs, test sets, workplan, and the recommendation memo.

##  License

MIT License
