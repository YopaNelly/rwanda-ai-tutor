import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
token = os.getenv("HF_TOKEN")

# Replace with a model supported by hf-inference
API_URL = "https://router.huggingface.co/hf-inference/models/perplexity-ai/pplx-embed-v2-late-0.6b"

r = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {token}"},
    json={"inputs": ["Mbura y'ibara ry'umuhondo"], "options": {"wait_for_model": True}},
    timeout=120,
)

print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Dim:", len(data[0]) if isinstance(data[0], list) else "check format:", str(data)[:200])
else:
    print("Error:", r.text[:500])
    