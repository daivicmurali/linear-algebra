"""
Data loader and state management module for RecomAI.
Handles loading catalog data, rating interaction matrices, and provides
reactive session state updates when users submit ratings.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st


USER_PROFILES = {
    "User_1": {
        "name": "Alex Chen",
        "tagline": "Sci-Fi & Action enthusiast, Rock listener, Gadget collector",
        "avatar": "🚀",
        "primary_genres": ["Sci-Fi", "Action", "Rock", "Electronics"],
        "color": "#8b5cf6"
    },
    "User_2": {
        "name": "Sophia Martinez",
        "tagline": "Romance & Comedy fan, Pop lover, Fashionista",
        "avatar": "✨",
        "primary_genres": ["Romance", "Comedy", "Pop", "Fashion"],
        "color": "#ec4899"
    },
    "User_3": {
        "name": "Marcus Vance",
        "tagline": "Psychological Thrillers, Neoclassical piano, Smart Home gear",
        "avatar": "🧠",
        "primary_genres": ["Thriller", "Classical", "Melody", "Home Appliances"],
        "color": "#06b6d4"
    },
    "User_4": {
        "name": "Elena Rostova",
        "tagline": "Adrenaline Action seeker, Hip-Hop head, Accessories curator",
        "avatar": "⚡",
        "primary_genres": ["Action", "Hip-Hop", "Accessories", "Fashion"],
        "color": "#f59e0b"
    },
    "User_5": {
        "name": "David Sterling",
        "tagline": "Eclectic Cinephile, Audiophile melody fan, Modern Lifestyle",
        "avatar": "🎯",
        "primary_genres": ["Sci-Fi", "Melody", "Electronics", "Home Appliances"],
        "color": "#10b981"
    },
    "Custom_User": {
        "name": "You (Interactive Guest)",
        "tagline": "Custom interactive profile -- Rate items to generate live recommendations!",
        "avatar": "🌟",
        "primary_genres": ["Personalized Live"],
        "color": "#a855f7"
    }
}


@st.cache_data
def load_catalogs():
    """Load items catalogs from CSV files."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    
    # If files don't exist yet, we will generate them
    movies_path = os.path.join(data_dir, "movies.csv")
    music_path = os.path.join(data_dir, "music.csv")
    products_path = os.path.join(data_dir, "products.csv")

    movies_df = pd.read_csv(movies_path) if os.path.exists(movies_path) else pd.DataFrame()
    music_df = pd.read_csv(music_path) if os.path.exists(music_path) else pd.DataFrame()
    products_df = pd.read_csv(products_path) if os.path.exists(products_path) else pd.DataFrame()

    return movies_df, music_df, products_df


@st.cache_data
def load_base_ratings():
    """Load baseline user ratings from CSV files."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    mov_r = pd.read_csv(os.path.join(data_dir, "movie_ratings.csv"))
    mus_r = pd.read_csv(os.path.join(data_dir, "music_ratings.csv"))
    prod_r = pd.read_csv(os.path.join(data_dir, "product_ratings.csv"))

    return mov_r, mus_r, prod_r


def get_active_ratings(category: str) -> pd.DataFrame:
    """
    Retrieve ratings for a category ('movies', 'music', 'shopping'),
    combining baseline datasets with active session ratings for the current user.
    """
    mov_r, mus_r, prod_r = load_base_ratings()
    
    if category == "movies":
        base_df = mov_r.copy()
    elif category == "music":
        base_df = mus_r.copy()
    else:
        base_df = prod_r.copy()

    # Check session state for user-submitted ratings
    if "user_ratings_override" in st.session_state and category in st.session_state["user_ratings_override"]:
        overrides = st.session_state["user_ratings_override"][category]
        if overrides:
            override_df = pd.DataFrame(overrides)
            # Remove any existing rows matching (user_id, item_id) in base_df
            merged = pd.concat([base_df, override_df], ignore_index=True)
            merged.drop_duplicates(subset=["user_id", "item_id"], keep="last", inplace=True)
            return merged

    return base_df


def add_user_rating(category: str, user_id: str, item_id: str, rating: float):
    """Save or update an active user's rating in st.session_state."""
    if "user_ratings_override" not in st.session_state:
        st.session_state["user_ratings_override"] = {"movies": [], "music": [], "shopping": []}
    
    records = st.session_state["user_ratings_override"][category]
    # Check if entry already exists and update
    found = False
    for rec in records:
        if rec["user_id"] == user_id and rec["item_id"] == item_id:
            rec["rating"] = rating
            found = True
            break
    if not found:
        records.append({"user_id": user_id, "item_id": item_id, "rating": rating})


def get_user_rated_items(category: str, user_id: str) -> dict:
    """Return a dictionary of {item_id: rating} rated by user in this category."""
    df = get_active_ratings(category)
    user_rows = df[df["user_id"] == user_id]
    return dict(zip(user_rows["item_id"], user_rows["rating"]))
