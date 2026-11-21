import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_tutor_response(query: str, context_chunks: list, lang: str = "en") -> str:
    """Calls Groq API with the retrieved context."""
    
    # Format the retrieved context
    context_text = ""
    for chunk in context_chunks:
        meta = chunk["metadata"]
        context_text += f"[Page {meta['page']} - {meta['topic']}]: {chunk['text']}\n\n"
    
    # Load system prompt
    with open("backend/prompts/tutor_system.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # Build the message
    user_prompt = f"Context:\n{context_text}\n\nStudent Question ({lang}): {query}"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"API Error: {response.text}"
