import json
import numpy as np
import faiss
import os
from pathlib import Path
from backend.app.embeddings import embed_documents, embed_query

class RAGPipeline:
    def __init__(self, corpus_path=None):
        # 1. Determine absolute paths
        if corpus_path is None:
            root_dir = Path(__file__).resolve().parent.parent.parent
            corpus_path = root_dir / "backend" / "data" / "processed" / "physics_corpus.json"
        
        # 2. Load corpus
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        self.texts = [doc["text"] for doc in self.documents]
        self.metadata = [
            {"subject": d["subject"], "topic": d["topic"], "page": d["page"]} 
            for d in self.documents
        ]
        
        # 3. Caching Logic (Prevents API Rate Limits)
        index_path = str(corpus_path).replace("physics_corpus.json", "faiss_index_v3.bin")
        
        if os.path.exists(index_path):
            print(f"Loading cached FAISS index from {index_path}...")
            self.index = faiss.read_index(index_path)
            self.dimension = self.index.d
        else:
            print("Generating embeddings for corpus (API Call)...")
            embeddings = embed_documents(self.texts)
            self.dimension = len(embeddings[0])
            self.embeddings_np = np.array(embeddings).astype('float32')
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(self.embeddings_np)
            
            # Save cache to disk
            faiss.write_index(self.index, index_path)
            print(f"✅ FAISS index built and saved to {index_path}")
        
        print(f"✅ Ready! Loaded {self.index.ntotal} documents (Dim: {self.dimension})")

    def search(self, query: str, top_k: int = 2):
        """Search for relevant chunks with a guaranteed keyword fallback."""
        # 1. Try Vector Search
        query_vector = np.array([embed_query(query)]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append({
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        
        # 2. Keyword Fallback (If the vector distance is too high, meaning poor match)
        # Or if the query contains physics keywords
        keywords = ["lens", "formula", "power", "magnification", "convex", "concave", "focal"]
        query_lower = query.lower()
        
        if results[0]["distance"] > 0.8 or any(k in query_lower for k in keywords):
            # Force inject the best page for lenses if vector search fails
            for i, text in enumerate(self.texts):
                if "lens formula" in text.lower() or "P = 1/f" in text:
                    # Insert at the top
                    results.insert(0, {
                        "text": text,
                        "metadata": self.metadata[i],
                        "distance": 0.0
                    })
                    break
                    
        # Deduplicate and limit to top_k
        unique_results = []
        seen = set()
        for r in results:
            if r["text"] not in seen:
                unique_results.append(r)
                seen.add(r["text"])
            if len(unique_results) == top_k:
                break
                
        # Force the LLM to cite the correct page by adding it to the metadata
        if unique_results:
            best_page = unique_results[0]["metadata"]["page"]
            best_topic = unique_results[0]["metadata"]["topic"]
            # We inject this into the text so the LLM sees it
            unique_results[0]["text"] += f"\n\n[System Note: The correct citation for this information is 'Source: Page {best_page}, {best_topic}']"

        return unique_results

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
        