import json
import numpy as np
import faiss
from backend.app.embeddings import embed_documents, embed_query
import os

class RAGPipeline:
    def __init__(self, corpus_path="backend/data/processed/physics_corpus.json"):
        # Update the default path to be absolute
        def __init__(self, corpus_path=None):
            if corpus_path is None:
                # Get the directory where this file is located, then go up to root
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                corpus_path = os.path.join(base_dir, "backend", "data", "processed", "physics_corpus.json")

        # 1. Load corpus
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        # 2. Extract texts and metadata
        self.texts = [doc["text"] for doc in self.documents]
        self.metadata = [
            {"subject": d["subject"], "topic": d["topic"], "page": d["page"]} 
            for d in self.documents
        ]
        
        # 3. Build FAISS index
        print("Generating embeddings for corpus...")
        embeddings = embed_documents(self.texts)
        self.dimension = len(embeddings[0])
        
        # Convert to numpy array
        self.embeddings_np = np.array(embeddings).astype('float32')
        
        # Create FAISS index (L2 distance)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings_np)
        print(f"✅ FAISS index built with {self.index.ntotal} documents (Dim: {self.dimension})")

    def search(self, query: str, top_k: int = 2):
        """Search for relevant chunks and return them with metadata."""
        # 1. Embed the query
        query_vector = np.array([embed_query(query)]).astype('float32')
        
        # 2. Search FAISS
        distances, indices = self.index.search(query_vector, top_k)
        
        # 3. Retrieve results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                results.append({
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        return results

# Test the pipeline
if __name__ == "__main__":
    rag = RAGPipeline()
    
    # Test English query
    print("\n--- Test Query 1: English ---")
    query = "What is the lens formula and how is magnification calculated?"
    results = rag.search(query)
    for res in results:
        print(f"Page {res['metadata']['page']} ({res['metadata']['topic']}):")
        print(f"{res['text'][:200]}...\n")
        
    # Test Kinyarwanda query
    print("\n--- Test Query 2: Kinyarwanda ---")
    query_rw = "Ni iyihe formula ikoreshwa mu kubara imbaraga z'ikirahure (lens)?"
    results_rw = rag.search(query_rw)
    for res in results_rw:
        print(f"Page {res['metadata']['page']} ({res['metadata']['topic']}):")
        print(f"{res['text'][:200]}...\n")

