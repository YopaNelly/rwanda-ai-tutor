import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load env variables
load_dotenv("backend/.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_tutor_response(query: str, context_chunks: list, lang: str = "en") -> str:
    """Calls Groq API with the retrieved context."""
    
    # 1. Format the retrieved context
    context_text = ""
    for chunk in context_chunks:
        meta = chunk["metadata"]
        context_text += f"[Page {meta['page']} - {meta['topic']}]: {chunk['text']}\n\n"
    
    # 2. Get absolute path to the prompt
    root_dir = Path(__file__).resolve().parent.parent.parent
    prompt_path = root_dir / "backend" / "prompts" / "tutor_system.txt"
    
    # 3. Load system prompt
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    # 4. Build the user prompt (THIS WAS MISSING)
    user_prompt = f"Context:\n{context_text}\n\nStudent Question ({lang}): {query}"
    
    # 5. Build API request
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-20b", # Using the working model
         "messages": [
            {"role": "system", "content": system_prompt + "\n\nCRITICAL: At the end of your answer, you MUST include the exact citation provided in the Context (e.g., 'Source: Page X, Topic'). Do not make up a page number."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    # 6. Make request
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
    