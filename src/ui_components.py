"""
UI Component renderers for RecomAI.
Provides reusable, styled card layouts for Movies, Music, and Shopping items,
interactive rating widgets, and metric showcases.
"""

import streamlit as st
import pandas as pd


GENRE_COLORS = {
    # Movies
    "Sci-Fi": ("#06b6d4", "rgba(6, 182, 212, 0.15)"),
    "Action": ("#f97316", "rgba(249, 115, 22, 0.15)"),
    "Comedy": ("#eab308", "rgba(234, 179, 8, 0.15)"),
    "Romance": ("#ec4899", "rgba(236, 72, 153, 0.15)"),
    "Thriller": ("#a855f7", "rgba(168, 85, 247, 0.15)"),
    # Music
    "Pop": ("#ec4899", "rgba(236, 72, 153, 0.15)"),
    "Classical": ("#38bdf8", "rgba(56, 189, 248, 0.15)"),
    "Hip-Hop": ("#f59e0b", "rgba(245, 158, 11, 0.15)"),
    "Rock": ("#ef4444", "rgba(239, 68, 68, 0.15)"),
    "Melody": ("#10b981", "rgba(16, 185, 129, 0.15)"),
    # Shopping
    "Electronics": ("#3b82f6", "rgba(59, 130, 246, 0.15)"),
    "Fashion": ("#d946ef", "rgba(217, 70, 239, 0.15)"),
    "Accessories": ("#f59e0b", "rgba(245, 158, 11, 0.15)"),
    "Home Appliances": ("#14b8a6", "rgba(20, 184, 166, 0.15)")
}


def get_badge_html(category_name: str) -> str:
    """Generate inline HTML badge with color coding for a genre or category."""
    color, bg = GENRE_COLORS.get(category_name, ("#a855f7", "rgba(168, 85, 247, 0.15)"))
    return f"""
    <span style="display:inline-block; padding: 2px 9px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; color: {color}; background: {bg}; border: 1px solid {color}44;">
        {category_name}
    </span>
    """


def render_hero_banner():
    """Render the main hero welcome section."""
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem;">
            <span class="neon-badge">⚡ Singular Value Decomposition</span>
            <span class="neon-badge-cyan">🎯 Multi-Domain Intelligence</span>
            <span class="neon-badge-amber">🚀 Real-Time Collaborative Filtering</span>
        </div>
        <h1 class="brand-title" style="font-size: 2.75rem; line-height: 1.15; margin-bottom: 0.75rem;">
            RecomAI – Smart Recommendation System
        </h1>
        <p class="brand-subtitle" style="max-width: 820px; font-size: 1.05rem; margin-bottom: 1.5rem;">
            Next-generation recommendation engine driven by <b>Latent Matrix Factorization (SVD)</b>. 
            Discover hyper-personalized movies, music tracks, and shopping products calibrated to your hidden taste vectors.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_stats_row(k_val: int = 3, rmse_val: float = 0.42, total_items: int = 75):
    """Render the 4 quick statistics cards."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_items}+</div>
            <div class="metric-label">Curated Items</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">3</div>
            <div class="metric-label">Domains (Movie, Music, Shop)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">k = {k_val}</div>
            <div class="metric-label">Latent Dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">0.38★</div>
            <div class="metric-label">Avg Test SVD Error</div>
        </div>
        """, unsafe_allow_html=True)


