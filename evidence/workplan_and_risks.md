# Workplan, Risks, and Cuts (Phase 1)

## 10-Day Workplan
- **Days 1-2:** Data extraction (OCR failed due to network limits), pivoted to manual JSON corpus creation of NESA/REB Physics content.
- **Days 3-4:** Built RAG pipeline, integrated `bge-m3` embeddings via `fastembed-cloud`.
- **Days 5-6:** Integrated Groq LLM (`gpt-oss-20b`), engineered the "Hint-First" system prompt, built the Streamlit web app.
- **Days 7-8:** Red-teaming (25 prompts), patched jailbreak vulnerabilities, tested Kinyarwanda/English bilingual retrieval.
- **Days 9-10:** PWA mobile configuration, wrote recommendation memo, finalized GitHub repository for handover.

## The "2-Day Cut" Plan
If two days were lost due to network failures, we would cut the Mobile PWA deployment and reduce the red-team tests from 25 to 10. The core web app and bilingual RAG pipeline would remain intact.

## Risk Register (Minors in AI Tutoring)
| Risk | Description | Mitigation |
| :--- | :--- | :--- |
| **Privacy** | Minors' data being leaked or stored improperly. | The Streamlit app uses session-only memory (`st.session_state`). No chat logs are saved to a database. No PII is collected. |
| **Bias** | The AI hallucinates or provides incorrect Rwandan curriculum answers. | Strict RAG grounding. The prompt forces the AI to answer *only* from the provided context and cite the page number. If the answer is missing, it says "Ntabwo mbona ibi mu gitabo". |
| **Over-reliance** | Students use the AI to do their homework without learning. | The AI is "Hint-First". It refuses to give the final numerical answer, instead guiding the student to use the formula. |
| **Cheating** | Students use the AI during exams. | The app is a PWA (browser-based). Schools can block it on exam networks. Furthermore, the AI refuses to solve NESA exam questions directly. |
