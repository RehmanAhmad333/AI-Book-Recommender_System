import streamlit as st
import pandas as pd
import pickle
 

# PAGE CONFIG
st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
 
# LOAD DATA  (cached so it only runs once)
 
@st.cache_resource
def load_data():
    popularity_df    = pickle.load(open("popular.pkl",          "rb"))
    df               = pickle.load(open("df.pkl",               "rb"))
    books_df         = pickle.load(open("books_df.pkl",         "rb"))
    similarity_score = pickle.load(open("similarity_score.pkl", "rb"))
    return popularity_df, df, books_df, similarity_score
 
popularity_df, df, books_df, similarity_score = load_data()
 
# All unique book titles for the dropdown
all_book_titles = ["-- Select a book --"] + sorted(df.index.tolist())
 
# Placeholder / fallback cover image (base64-safe URL)
FALLBACK_IMG = "https://via.placeholder.com/300x400/1a1a4e/FFD93D?text=No+Cover"
 
 
# CSS
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&display=swap');
 
*, *::before, *::after { box-sizing: border-box; }
 
body, .stApp {
    font-family: 'Cormorant Garamond', 'Times New Roman', Georgia, serif;
    background: linear-gradient(135deg, #0a0a2e 0%, #1a1a4e 50%, #16213e 100%);
    background-attachment: fixed;
}
 
/* ── Main container ── */
.main .block-container {
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    border-radius: 28px;
    padding: 1.5rem 2rem 3rem !important;
    margin: 1rem auto !important;
    max-width: 1400px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.1);
}
 
