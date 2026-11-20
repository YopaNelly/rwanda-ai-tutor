"""Embedding layer using fastembed-cloud (bge-m3, 1024 dims).
No PyTorch required. Free tier with auto-provisioned key.
"""
from fastembed_cloud import CloudTextEmbedding

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = CloudTextEmbedding(model_name="bge-m3")
    return _model

def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a list of document chunks."""
    model = _get_model()
    return [model.query_embed(t) for t in texts]

def embed_query(text: str) -> list[float]:
    """Embed a single query."""
    return _get_model().query_embed(text)
