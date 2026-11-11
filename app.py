"""
RecomAI – Smart Recommendation System
A modern AI-powered multi-domain recommendation platform built with Python,
Streamlit, and Machine Learning using Singular Value Decomposition (SVD).

Domains:
- 🎬 Movies (Action, Comedy, Romance, Thriller, Sci-Fi)
- 🎵 Music (Melody, Pop, Hip-Hop, Classical, Rock)
- 🛍️ Shopping (Electronics, Fashion, Accessories, Home Appliances)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Local application modules
from src.styles import get_custom_css
from src.data_loader import (
    load_catalogs,
    load_base_ratings,
    get_active_ratings,
    add_user_rating,
    get_user_rated_items,
    USER_PROFILES
)
from src.svd_engine import SVDEngine
from src.ui_components import (
    render_hero_banner,
    render_stats_row,
    render_movie_card,
    render_music_card,
    render_product_card,
    get_badge_html
)

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RecomAI – Smart Recommendation System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS theme (Dark navy & purple gradient theme)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "active_user" not in st.session_state:
    st.session_state["active_user"] = "User_1"

if "user_ratings_override" not in st.session_state:
    st.session_state["user_ratings_override"] = {"movies": [], "music": [], "shopping": []}

if "k_factors" not in st.session_state:
    st.session_state["k_factors"] = 3

if "cart_count" not in st.session_state:
    st.session_state["cart_count"] = 0

# -----------------------------------------------------------------------------
# 3. DATA & MODEL CACHING HELPERS
# -----------------------------------------------------------------------------
movies_df, music_df, products_df = load_catalogs()

def get_fitted_svd_engine(category: str, k: int) -> SVDEngine:
    """Instantiate and train SVD engine for the selected category."""
    ratings = get_active_ratings(category)
    if category == "movies":
        catalog = movies_df
    elif category == "music":
        catalog = music_df
    else:
        catalog = products_df

    engine = SVDEngine(k_factors=k)
    engine.fit(ratings, catalog)
    return engine

def handle_user_rating(category: str, item_id: str, rating_val: float):
    """Callback when user submits a rating."""
    user = st.session_state["active_user"]
    add_user_rating(category, user, item_id, rating_val)
    st.toast(f"✅ Rated {item_id} with {rating_val}★! SVD model updated.", icon="⭐")
    st.rerun()

# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & PROFILE CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom: 1.25rem;">
        <div style="background: linear-gradient(135deg, #8b5cf6, #ec4899); width: 44px; height: 44px; border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size: 24px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);">
            ⚡
        </div>
        <div>
            <h2 style="margin:0; font-size: 1.4rem; color: #fff; font-weight:800; letter-spacing: -0.02em;">RecomAI</h2>
            <p style="margin:0; font-size: 0.72rem; color: #a78bfa; font-weight:600; text-transform:uppercase; letter-spacing: 0.05em;">SVD Machine Learning</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; opacity: 0.2;'/>", unsafe_allow_html=True)

    # Page Navigation
    nav_selection = st.radio(
        "Navigation Menu",
        options=[
            "🏠 Home",
            "🎬 Movies",
            "🎵 Music",
            "🛍️ Shopping",
            "🌟 My Recommendations",
            "🔬 SVD Analysis",
            "ℹ️ About Project"
        ],
        index=0
    )

    st.markdown("<hr style='margin: 1.25rem 0; opacity: 0.2;'/>", unsafe_allow_html=True)

    # Active User Profile Selector
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#e2e8f0; margin-bottom:4px;'>👤 ACTIVE USER PROFILE</p>", unsafe_allow_html=True)
    profile_options = list(USER_PROFILES.keys())
    
    def format_user_label(uid):
        p = USER_PROFILES[uid]
        return f"{p['avatar']} {p['name']} ({uid})"

    selected_user = st.selectbox(
        "Select User Persona:",
        options=profile_options,
        index=profile_options.index(st.session_state["active_user"]),
        format_func=format_user_label
    )
    if selected_user != st.session_state["active_user"]:
        st.session_state["active_user"] = selected_user
        st.rerun()

    # Active Profile Card Info
    curr_profile = USER_PROFILES[selected_user]
    total_active_ratings = (
        len(get_user_rated_items("movies", selected_user)) +
        len(get_user_rated_items("music", selected_user)) +
        len(get_user_rated_items("shopping", selected_user))
    )

    st.markdown(f"""
    <div style="background: rgba(22, 18, 54, 0.75); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 12px; margin-top: 8px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <b style="color: {curr_profile['color']}; font-size: 0.95rem;">{curr_profile['avatar']} {curr_profile['name']}</b>
            <span style="font-size: 0.7rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; color:#cbd5e1;">{selected_user}</span>
        </div>
        <p style="font-size: 0.75rem; color: #94a3b8; margin: 6px 0 8px 0; line-height: 1.4;">
            {curr_profile['tagline']}
        </p>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.75rem; color: #34d399; font-weight: 600;">
            <span>Rated Items: {total_active_ratings}</span>
            <span style="color:#c084fc;">Active Mode</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SVD Latent Rank Slider in Sidebar
    st.markdown("<hr style='margin: 1.25rem 0; opacity: 0.2;'/>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; font-weight:700; color:#e2e8f0; margin-bottom:4px;'>⚙️ SVD LATENT DIMENSIONS (k)</p>", unsafe_allow_html=True)
    k_slider = st.slider(
        "Latent Factors (k):",
        min_value=1,
        max_value=6,
        value=st.session_state["k_factors"],
        help="Number of singular vectors retained for matrix decomposition."
    )
    if k_slider != st.session_state["k_factors"]:
        st.session_state["k_factors"] = k_slider
        st.rerun()

    # Reset ratings button
    if st.button("🔄 Reset Custom Ratings", use_container_width=True):
        st.session_state["user_ratings_override"] = {"movies": [], "music": [], "shopping": []}
        st.toast("Restored baseline sample ratings!", icon="🔄")
        st.rerun()


