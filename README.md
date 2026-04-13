# LeetCode Neural Search Engine

A hybrid search engine for LeetCode problems that fuses **BM25 lexical matching** with **SBERT semantic embeddings** using Reciprocal Rank Fusion (RRF), served through a Streamlit UI.

## How It Works

| Component | Purpose |
|---|---|
| **BM25** | Keyword-level matching for exact problem titles |
| **SBERT** (`all-MiniLM-L6-v2`) | Semantic similarity for conceptual queries |
| **RRF (k=60)** | Fuses both rankings into a single result list |

> Search for concepts like *"multi-source BFS"* or *"sliding window maximum"* and get ranked LeetCode problems with difficulty badges and direct links.

## Project Structure

```
├── app.py              # Streamlit frontend
├── engine.py           # Hybrid search engine (BM25 + SBERT + RRF)
├── reports.py          # Evaluation chart generation
├── data/               # CSV datasets (not tracked)
├── models/             # Pre-built BM25 + embedding pickle files (not tracked)
└── notebooks/          # EDA, data processing, and analysis notebooks
```

## Setup

```bash
# Clone and install dependencies
git clone https://github.com/ComradeV7/Leetcode-Neural-Search-Engine.git
cd Leetcode-Neural-Search-Engine
pip install streamlit pandas numpy scikit-learn sentence-transformers rank-bm25 matplotlib

# Place data & model files
# data/leetcode_final.csv
# models/lexical_model.pkl
# models/semantic_embeddings.pkl

# Run
streamlit run app.py
```

## Performance

| Metric | BM25 | SBERT | Hybrid RRF |
|---|---|---|---|
| MRR | 0.425 | 0.410 | **0.517** |
| Precision@5 | 0.480 | 0.520 | **0.650** |

## Result

<img width="1881" height="903" alt="image" src="https://github.com/user-attachments/assets/453dea14-988b-4c15-b1e9-a8d844958229" />



