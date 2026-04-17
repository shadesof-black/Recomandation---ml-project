import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_FALLBACK = "https://via.placeholder.com/300x450/1a1a2e/e94560?text=No+Poster"

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================
# STYLES — Dark Cinema Theme
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Root theme */
:root {
    --bg-deep:    #0a0a0f;
    --bg-card:    #12121a;
    --bg-hover:   #1c1c28;
    --accent:     #e94560;
    --accent2:    #f5a623;
    --text-bright:#f0f0f5;
    --text-muted: #8888aa;
    --border:     rgba(255,255,255,0.07);
    --radius:     14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-bright) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Main container */
.block-container {
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 1500px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0e0e18 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-bright) !important; }

/* Title */
h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3.2rem !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, #e94560, #f5a623);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 0 !important;
}

h2, h3 { font-family: 'DM Sans', sans-serif !important; }

/* Section headers */
.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 2px;
    color: var(--accent);
    border-left: 4px solid var(--accent);
    padding-left: 12px;
    margin: 1.5rem 0 1rem;
}

/* Movie cards */
.movie-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    position: relative;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(233,69,96,0.25);
    border-color: var(--accent);
}
.movie-card img { border-radius: var(--radius) var(--radius) 0 0; }

.movie-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-bright);
    padding: 8px 10px 6px;
    line-height: 1.25;
    min-height: 2.6rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Badge */
.badge {
    display: inline-block;
    background: var(--accent);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.badge-gold { background: var(--accent2); color: #111; }

/* Detail card */
.detail-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 32px;
}

/* Pill tags */
.genre-pill {
    display: inline-block;
    background: rgba(233,69,96,0.15);
    border: 1px solid rgba(233,69,96,0.4);
    color: #f0a0b0;
    font-size: 0.75rem;
    padding: 3px 12px;
    border-radius: 20px;
    margin: 3px 3px;
}

/* Inputs */
[data-testid="stTextInput"] input {
    background: #1a1a28 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-bright) !important;
    font-size: 1rem !important;
    padding: 10px 14px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(233,69,96,0.2) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 6px 14px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: #c73550 !important;
}

/* Back button override */
.back-btn > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
}
.back-btn > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #1a1a28 !important;
    border-color: var(--border) !important;
    color: var(--text-bright) !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Muted text */
.muted { color: var(--text-muted); font-size: 0.88rem; }

/* Poster fallback placeholder */
.no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-radius: var(--radius) var(--radius) 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}

/* Stat chips */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-right: 8px;
}
.stat-chip b { color: var(--text-bright); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=60)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def safe_poster(url):
    """Returns url if valid, else None."""
    if url and isinstance(url, str) and url.startswith("http"):
        return url
    return None


