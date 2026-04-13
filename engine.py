import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class LeetCodeSearchEngine:
    def __init__(self, data_path, lexical_path, semantic_path):
        """Initializes and loads all heavy assets into memory."""
        self.df = pd.read_csv(data_path)
        
        with open(lexical_path, "rb") as f:
            self.bm25 = pickle.load(f)
            
        with open(semantic_path, "rb") as f:
            self.embeddings = pickle.load(f)
            
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _get_lexical_ranks(self, query):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        return np.argsort(scores)[::-1]

    def _get_semantic_ranks(self, query):
        query_vec = self.model.encode([query])
        scores = cosine_similarity(query_vec, self.embeddings).flatten()
        return np.argsort(scores)[::-1]

    def search(self, query, n_results=10, k=60):
        """Performs Hybrid RRF Search."""
        lex_ranks = self._get_lexical_ranks(query)
        sem_ranks = self._get_semantic_ranks(query)
        
        rrf_scores = {}
        # Fuse top 50 results
        for rank, idx in enumerate(lex_ranks[:50], 1):
            rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank)
            
        for rank, idx in enumerate(sem_ranks[:50], 1):
            rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank)
            
        sorted_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        return self.df.loc[sorted_indices[:n_results]]