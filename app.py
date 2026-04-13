import streamlit as st
from engine import LeetCodeSearchEngine

# --- 1. CONFIG ---
st.set_page_config(page_title="Leetcode Search Engine", layout="wide", page_icon="")

@st.cache_resource
def init_engine():
    return LeetCodeSearchEngine(
        data_path="data/leetcode_final.csv",
        lexical_path="models/lexical_model.pkl",
        semantic_path="models/semantic_embeddings.pkl"
    )

search_engine = init_engine()

# --- 2. ADVANCED STYLING (The "Beauty" Logic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d1117;
    }

    .result-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(10px);
        padding: 8px 14px;      /* Tighter internal spacing */
        border-radius: 8px;     /* Sharper corners for small boxes */
        border: 1px solid #30363d;
        margin-bottom: 8px;     /* Less gap between cards */
        transition: all 0.2s ease-in-out;
    }

    .result-card:hover {
        border-color: #58a6ff;
        transform: translateX(4px); /* Subtle shift instead of lift */
    }

    /* Small Problem Title */
    .problem-title {
        margin: 4px 0px !important;
        color: #f0f6fc;
        font-size: 1.05rem;     /* Smaller text */
        font-weight: 600;
    }

    .badge {
        padding: 2px 8px;       /* Slimmer badges */
        border-radius: 4px;
        font-size: 0.65rem;     /* Tiny font for metadata */
        font-weight: 700;
        text-transform: uppercase;
    }
    .Easy { background: rgba(45, 181, 93, 0.1); color: #2db55d; border: 1px solid rgba(45, 181, 93, 0.3); }
    .Medium { background: rgba(255, 184, 0, 0.1); color: #ffb800; border: 1px solid rgba(255, 184, 0, 0.3); }
    .Hard { background: rgba(239, 71, 67, 0.1); color: #ef4743; border: 1px solid rgba(239, 71, 67, 0.3); }

    .topic-tag {
        display: inline-block;
        background: #21262d;
        color: #8b949e;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.7rem;       /* Reduced from 0.8 */
        margin-right: 4px;
        margin-top: 4px;
        border: 1px solid #30363d;
    }

    .solve-btn {
        display: inline-block;
        margin-top: 8px;         /* Reduced from 15px */
        color: #58a6ff;
        text-decoration: none;
        font-size: 0.85rem;      /* Smaller button text */
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. UI LAYOUT ---

# Hero Header
st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0rem;">
        <h1 style="
            background: linear-gradient(90deg, #58a6ff, #bc8cff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        ">LeetCode Neural Search</h1>
        <p style="
            color: #8b949e;
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        ">
            Find LeetCode problems mapped to your choice of 
            <b style="color: #f0f6fc;">patterns</b>, 
            <b style="color: #f0f6fc;">logic</b>, and 
            <b style="color: #f0f6fc;">approaches</b>.
        </p>
    </div>
""", unsafe_allow_html=True)

# Main Search Row
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    query = st.text_input("Search Problems", placeholder="Search concepts like 'Multi-source BFS' or 'finding shortest path'...", label_visibility="collapsed")

# Sidebar Filters
st.sidebar.markdown("### Controls")
diff_filter = st.sidebar.multiselect("Difficulty", ["Easy", "Medium", "Hard"], default=["Easy", "Medium", "Hard"])
top_n = st.sidebar.slider("Show Top Results", 5, 20, 10)

if query:
    results = search_engine.search(query, n_results=top_n)
    results = results[results['difficulty'].isin(diff_filter)]
    
    if not results.empty:
        for _, row in results.iterrows():
            topic_html = "".join([f'<span class="topic-tag">{t.strip()}</span>' for t in str(row['Topics']).split(',')])
            
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge {row['difficulty']}">{row['difficulty']}</span>
                    <span style="color: #484f58; font-size: 0.75rem;">ID: {row['ID']}</span>
                </div>
                <div class="problem-title">{row['title']}</div>
                <div>{topic_html}</div>
                <a class="solve-btn" href="{row['Link']}" target="_blank">Solve ↗</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center; padding: 50px; color: #8b949e;'>No results found. Try a broader search term!</div>", unsafe_allow_html=True)
