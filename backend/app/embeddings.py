import numpy as np
import re

_doc_freq = {}

def _tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def _get_hash_index(token, max_features=1024):
    return hash(token) % max_features

def embed_documents(texts: list[str]) -> list[list[float]]:
    global _doc_freq
    embeddings = []
    _doc_freq = {}
    
    for text in texts:
        tokens = set(_tokenize(text))
        for t in tokens:
            _doc_freq[t] = _doc_freq.get(t, 0) + 1
            
    for text in texts:
        vec = np.zeros(1024)
        tokens = _tokenize(text)
        for t in tokens:
            idx = _get_hash_index(t)
            weight = 1.0 / (_doc_freq.get(t, 1) + 1)
            vec[idx] += weight
        
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        embeddings.append(vec.tolist())
        
    return embeddings

def embed_query(text: str) -> list[float]:
    vec = np.zeros(1024)
    tokens = _tokenize(text)
    for t in tokens:
        idx = _get_hash_index(t)
        weight = 1.0 / (_doc_freq.get(t, 1) + 1)
        vec[idx] += weight
        
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()
