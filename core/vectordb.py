import faiss
import numpy as np
from pathlib import Path
import pickle
from typing import List, Tuple, Optional
from core.embeddings import EmbeddingModel

class VectorDB:
    def __init__(self, index_path: str, metadata_path: str, embedding_model: EmbeddingModel):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.embedding_model = embedding_model
        self.index: Optional[faiss.Index] = None
        self.metadata: List[str] = []
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.load()

    def build(self, texts: List[str]):
        embeddings = self.embedding_model.create_embeddings(texts)
        faiss.normalize_L2(embeddings)
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.embedding_model.embedding_dim)
        self.index.add(embeddings.astype(np.float32))
        self.metadata.extend(texts)
        self.save()

    def search(self, query_text: str, k: int = 5) -> List[Tuple[str, float]]:
        if self.index is None: return []
        query_embedding = self.embedding_model.create_embeddings([query_text])
        faiss.normalize_L2(query_embedding)
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)
        return [(self.metadata[i], float(d)) for i, d in zip(indices[0], distances[0]) if i != -1]

    def save(self):
        if self.index:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)

    def load(self):
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)