/* ── Typography ── */
h1 {
    text-align: center;
    background: linear-gradient(135deg, #FFD93D, #FF6B6B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-size: clamp(2rem, 6vw, 3.5rem);
    font-weight: 700;
    margin-bottom: 0.4rem;
    letter-spacing: 2px;
}
 
.subtitle {
    text-align: center;
    # color: #b0b8d0;
    font-size: clamp(0.9rem, 3vw, 1.2rem);
    margin-bottom: 2rem;
    font-style: italic;
}
 
.section-header {
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FFD93D, #FFA500);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 1.5rem 0 1rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid rgba(255,217,61,0.3);
    letter-spacing: 1px;
}
 
/* ── Book card ── */
.book-card {
    background: rgba(25,30,50,0.95);
    border-radius: 18px;
    padding: 0.9rem;
    height: 530px;
    display: flex;
    flex-direction: column;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.book-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 32px rgba(0,0,0,0.45);
    border-color: rgba(255,217,61,0.45);
}
 
.book-cover {
    width: 100%;
    height: 400px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    background: #1a1a4e;   /* while image loads */
}
 
.book-title {
    font-weight: 700;
    font-size: 1rem;
    color: #FFD93D;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.book-author {
    font-size: 0.84rem;
    color: #FFD93D;
    font-style: italic;
    margin: 0.25rem 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.book-rating {
    font-size: 0.84rem;
    color: #FFD93D;
    font-weight: 600;
    margin-top: auto;
}
 
/* ── Selectbox (dropdown) ── */
.stSelectbox > div > div {
    background: white !important;
    border-radius: 50px !important;
    border: 2px solid rgba(255,217,61,0.35) !important;
    color: black !important;
}
.stSelectbox label { color: #FFD93D !important; font-weight: 600; }
 
/* ── Number input ── */
.stNumberInput > div > div > input {
    border-radius: 50px !important;
    border: 2px solid rgba(255,217,61,0.35) !important;
    background: white !important;
    color: black !important;
    padding: 12px 20px !important;
}
 
/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.7rem 2rem;
    font-weight: 700;
    font-size: 1rem;
    width: 100%;
    font-family: 'Cormorant Garamond', 'Times New Roman', serif;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.25);
    background: linear-gradient(135deg, #FF5252, #FF6B6B);
}
 
/* ── Alerts ── */
.stAlert {
    background: rgba(255,217,61,0.12) !important;
    border-left: 4px solid #FFD93D !important;
    color: #FFD93D !important;
}
 
/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1.5rem 0;
    border-top: 1px solid rgba(255,255,255,0.1);
    color: #6f7a9e;
    font-size: 0.85rem;
}
 
/* ── Responsive ── */
@media (max-width: 1200px) {
    .book-card  { height: 400px; }
    .book-cover { height: 230px; }
}
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem 2rem !important; }
    .book-card  { height: 360px; }
    .book-cover { height: 200px; }
    .book-title { font-size: 0.85rem; }
    .book-author{ font-size: 0.75rem; }
}
</style>
""", unsafe_allow_html=True)


# HELPER: render a book card safely
def book_card_html(title: str, author: str, cover_url: str, badge: str) -> str:
    """Return the HTML for one book card with a fallback cover on error."""
    safe_title  = (title[:57]  + "…") if len(title)  > 60 else title
    safe_author = (author[:37] + "…") if len(author) > 40 else author
    cover       = cover_url if cover_url else FALLBACK_IMG
    return f"""
    <div class="book-card">
        <img
            src="{cover}"
            class="book-cover"
            alt="{safe_title}"
            onerror="this.onerror=null;this.src='{FALLBACK_IMG}';"
        >
        <div class="book-title">{safe_title}</div>
        <div class="book-author">by {safe_author}</div>
        <div class="book-rating">{badge}</div>
    </div>"""


# HELPER: render books in a 4-column grid
def render_grid(books: list[dict]):
    COLS = 4
    for row_start in range(0, len(books), COLS):
        cols = st.columns(COLS)
        for col_idx, col in enumerate(cols):
            book_idx = row_start + col_idx
            if book_idx < len(books):
                b = books[book_idx]
                with col:
                    st.markdown(
                        book_card_html(b["title"], b["author"], b["cover"], b["badge"]),
                        unsafe_allow_html=True,
                    )


# RECOMMENDATION FUNCTION  (cached per query)
@st.cache_data(show_spinner=False)
def get_recommendations(book_name: str, num_books: int) -> list[dict] | None:
    """Collaborative filtering recommendations using precomputed cosine similarity."""
    if book_name not in df.index:
        return None

    index = df.index.get_loc(book_name)

    # Sort by similarity, skip index 0 (the book itself)
    similar_items = sorted(
        enumerate(similarity_score[index]),
        key=lambda x: x[1],
        reverse=True,
    )[1 : num_books + 1]

    recommendations = []
    for item_idx, sim_score in similar_items:
        book_title = df.index[item_idx]
        similarity = round(sim_score * 100, 2)

        match = books_df[books_df["Book-Title"] == book_title].drop_duplicates("Book-Title")
        if not match.empty:
            row = match.iloc[0]
            recommendations.append({
                "title":  book_title,
                "author": row.get("Book-Author", "Unknown"),
                "cover":  row.get("Image-URL-L", ""),
                "badge":  f"{similarity}% match",
            })

    return recommendations or None


# HEADER

st.markdown("<h1>📚 Book Recommender System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Discover your next favourite read — powered by AI</p>",
    unsafe_allow_html=True,
)


# SECTION 1 — POPULAR BOOKS
st.markdown("<div class='section-header'>🔥 Popular Books</div>", unsafe_allow_html=True)
 
_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    num_popular = st.number_input(
        "How many popular books do you want to see?",
        min_value=5, max_value=50, value=10, step=5,
        help="Select how many top-rated books to display",
    )
 
st.markdown(
    f"<p style='color:#b0b8d0; margin-bottom:1rem;'>"
    f"Top {int(num_popular)} most-rated books loved by the community</p>",
    unsafe_allow_html=True,
)
 
popular_subset = popularity_df.head(int(num_popular))
popular_books  = [
    {
        "title":  row["Book-Title"],
        "author": row["Book-Author"],
        "cover":  row.get("Image-URL-L", ""),
        "badge":  f"{round(row['avg_rating'], 2)} / 10  ({row['num_rating']} ratings)",
    }
    for _, row in popular_subset.iterrows()
]
render_grid(popular_books)
 
 
# SECTION 2 — COLLABORATIVE FILTERING
 
st.markdown(
    "<div class='section-header'>🤖 Personalised Recommendations</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#b0b8d0; margin-bottom:1rem;'>"
    "Find books similar to your favourites using collaborative filtering</p>",
    unsafe_allow_html=True,
)
 
col1, col2, col3 = st.columns([3, 1, 1])
 
with col1:
    # FIX: st.selectbox does NOT accept a 'placeholder' kwarg.
    # A sentinel option is the correct Streamlit pattern.
    book_name = st.selectbox(
        "Select a book",
        options=all_book_titles,
        label_visibility="collapsed",
    )
 
with col2:
    num_recs = st.selectbox(
        "Recommendations",
        options=[1, 2, 5, 10, 15, 20],
        index=2,
        label_visibility="collapsed",
    )
 
with col3:
    search_clicked = st.button("🔍 Find Similar Books", use_container_width=True)
 
# ── Session-state: persist recommendations across reruns ──
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "searched_book" not in st.session_state:
    st.session_state.searched_book = ""
 
if search_clicked:
    # Guard: user hasn't selected a real book
    if book_name == "-- Select a book --":
        st.warning("Please select a book from the dropdown first.")
    else:
        # FIX: use st.spinner (built-in) instead of a manual time.sleep hack
        with st.spinner("🔍 Finding similar books..."):
            recs = get_recommendations(book_name, int(num_recs))
 
        if recs:
            st.session_state.recommendations = recs
            st.session_state.searched_book   = book_name
        else:
            st.session_state.recommendations = None
            st.session_state.searched_book   = book_name
            st.error(f"'{book_name}' was not found in the database. Please try another book.")
 
# ── Display stored recommendations ──
if st.session_state.recommendations:
    st.markdown(
        f"<div class='section-header' style='font-size:1.55rem; margin-top:0;'>"
        f"Similar to &ldquo;{st.session_state.searched_book}&rdquo;</div>",
        unsafe_allow_html=True,
    )
    rec_cards = [
        {
            "title":  r["title"],
            "author": r["author"],
            "cover":  r["cover"],
            "badge":  r["badge"],
        }
        for r in st.session_state.recommendations
    ]
    render_grid(rec_cards)
 
 
# FOOTER
 
st.markdown("""
<div class="footer">
    <p>Built by <strong>Rehman Ahmad Cheema</strong> with 🤗 Streamlit &bull;
       Books Dataset from <em>Book-Crossing</em></p>
    <p>Popularity-Based Filtering + Collaborative Filtering (Cosine Similarity)</p>
</div>
""", unsafe_allow_html=True)
 