def poster_grid(cards, cols=5, key_prefix="grid"):
    if not cards:
        st.markdown("<div class='muted'>No movies to show.</div>", unsafe_allow_html=True)
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1
            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = safe_poster(m.get("poster_url"))

            with colset[c]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                if poster:
                    # FIX: use use_container_width instead of deprecated use_column_width
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        "<div class='no-poster'>🎬</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if tmdb_id:
                    if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}"):
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": safe_poster(tmdb.get("poster_url")),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = safe_poster(m.get("poster_url"))
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [{
        "tmdb_id": x["tmdb_id"],
        "title": x["title"],
        "poster_url": x["poster_url"],
    } for x in final_list[:limit]]

    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown(
        "<div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;"
        "letter-spacing:3px;color:#e94560;padding:10px 0 4px'>🎬 CineMatch</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='muted' style='margin-bottom:16px'>Your personal film guide</div>", unsafe_allow_html=True)

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("<div class='muted' style='font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px'>Browse</div>", unsafe_allow_html=True)

    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<div class='muted' style='font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin:16px 0 8px'>Grid Size</div>", unsafe_allow_html=True)
    grid_cols = st.slider("Columns", 3, 7, 5, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(
        "<div class='muted' style='font-size:0.75rem;line-height:1.6'>"
        "Powered by TMDB & TF-IDF recommendations.<br>Built with ❤️ using Streamlit."
        "</div>",
        unsafe_allow_html=True,
    )

# =============================
# HEADER
# =============================
col_title, col_search = st.columns([1, 2], gap="large")
with col_title:
    st.markdown("<h1>CineMatch</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='muted'>Discover • Explore • Recommend</div>",
        unsafe_allow_html=True,
    )

with col_search:
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    typed = st.text_input(
        "",
        placeholder="🔍  Search: avenger, batman, inception...",
        label_visibility="collapsed",
    )

st.markdown("<hr style='margin:12px 0 20px'>", unsafe_allow_html=True)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.markdown("<div class='muted'>Type at least 2 characters...</div>", unsafe_allow_html=True)
        else:
            with st.spinner("Searching..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels = ["— Pick a movie —"] + [s[0] for s in suggestions]
                    selected = st.selectbox("", labels, index=0, label_visibility="collapsed")
                    if selected != "— Pick a movie —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                if cards:
                    st.markdown(
                        f"<div class='section-label'>Search Results — {len(cards)} found</div>",
                        unsafe_allow_html=True,
                    )
                    poster_grid(cards, cols=grid_cols, key_prefix="search")
                else:
                    st.markdown("<div class='muted'>No results matched your search.</div>", unsafe_allow_html=True)

        st.stop()

    # HOME FEED MODE
    cat_labels = {
        "trending": "🔥 Trending Now",
        "popular": "⭐ Popular",
        "top_rated": "🏆 Top Rated",
        "now_playing": "🎭 Now Playing",
        "upcoming": "🗓 Upcoming",
    }
    st.markdown(
        f"<div class='section-label'>{cat_labels.get(home_category, home_category)}</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})

    if err or not home_cards:
        st.error(f"Could not load feed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
        if st.button("← Back to Home"):
            goto_home()
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # Back button
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop
    if data.get("backdrop_url"):
        st.markdown(
            f"""<div style="width:100%;height:280px;background:linear-gradient(to bottom, transparent 40%, #0a0a0f),
            url('{data['backdrop_url']}') center/cover no-repeat;
            border-radius:16px;margin-bottom:24px;"></div>""",
            unsafe_allow_html=True,
        )

    # Details layout
    left, right = st.columns([1, 2.6], gap="large")

    with left:
        poster = safe_poster(data.get("poster_url"))
        if poster:
            st.image(poster, use_container_width=True)
        else:
            st.markdown(
                "<div class='no-poster' style='border-radius:14px;aspect-ratio:2/3;height:400px'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)

        title = data.get("title", "Unknown Title")
        release = (data.get("release_date") or "")[:4]
        st.markdown(
            f"<div style='font-family:Bebas Neue,sans-serif;font-size:2.4rem;"
            f"letter-spacing:2px;color:#f0f0f5;line-height:1'>{title}"
            f"<span style='color:#8888aa;font-size:1.4rem;margin-left:12px'>({release})</span></div>",
            unsafe_allow_html=True,
        )

        # Stats row
        vote = data.get("vote_average")
        runtime = data.get("runtime")
        lang = data.get("original_language", "").upper()

        stats_html = ""
        if vote:
            stars = "★" * round(vote / 2) + "☆" * (5 - round(vote / 2))
            stats_html += f"<span class='stat-chip'>⭐ <b>{vote:.1f}</b>/10 {stars}</span>"
        if runtime:
            stats_html += f"<span class='stat-chip'>⏱ <b>{runtime} min</b></span>"
        if lang:
            stats_html += f"<span class='stat-chip'>🌐 <b>{lang}</b></span>"
        if stats_html:
            st.markdown(f"<div style='margin:10px 0'>{stats_html}</div>", unsafe_allow_html=True)

        # Genres
        genres = data.get("genres", [])
        if genres:
            pills = "".join([f"<span class='genre-pill'>{g['name']}</span>" for g in genres])
            st.markdown(f"<div style='margin:8px 0 14px'>{pills}</div>", unsafe_allow_html=True)

        st.markdown("<div style='color:#aaa;font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px'>Overview</div>", unsafe_allow_html=True)
        overview = data.get("overview") or "No overview available."
        st.markdown(
            f"<div style='color:#c8c8d8;line-height:1.75;font-size:0.95rem'>{overview}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Recommendations
    st.markdown("<hr style='margin:28px 0 20px'>", unsafe_allow_html=True)

    title_str = (data.get("title") or "").strip()
    if title_str:
        with st.spinner("Finding recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            genre_cards = bundle.get("genre_recommendations", [])

            if tfidf_cards:
                st.markdown(
                    "<div class='section-label'>🔎 Similar Movies (AI Match)</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")

            if genre_cards:
                st.markdown(
                    "<div class='section-label'>🎭 More Like This (Genre)</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="details_genre")

        else:
            st.markdown(
                "<div class='section-label'>🎭 Genre Recommendations</div>",
                unsafe_allow_html=True,
            )
            with st.spinner("Loading genre recommendations..."):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fallback")
            else:
                st.info("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")