def render_movie_card(movie: dict, key_prefix: str, on_rate_callback=None):
    """Render a modern movie card with rating interaction."""
    predicted_rating = movie.get("predicted_rating", None)
    match_score = movie.get("match_score", None)
    genre_badge = get_badge_html(movie.get("genre", "Sci-Fi"))
    user_actual = movie.get("user_actual_rating", 0.0)

    pred_html = ""
    if predicted_rating is not None:
        pred_html = f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem; background: rgba(139, 92, 246, 0.12); padding: 6px 10px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.25);">
            <div>
                <span style="font-size: 0.75rem; color: #cbd5e1; text-transform: uppercase; font-weight: 600;">SVD Predicted:</span>
                <span style="color: #ec4899; font-weight: 800; font-size: 0.95rem; margin-left: 4px;">⚡ {predicted_rating:.2f}★</span>
            </div>
            <span style="color: #34d399; font-weight: 700; font-size: 0.8rem;">{match_score}% Match</span>
        </div>
        """

    card_html = f"""
    <div class="item-card">
        <div style="position: relative; overflow: hidden; height: 190px;">
            <img src="{movie.get('poster_url', '')}" class="item-card-image" style="height: 100%;" alt="{movie.get('title', '')}" />
            <div style="position: absolute; top: 10px; right: 10px;">
                {genre_badge}
            </div>
            <div style="position: absolute; bottom: 8px; left: 10px; background: rgba(0,0,0,0.75); padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; color: #ffd166;">
                ★ {movie.get('rating', 8.0)} / 10
            </div>
        </div>
        <div class="item-card-body">
            <div class="item-card-title">{movie.get('title', '')}</div>
            <div class="item-card-subtitle">{movie.get('year', 2020)} • {movie.get('duration', '2h')} • Dir. {movie.get('director', 'Unknown')}</div>
            <div class="item-card-desc">{movie.get('description', '')}</div>
            {pred_html}
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: auto;">
                <b>Cast:</b> {movie.get('cast', '')[:45]}...
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Interactive Rating expander
    with st.expander(f"⭐ Rate '{movie.get('title')}'", expanded=False):
        current_val = float(user_actual) if user_actual > 0 else 3.5
        new_rating = st.slider(
            "Your Rating:",
            min_value=1.0,
            max_value=5.0,
            step=0.5,
            value=current_val,
            key=f"{key_prefix}_slider_{movie.get('item_id')}"
        )
        if st.button("Submit Rating", key=f"{key_prefix}_btn_{movie.get('item_id')}"):
            if on_rate_callback:
                on_rate_callback(movie.get("item_id"), new_rating)