# -----------------------------------------------------------------------------
# 5. PAGE: HOME
# -----------------------------------------------------------------------------
def page_home():
    render_hero_banner()
    render_stats_row(k_val=st.session_state["k_factors"], total_items=len(movies_df) + len(music_df) + len(products_df))

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Category overview showcase
    st.markdown("### 🌐 Explore Recommendation Categories")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎬</div>
            <div class="feature-title">Movie Recommendations</div>
            <div class="feature-text">
                Personalized cinematic selections spanning <b>Action, Comedy, Romance, Thriller, and Sci-Fi</b>. 
                Decomposes viewing habits to unearth films matching your narrative taste vectors.
            </div>
            <div style="margin-top: 1rem;">
                <span class="neon-badge-cyan">Top 10 Picks</span>
                <span class="neon-badge">Genre Filters</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🎵</div>
            <div class="feature-title">Music Recommendations</div>
            <div class="feature-text">
                Rhythm and vibe matching across <b>Melody, Pop, Hip-Hop, Classical, and Rock</b>. 
                SVD captures latent acoustic patterns to recommend songs perfectly synced to your sonic profile.
            </div>
            <div style="margin-top: 1rem;">
                <span class="neon-badge">Audio Vibes</span>
                <span class="neon-badge-amber">Artist Radar</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🛍️</div>
            <div class="feature-title">Shopping Recommendations</div>
            <div class="feature-text">
                E-Commerce intelligence across <b>Electronics, Fashion, Accessories, and Home Appliances</b>. 
                Predicts purchasing affinities and rates products you didn't know you needed.
            </div>
            <div style="margin-top: 1rem;">
                <span class="neon-badge-amber">Smart Deals</span>
                <span class="neon-badge-cyan">Personalized Cart</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

    # How SVD Works section
    st.markdown("### 🧠 How Singular Value Decomposition (SVD) Works")
    st.markdown(r"""
    Singular Value Decomposition factorizes our high-dimensional, sparse user-item interaction matrix 
    \( R \) into three informative constituent matrices:
    """)

    svd_col1, svd_col2, svd_col3 = st.columns(3)
    with svd_col1:
        st.markdown(r"""
        <div style="background: rgba(22, 18, 54, 0.6); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(139,92,246,0.2);">
            <div style="color: #c084fc; font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">1. User Matrix (U)</div>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Maps each user into an orthonormal latent preference space of dimension <b>k</b>. Represents how much a user prefers latent features (e.g., sci-fi themes, high bpm, premium aesthetics).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with svd_col2:
        st.markdown(r"""
        <div style="background: rgba(22, 18, 54, 0.6); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(139,92,246,0.2);">
            <div style="color: #38bdf8; font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">2. Singular Values (Σ)</div>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Diagonal matrix of singular values \(\sigma_1 \ge \sigma_2 \dots \ge \sigma_k\). Encodes the relative strength and variance captured by each hidden latent dimension.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with svd_col3:
        st.markdown(r"""
        <div style="background: rgba(22, 18, 54, 0.6); padding: 1.25rem; border-radius: 12px; border: 1px solid rgba(139,92,246,0.2);">
            <div style="color: #34d399; font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">3. Item Matrix (Vᵀ)</div>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Maps items (movies, songs, products) into the same <b>k</b>-dimensional space. Enables cosine similarity and rating dot product predictions \(\hat{R} = U \Sigma V^T + \mu_u\).
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

    # Featured Top Picks Preview for the active user
    st.markdown(f"### ⭐ Live Top Picks for {curr_profile['avatar']} {curr_profile['name']}")
    
    # Run SVD engines for the 3 domains
    mov_engine = get_fitted_svd_engine("movies", st.session_state["k_factors"])
    mus_engine = get_fitted_svd_engine("music", st.session_state["k_factors"])
    prd_engine = get_fitted_svd_engine("shopping", st.session_state["k_factors"])

    top_mov = mov_engine.get_top_recommendations(st.session_state["active_user"], n=1)
    top_mus = mus_engine.get_top_recommendations(st.session_state["active_user"], n=1)
    top_prd = prd_engine.get_top_recommendations(st.session_state["active_user"], n=1)

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.markdown("<h4 style='color:#c084fc;'>🎬 Recommended Movie</h4>", unsafe_allow_html=True)
        if not top_mov.empty:
            render_movie_card(top_mov.iloc[0].to_dict(), "home_mov", lambda i, r: handle_user_rating("movies", i, r))

    with fcol2:
        st.markdown("<h4 style='color:#38bdf8;'>🎵 Recommended Song</h4>", unsafe_allow_html=True)
        if not top_mus.empty:
            render_music_card(top_mus.iloc[0].to_dict(), "home_mus", lambda i, r: handle_user_rating("music", i, r))

    with fcol3:
        st.markdown("<h4 style='color:#34d399;'>🛍️ Recommended Product</h4>", unsafe_allow_html=True)
        if not top_prd.empty:
            render_product_card(top_prd.iloc[0].to_dict(), "home_prd", lambda i, r: handle_user_rating("shopping", i, r))


# -----------------------------------------------------------------------------
# 6. PAGE: MOVIES
# -----------------------------------------------------------------------------
def page_movies():
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.5rem;">
        <div>
            <h1 class="brand-title" style="font-size: 2.2rem; margin:0;">🎬 Movie Recommendations</h1>
            <p style="color:#94a3b8; font-size:0.95rem; margin:4px 0 0 0;">
                Personalized cinema suggestions computed via Singular Value Decomposition matrix factorization.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    engine = get_fitted_svd_engine("movies", st.session_state["k_factors"])
    user = st.session_state["active_user"]

    # Filter & Search bar
    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        genre_filter = st.selectbox(
            "Filter by Genre:",
            options=["All", "Action", "Comedy", "Romance", "Thriller", "Sci-Fi"],
            index=0
        )
    with fcol2:
        search_query = st.text_input("🔍 Search Movies by Title or Director:", "")
    with fcol3:
        rec_mode = st.radio(
            "Display Mode:",
            options=["Personalized Top 10", "Full Catalog & Ratings"],
            horizontal=True
        )

    st.markdown("<hr style='opacity:0.15; margin: 1rem 0 1.5rem 0;'/>", unsafe_allow_html=True)

    if "Top 10" in rec_mode:
        st.markdown(f"### 🏆 Top 10 Personalized Movies for {USER_PROFILES[user]['avatar']} {USER_PROFILES[user]['name']}")
        recs = engine.get_top_recommendations(
            user,
            n=10,
            category_col="genre" if genre_filter != "All" else None,
            category_val=genre_filter if genre_filter != "All" else None,
            exclude_rated=False
        )

        if search_query:
            recs = recs[recs["title"].str.contains(search_query, case=False) | recs["director"].str.contains(search_query, case=False)]

        if recs.empty:
            st.info("No movies matched your current filters. Try relaxing the search or genre criteria.")
            return

        # Render in 3 responsive columns
        cols = st.columns(3)
        for idx, (_, movie) in enumerate(recs.iterrows()):
            with cols[idx % 3]:
                render_movie_card(movie.to_dict(), f"mov_rec_{idx}", lambda i, r: handle_user_rating("movies", i, r))
    else:
        st.markdown("### 📽️ All Catalog Movies & Your Ratings")
        cat_df = movies_df.copy()
        user_ratings = get_user_rated_items("movies", user)
        cat_df["user_actual_rating"] = cat_df["item_id"].map(user_ratings).fillna(0.0)
        cat_df["predicted_rating"] = cat_df["item_id"].apply(lambda i: engine.predict_rating(user, i))
        cat_df["match_score"] = (cat_df["predicted_rating"] / 5.0 * 100).round(1)

        if genre_filter != "All":
            cat_df = cat_df[cat_df["genre"].str.lower() == genre_filter.lower()]
        if search_query:
            cat_df = cat_df[cat_df["title"].str.contains(search_query, case=False) | cat_df["director"].str.contains(search_query, case=False)]

        cols = st.columns(3)
        for idx, (_, movie) in enumerate(cat_df.iterrows()):
            with cols[idx % 3]:
                render_movie_card(movie.to_dict(), f"mov_cat_{idx}", lambda i, r: handle_user_rating("movies", i, r))


# -----------------------------------------------------------------------------
# 7. PAGE: MUSIC
# -----------------------------------------------------------------------------
def page_music():
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.5rem;">
        <div>
            <h1 class="brand-title" style="font-size: 2.2rem; margin:0;">🎵 Music Recommendations</h1>
            <p style="color:#94a3b8; font-size:0.95rem; margin:4px 0 0 0;">
                Acoustic vibes and artist recommendations powered by SVD latent collaborative filtering.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    engine = get_fitted_svd_engine("music", st.session_state["k_factors"])
    user = st.session_state["active_user"]

    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        genre_filter = st.selectbox(
            "Filter by Genre:",
            options=["All", "Melody", "Pop", "Hip-Hop", "Classical", "Rock"],
            index=0
        )
    with fcol2:
        search_query = st.text_input("🔍 Search Tracks by Title or Artist:", "")
    with fcol3:
        rec_mode = st.radio(
            "Display Mode:",
            options=["Personalized Suggestions", "Full Discography"],
            horizontal=True
        )

    st.markdown("<hr style='opacity:0.15; margin: 1rem 0 1.5rem 0;'/>", unsafe_allow_html=True)

    if "Personalized" in rec_mode:
        st.markdown(f"### 🎧 Curated Tracks for {USER_PROFILES[user]['avatar']} {USER_PROFILES[user]['name']}")
        recs = engine.get_top_recommendations(
            user,
            n=10,
            category_col="genre" if genre_filter != "All" else None,
            category_val=genre_filter if genre_filter != "All" else None,
            exclude_rated=False
        )

        if search_query:
            recs = recs[recs["title"].str.contains(search_query, case=False) | recs["artist"].str.contains(search_query, case=False)]

        if recs.empty:
            st.info("No songs found matching your search criteria.")
            return

        cols = st.columns(3)
        for idx, (_, song) in enumerate(recs.iterrows()):
            with cols[idx % 3]:
                render_music_card(song.to_dict(), f"mus_rec_{idx}", lambda i, r: handle_user_rating("music", i, r))
    else:
        st.markdown("### 🎼 All Tracks & SVD Affinity")
        cat_df = music_df.copy()
        user_ratings = get_user_rated_items("music", user)
        cat_df["user_actual_rating"] = cat_df["item_id"].map(user_ratings).fillna(0.0)
        cat_df["predicted_rating"] = cat_df["item_id"].apply(lambda i: engine.predict_rating(user, i))
        cat_df["match_score"] = (cat_df["predicted_rating"] / 5.0 * 100).round(1)

        if genre_filter != "All":
            cat_df = cat_df[cat_df["genre"].str.lower() == genre_filter.lower()]
        if search_query:
            cat_df = cat_df[cat_df["title"].str.contains(search_query, case=False) | cat_df["artist"].str.contains(search_query, case=False)]

        cols = st.columns(3)
        for idx, (_, song) in enumerate(cat_df.iterrows()):
            with cols[idx % 3]:
                render_music_card(song.to_dict(), f"mus_cat_{idx}", lambda i, r: handle_user_rating("music", i, r))


# -----------------------------------------------------------------------------
# 8. PAGE: SHOPPING
# -----------------------------------------------------------------------------
def page_shopping():
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 1.5rem;">
        <div>
            <h1 class="brand-title" style="font-size: 2.2rem; margin:0;">🛍️ Shopping Recommendations</h1>
            <p style="color:#94a3b8; font-size:0.95rem; margin:4px 0 0 0;">
                Smart e-commerce recommendations tuned to your lifestyle, tech, and aesthetic preferences.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    engine = get_fitted_svd_engine("shopping", st.session_state["k_factors"])
    user = st.session_state["active_user"]

    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        cat_filter = st.selectbox(
            "Filter Category:",
            options=["All", "Electronics", "Fashion", "Accessories", "Home Appliances"],
            index=0
        )
    with fcol2:
        price_range = st.slider(
            "Max Price ($):",
            min_value=50,
            max_value=1500,
            value=1500,
            step=50
        )
    with fcol3:
        search_query = st.text_input("🔍 Search Products:", "")

    st.markdown("<hr style='opacity:0.15; margin: 1rem 0 1.5rem 0;'/>", unsafe_allow_html=True)

    st.markdown(f"### 🏷️ Personalized Picks for {USER_PROFILES[user]['avatar']} {USER_PROFILES[user]['name']}")
    recs = engine.get_top_recommendations(
        user,
        n=12,
        category_col="category" if cat_filter != "All" else None,
        category_val=cat_filter if cat_filter != "All" else None,
        exclude_rated=False
    )

    recs = recs[recs["price"] <= price_range]
    if search_query:
        recs = recs[recs["name"].str.contains(search_query, case=False) | recs["brand"].str.contains(search_query, case=False)]

    if recs.empty:
        st.info("No products matched your price and category filters.")
        return

    cols = st.columns(3)
    for idx, (_, product) in enumerate(recs.iterrows()):
        with cols[idx % 3]:
            render_product_card(product.to_dict(), f"prod_rec_{idx}", lambda i, r: handle_user_rating("shopping", i, r))


# -----------------------------------------------------------------------------
# 9. PAGE: MY RECOMMENDATIONS (COMBINED MULTI-DOMAIN)
# -----------------------------------------------------------------------------
def page_my_recommendations():
    user = st.session_state["active_user"]
    profile = USER_PROFILES[user]

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <span class="neon-badge">✨ Unified Multi-Domain Taste Dashboard</span>
        <h1 class="brand-title" style="font-size: 2.25rem; margin-top: 0.5rem;">
            {profile['avatar']} Personalized Recommendations for {profile['name']}
        </h1>
        <p style="color:#94a3b8; font-size:1rem;">
            Cross-domain intelligence integrating your Movie, Music, and Shopping latent factors.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Radar Chart of User Preference Profile
    mov_engine = get_fitted_svd_engine("movies", st.session_state["k_factors"])
    mus_engine = get_fitted_svd_engine("music", st.session_state["k_factors"])
    prd_engine = get_fitted_svd_engine("shopping", st.session_state["k_factors"])

    # Calculate average predicted affinity per genre/category
    radar_data = []
    
    # Movie genres
    for g in ["Sci-Fi", "Action", "Thriller", "Comedy", "Romance"]:
        items_in_g = movies_df[movies_df["genre"] == g]["item_id"]
        pred_scores = [mov_engine.predict_rating(user, i) for i in items_in_g]
        avg_score = np.mean(pred_scores) if pred_scores else 3.5
        radar_data.append({"Category": f"🎬 {g}", "Affinity": round(avg_score, 2), "Domain": "Movie"})

    # Music genres
    for g in ["Rock", "Pop", "Hip-Hop", "Classical", "Melody"]:
        items_in_g = music_df[music_df["genre"] == g]["item_id"]
        pred_scores = [mus_engine.predict_rating(user, i) for i in items_in_g]
        avg_score = np.mean(pred_scores) if pred_scores else 3.5
        radar_data.append({"Category": f"🎵 {g}", "Affinity": round(avg_score, 2), "Domain": "Music"})

    # Shopping categories
    for g in ["Electronics", "Fashion", "Accessories", "Home Appliances"]:
        items_in_g = products_df[products_df["category"] == g]["item_id"]
        pred_scores = [prd_engine.predict_rating(user, i) for i in items_in_g]
        avg_score = np.mean(pred_scores) if pred_scores else 3.5
        radar_data.append({"Category": f"🛍️ {g}", "Affinity": round(avg_score, 2), "Domain": "Shopping"})

    radar_df = pd.DataFrame(radar_data)

    chart_col1, chart_col2 = st.columns([3, 2])
    with chart_col1:
        st.markdown("#### 🎯 Latent Taste Affinity Radar")
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_df["Affinity"],
            theta=radar_df["Category"],
            fill='toself',
            name=profile['name'],
            line=dict(color='#a855f7', width=2),
            fillcolor='rgba(168, 85, 247, 0.25)'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[1.0, 5.0],
                    tickfont=dict(color="#cbd5e1", size=10),
                    gridcolor="rgba(255,255,255,0.1)"
                ),
                angularaxis=dict(
                    tickfont=dict(color="#e2e8f0", size=11, family="Plus Jakarta Sans"),
                    gridcolor="rgba(255,255,255,0.1)"
                ),
                bgcolor="rgba(20, 16, 51, 0.4)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=30, b=30),
            showlegend=False,
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown("#### 💡 Cross-Domain Synergy Insights")
        top_cats = radar_df.sort_values(by="Affinity", ascending=False).head(3)["Category"].tolist()
        
        st.markdown(f"""
        <div style="background: rgba(22, 18, 54, 0.7); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 14px; padding: 1.25rem;">
            <div style="color:#c084fc; font-weight:700; margin-bottom:0.5rem; font-size:1rem;">Top Predicted Passions:</div>
            <ul style="padding-left: 1.2rem; color: #f1f5f9; line-height: 1.7; font-size: 0.9rem;">
                <li><b>{top_cats[0]}</b></li>
                <li><b>{top_cats[1]}</b></li>
                <li><b>{top_cats[2]}</b></li>
            </ul>
            <hr style="opacity:0.15; margin: 1rem 0;"/>
            <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
                ⚡ <b>SVD Synergy Rule:</b> Users with high affinity for {top_cats[0]} and {top_cats[1]} exhibit a 
                strong mathematical co-occurrence with {top_cats[2]}, demonstrating genuine latent factor alignment across entertainment and shopping!
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.2; margin: 2rem 0;'/>", unsafe_allow_html=True)

    # Side-by-side Top Picks
    st.markdown("### 🌟 Top 3 Recommendations Across All Domains")
    m_col, mu_col, p_col = st.columns(3)

    top_m = mov_engine.get_top_recommendations(user, n=3)
    top_mu = mus_engine.get_top_recommendations(user, n=3)
    top_p = prd_engine.get_top_recommendations(user, n=3)

    with m_col:
        st.markdown("<h3 style='color:#c084fc; font-size:1.25rem;'>🎬 Top Movies</h3>", unsafe_allow_html=True)
        for idx, (_, row) in enumerate(top_m.iterrows()):
            render_movie_card(row.to_dict(), f"my_mov_{idx}", lambda i, r: handle_user_rating("movies", i, r))

    with mu_col:
        st.markdown("<h3 style='color:#38bdf8; font-size:1.25rem;'>🎵 Top Songs</h3>", unsafe_allow_html=True)
        for idx, (_, row) in enumerate(top_mu.iterrows()):
            render_music_card(row.to_dict(), f"my_mus_{idx}", lambda i, r: handle_user_rating("music", i, r))

    with p_col:
        st.markdown("<h3 style='color:#34d399; font-size:1.25rem;'>🛍️ Top Products</h3>", unsafe_allow_html=True)
        for idx, (_, row) in enumerate(top_p.iterrows()):
            render_product_card(row.to_dict(), f"my_prod_{idx}", lambda i, r: handle_user_rating("shopping", i, r))


# -----------------------------------------------------------------------------
# 10. PAGE: SVD ANALYSIS (MATHEMATICAL & VISUALIZATION DASHBOARD)
# -----------------------------------------------------------------------------
def page_svd_analysis():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <span class="neon-badge">🔬 Machine Learning & Linear Algebra</span>
        <h1 class="brand-title" style="font-size: 2.25rem; margin-top: 0.5rem;">
            Singular Value Decomposition (SVD) Analysis
        </h1>
        <p style="color:#94a3b8; font-size:0.95rem;">
            Deep-dive into matrix factorization, singular values, latent embedding projections, and reconstruction accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Domain selector for analysis
    domain_col, k_col = st.columns([2, 2])
    with domain_col:
        selected_domain = st.selectbox(
            "Select Recommendation Domain for SVD Inspection:",
            options=["Movies", "Music", "Shopping"],
            index=0
        )
    with k_col:
        k_analysis = st.slider(
            "Analysis Latent Dimensions (k):",
            min_value=1,
            max_value=6,
            value=st.session_state["k_factors"],
            key="analysis_k_slider"
        )

    cat_key = selected_domain.lower()
    engine = get_fitted_svd_engine(cat_key, k_analysis)

    # Technical Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{engine.user_item_matrix.shape[0]} × {engine.user_item_matrix.shape[1]}</div>
            <div class="metric-label">Matrix Dimensions (Users × Items)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">k = {k_analysis}</div>
            <div class="metric-label">Truncated Rank</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{engine.rmse:.3f}★</div>
            <div class="metric-label">Reconstruction RMSE</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        cum_var = np.sum(engine.explained_variance_ratio[:k_analysis]) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{cum_var:.1f}%</div>
            <div class="metric-label">Cumulative Energy / Variance</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.2; margin: 1.5rem 0;'/>", unsafe_allow_html=True)

    # Visualizations Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Latent Factor Space (Item Embeddings)",
        "🔥 Rating Matrices (Raw vs Reconstructed)",
        "📉 Singular Value Spectrum (Scree Plot)",
        "📐 Mathematical Formulation"
    ])

    with tab1:
        st.markdown("### 🌌 2D Item Latent Factor Space (Embeddings)")
        st.markdown(r"""
        By projecting item vectors into the first two latent singular dimensions:
        \( \mathbf{v}_i \cdot \sqrt{\Sigma} \), we can observe how SVD automatically clusters similar genres together!
        """)
        latent_df = engine.get_latent_item_factors()
        
        if not latent_df.empty and "Latent_Factor_1" in latent_df.columns:
            group_col = "genre" if "genre" in latent_df.columns else "category"
            title_col = "title" if "title" in latent_df.columns else "name"

            # Determine second dimension (fallback to 0 if k=1)
            y_col = "Latent_Factor_2" if "Latent_Factor_2" in latent_df.columns else "Latent_Factor_1"

            fig_scatter = px.scatter(
                latent_df,
                x="Latent_Factor_1",
                y=y_col,
                color=group_col,
                hover_data=[title_col, "rating"],
                title=f"Latent Factor 1 vs Latent Factor 2 ({selected_domain})",
                template="plotly_dark",
                height=520
            )
            fig_scatter.update_traces(marker=dict(size=12, line=dict(width=1.5, color='white')))
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(18, 14, 46, 0.5)",
                font=dict(family="Plus Jakarta Sans", color="#cbd5e1")
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        st.markdown("### 🔥 User-Item Interaction Matrix Heatmaps")
        st.markdown("Observe how missing (unrated) entries in the original matrix are predicted by SVD low-rank reconstruction:")

        hm_col1, hm_col2 = st.columns(2)
        with hm_col1:
            st.markdown("#### 1. Original Sparse Matrix (NaN = Unrated)")
            raw_matrix = engine.user_item_matrix.fillna(0.0)
            fig_raw = px.imshow(
                raw_matrix.values,
                x=raw_matrix.columns,
                y=raw_matrix.index,
                labels=dict(x="Item ID", y="User ID", color="Rating"),
                color_continuous_scale="Purples",
                template="plotly_dark",
                height=400
            )
            fig_raw.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_raw, use_container_width=True)

        with hm_col2:
            st.markdown(f"#### 2. SVD Reconstructed Dense Matrix (k = {k_analysis})")
            pred_matrix = engine.predicted_matrix
            fig_pred = px.imshow(
                pred_matrix.values,
                x=pred_matrix.columns,
                y=pred_matrix.index,
                labels=dict(x="Item ID", y="User ID", color="Predicted"),
                color_continuous_scale="Plasma",
                template="plotly_dark",
                height=400
            )
            fig_pred.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pred, use_container_width=True)

    with tab3:
        st.markdown("### 📉 Singular Values Spectrum & Explained Variance")
        scree_df = pd.DataFrame({
            "Component": [f"σ_{i+1}" for i in range(len(engine.sigma_full))],
            "Singular Value": engine.sigma_full,
            "Explained Variance (%)": (engine.explained_variance_ratio * 100).round(2),
            "Cumulative Variance (%)": (np.cumsum(engine.explained_variance_ratio) * 100).round(2)
        })

        sc_col1, sc_col2 = st.columns([3, 2])
        with sc_col1:
            fig_scree = px.bar(
                scree_df,
                x="Component",
                y="Explained Variance (%)",
                text="Explained Variance (%)",
                title="Variance Retained per Latent Factor",
                template="plotly_dark",
                color="Explained Variance (%)",
                color_continuous_scale="Purples",
                height=380
            )
            fig_scree.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(18, 14, 46, 0.5)")
            st.plotly_chart(fig_scree, use_container_width=True)

        with sc_col2:
            st.markdown("#### Singular Value Decomposition Table")
            st.dataframe(scree_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### 📐 Mathematical Formulation of SVD Collaborative Filtering")
        st.markdown(r"""
        <div class="formula-card">
            <b>1. De-Meaning User Ratings to Mitigate User Bias:</b><br/>
            $$R_{u, i}^{norm} = R_{u, i} - \mu_u \quad \forall (u, i) \in \text{Observed}$$
            $$\text{Where } \mu_u = \frac{1}{|I_u|} \sum_{i \in I_u} R_{u, i}$$
        </div>

        <div class="formula-card">
            <b>2. Singular Value Decomposition Factorization:</b><br/>
            $$R^{norm} \approx U_k \Sigma_k V_k^T$$
            <ul>
                <li>\( U_k \in \mathbb{R}^{M \times k} \): Orthogonal user latent feature matrix.</li>
                <li>\( \Sigma_k \in \mathbb{R}^{k \times k} \): Diagonal matrix of top-k singular values.</li>
                <li>\( V_k^T \in \mathbb{R}^{k \times N} \): Orthogonal item latent feature matrix.</li>
            </ul>
        </div>

        <div class="formula-card">
            <b>3. Predicted Rating Reconstruction:</b><br/>
            $$\hat{R}_{u, i} = \mu_u + \left[ U_k \Sigma_k V_k^T \right]_{u, i}$$
            $$\text{Final Rating } = \text{clip}(\hat{R}_{u, i}, 1.0, 5.0)$$
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 11. PAGE: ABOUT PROJECT
# -----------------------------------------------------------------------------
def page_about():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <span class="neon-badge">🎓 Academic & Technical Overview</span>
        <h1 class="brand-title" style="font-size: 2.25rem; margin-top: 0.5rem;">
            About RecomAI – Smart Recommendation System
        </h1>
        <p style="color:#94a3b8; font-size:1rem;">
            B.Tech Computer Science Capstone Project in Artificial Intelligence & Machine Learning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### 🎯 Project Abstract & Objectives
        Recommendation systems form the foundational backbone of contemporary digital services, 
        including streaming giants (Netflix, Spotify) and e-commerce platforms (Amazon).
        
        **RecomAI** provides an end-to-end multi-domain recommendation platform integrating:
        1. **Movie Recommendations** across 5 distinct genres with director, cast, and poster metadata.
        2. **Music Recommendations** matching vibe, duration, and artist acoustic signatures.
        3. **Shopping Recommendations** tailoring product categories, prices, and discounts.
        4. **Live Collaborative Filtering via SVD** to dynamically compute missing ratings and update recommendations instantaneously.
        
        ### 🛠️ Technology Stack
        - **Frontend Framework:** Streamlit with custom CSS glassmorphism, responsive grid layouts, and CSS transitions.
        - **Backend Runtime:** Python 3.12.
        - **Machine Learning & Linear Algebra:** NumPy, SciPy (`svd`), Pandas.
        - **Interactive Data Visualization:** Plotly Graph Objects & Express.
        - **Model Persistence & State:** Real-time reactive session state management.
        """)

    with col2:
        st.markdown("""
        <div style="background: rgba(22, 18, 54, 0.7); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 14px; padding: 1.5rem;">
            <h4 style="color: #c084fc; margin-top:0;">🎓 Capstone Metadata</h4>
            <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.8;">
                <b>Project Title:</b> RecomAI<br/>
                <b>Discipline:</b> Computer Science & Engineering<br/>
                <b>Core ML Model:</b> Truncated Singular Value Decomposition (SVD)<br/>
                <b>Domains Covered:</b> 3 (Movies, Music, Shopping)<br/>
                <b>Catalog Size:</b> 75 Items (25 per domain)<br/>
                <b>Active User Personas:</b> 6 Distinct Profiles + Dynamic Custom Mode<br/>
                <b>Deployment Status:</b> Streamlit Cloud Ready
            </div>
            <hr style="opacity:0.2; margin: 1rem 0;"/>
            <div style="font-size: 0.8rem; color: #34d399; font-weight:600;">
                ✓ Verified Zero-Dependency on External Paid APIs<br/>
                ✓ Fully reproducible standalone datasets<br/>
                ✓ Dynamic Star Rating Feedback Loop
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.2; margin: 2rem 0;'/>", unsafe_allow_html=True)
    st.markdown("### 🔄 System Architecture Flowchart")
    st.markdown("""
    ```
    [ User Ratings Database / Dynamic User Session ]
                          │
                          ▼
            [ User-Item Interaction Matrix R ]
                          │
                          ▼
             [ User Mean De-Centering (R - μ) ]
                          │
                          ▼
     [ Truncated SVD Decomposition: R ≈ U_k · Σ_k · V_kᵀ ]
                          │
                          ▼
      [ Rating Reconstruction: R̂ = μ + U_k · Σ_k · V_kᵀ ]
                          │
                          ▼
     [ Rank Unrated Items Descending by Predicted Rating ]
                          │
                          ▼
    [ Multi-Domain Dashboards: Movies, Music, Shopping ]
    ```
    """)


# -----------------------------------------------------------------------------
# 12. ROUTING CONTROLLER
# -----------------------------------------------------------------------------
if "Home" in nav_selection:
    page_home()
elif "Movies" in nav_selection:
    page_movies()
elif "Music" in nav_selection:
    page_music()
elif "Shopping" in nav_selection:
    page_shopping()
elif "My Recommendations" in nav_selection:
    page_my_recommendations()
elif "SVD Analysis" in nav_selection:
    page_svd_analysis()
elif "About Project" in nav_selection:
    page_about()
