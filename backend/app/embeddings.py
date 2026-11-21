from fastembed_cloud import CloudTextEmbedding
import numpy as np
import re

# Try the API first
try:
    _model = CloudTextEmbedding(model_name="bge-m3")
    _model.query_embed("test")
    USE_API = True
    print("✅ Using Cloud Embeddings (bge-m3)")
except Exception as e:
    USE_API = False
    print(f"⚠️ Cloud API rate limited. Falling back to local Hash Embeddings.")
    _vocab = {}
    _doc_freq = {}

def _tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def _get_hash_index(token, max_features=1024):
    return hash(token) % max_features

def embed_documents(texts: list[str]) -> list[list[float]]:
    global _doc_freq
    if USE_API:
        return [_model.query_embed(t) for t in texts]
    else:
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
    if USE_API:
        return _model.query_embed(text)
    else:
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
    