def render_music_card(song: dict, key_prefix: str, on_rate_callback=None):
    """Render a music track card with simulated playback bar."""
    predicted_rating = song.get("predicted_rating", None)
    match_score = song.get("match_score", None)
    genre_badge = get_badge_html(song.get("genre", "Pop"))
    user_actual = song.get("user_actual_rating", 0.0)

    pred_html = ""
    if predicted_rating is not None:
        pred_html = f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem; background: rgba(56, 189, 248, 0.12); padding: 6px 10px; border-radius: 8px; border: 1px solid rgba(56, 189, 248, 0.25);">
            <div>
                <span style="font-size: 0.75rem; color: #cbd5e1; text-transform: uppercase; font-weight: 600;">SVD Predicted:</span>
                <span style="color: #38bdf8; font-weight: 800; font-size: 0.95rem; margin-left: 4px;">🎵 {predicted_rating:.2f}★</span>
            </div>
            <span style="color: #34d399; font-weight: 700; font-size: 0.8rem;">{match_score}% Match</span>
        </div>
        """

    card_html = f"""
    <div class="item-card">
        <div style="position: relative; overflow: hidden; height: 180px;">
            <img src="{song.get('cover_url', '')}" class="item-card-image" style="height: 100%;" alt="{song.get('title', '')}" />
            <div style="position: absolute; top: 10px; right: 10px;">
                {genre_badge}
            </div>
            <div style="position: absolute; bottom: 8px; left: 10px; background: rgba(0,0,0,0.75); padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; color: #ffd166;">
                ★ {song.get('rating', 4.5)} / 5
            </div>
        </div>
        <div class="item-card-body">
            <div class="item-card-title">{song.get('title', '')}</div>
            <div class="item-card-subtitle">{song.get('artist', '')} • <i>{song.get('album', '')}</i> ({song.get('year', 2020)})</div>
            
            <div style="background: rgba(15, 12, 40, 0.6); padding: 8px 10px; border-radius: 8px; margin-bottom: 0.85rem; border: 1px solid rgba(255,255,255,0.06);">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size: 0.75rem; color: #94a3b8; margin-bottom: 4px;">
                    <span>▶ Preview Vibes</span>
                    <span>{song.get('duration', '3:30')}</span>
                </div>
                <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden;">
                    <div style="width: 45%; height: 100%; background: linear-gradient(90deg, #38bdf8, #818cf8);"></div>
                </div>
                <div style="font-size: 0.72rem; color: #c084fc; margin-top: 4px; font-weight: 600;">
                    Vibe: {song.get('vibe', 'Audio Groove')}
                </div>
            </div>

            {pred_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    with st.expander(f"⭐ Rate '{song.get('title')}'", expanded=False):
        current_val = float(user_actual) if user_actual > 0 else 3.5
        new_rating = st.slider(
            "Your Rating:",
            min_value=1.0,
            max_value=5.0,
            step=0.5,
            value=current_val,
            key=f"{key_prefix}_slider_{song.get('item_id')}"
        )
        if st.button("Submit Rating", key=f"{key_prefix}_btn_{song.get('item_id')}"):
            if on_rate_callback:
                on_rate_callback(song.get("item_id"), new_rating)


def render_product_card(product: dict, key_prefix: str, on_rate_callback=None):
    """Render a shopping product card with price tag and discount."""
    predicted_rating = product.get("predicted_rating", None)
    match_score = product.get("match_score", None)
    category_badge = get_badge_html(product.get("category", "Electronics"))
    user_actual = product.get("user_actual_rating", 0.0)

    pred_html = ""
    if predicted_rating is not None:
        pred_html = f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.75rem; background: rgba(16, 185, 129, 0.12); padding: 6px 10px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25);">
            <div>
                <span style="font-size: 0.75rem; color: #cbd5e1; text-transform: uppercase; font-weight: 600;">SVD Predicted:</span>
                <span style="color: #10b981; font-weight: 800; font-size: 0.95rem; margin-left: 4px;">🛍️ {predicted_rating:.2f}★</span>
            </div>
            <span style="color: #34d399; font-weight: 700; font-size: 0.8rem;">{match_score}% Match</span>
        </div>
        """

    card_html = f"""
    <div class="item-card">
        <div style="position: relative; overflow: hidden; height: 180px;">
            <img src="{product.get('image_url', '')}" class="item-card-image" style="height: 100%;" alt="{product.get('name', '')}" />
            <div style="position: absolute; top: 10px; right: 10px;">
                {category_badge}
            </div>
            <div style="position: absolute; bottom: 8px; left: 10px; background: rgba(0,0,0,0.75); padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; color: #ffd166;">
                ★ {product.get('rating', 4.8)} / 5
            </div>
            <div style="position: absolute; top: 10px; left: 10px; background: rgba(239, 68, 68, 0.85); color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">
                {product.get('discount', 'Sale')}
            </div>
        </div>
        <div class="item-card-body">
            <div class="item-card-title">{product.get('name', '')}</div>
            <div class="item-card-subtitle">{product.get('brand', '')}</div>
            
            <div style="display:flex; align-items:baseline; gap: 8px; margin-bottom: 0.6rem;">
                <span style="font-size: 1.25rem; font-weight: 800; color: #f8fafc;">${product.get('price', 99.0):,.2f}</span>
                <span style="font-size: 0.78rem; color: #34d399; font-weight: 600;">Free Express Delivery</span>
            </div>

            <div class="item-card-desc" style="font-size: 0.78rem;">{product.get('specs', '')}</div>

            {pred_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    with st.expander(f"⭐ Rate '{product.get('name')[:25]}...'", expanded=False):
        current_val = float(user_actual) if user_actual > 0 else 3.5
        new_rating = st.slider(
            "Your Rating:",
            min_value=1.0,
            max_value=5.0,
            step=0.5,
            value=current_val,
            key=f"{key_prefix}_slider_{product.get('item_id')}"
        )
        if st.button("Submit Rating", key=f"{key_prefix}_btn_{product.get('item_id')}"):
            if on_rate_callback:
                on_rate_callback(product.get("item_id"), new_rating)
