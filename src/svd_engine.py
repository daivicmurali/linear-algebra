"""
SVD Recommendation Engine
Implements Singular Value Decomposition for Collaborative Filtering.
De-means user interaction matrices, decomposes via SVD, reconstructs
predicted ratings, and extracts latent factors for 2D/3D visualizations.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List, Optional


class SVDEngine:
    def __init__(self, k_factors: int = 3):
        """
        Initialize the SVD Recommendation Engine.
        
        Args:
            k_factors: Number of latent dimensions to retain in truncated SVD.
        """
        self.k_factors = k_factors
        self.user_item_matrix = None        # Raw user x item DataFrame with NaNs
        self.imputed_matrix = None          # Mean-centered matrix filled with 0s
        self.user_means = None              # Series of mean rating per user
        self.global_mean = 3.5              # Overall fallback rating
        self.predicted_matrix = None        # Reconstructed dense ratings DataFrame
        self.U = None                       # User latent factors
        self.sigma = None                   # Singular values array
        self.Vt = None                      # Item latent factors (transposed)
        self.user_ids = []                  # Ordered list of user IDs
        self.item_ids = []                  # Ordered list of item IDs
        self.items_df = None                # Metadata DataFrame for items
        self.ratings_df = None              # Original ratings DataFrame
        self.explained_variance_ratio = []  # Variance explained by each singular value
        self.rmse = 0.0                     # Training RMSE on known ratings
        self.mae = 0.0                      # Training MAE on known ratings

    def fit(self, ratings_df: pd.DataFrame, items_df: pd.DataFrame, k: Optional[int] = None):
        """
        Fit the SVD model on user-item interaction data.
        
        Args:
            ratings_df: DataFrame containing ['user_id', 'item_id', 'rating']
            items_df: DataFrame containing item metadata with 'item_id' column
            k: Optional override for number of latent factors
        """
        if k is not None:
            self.k_factors = k

        self.ratings_df = ratings_df.copy()
        self.items_df = items_df.copy()

        # Build pivot table: rows = users, cols = items
        self.user_item_matrix = self.ratings_df.pivot_table(
            index="user_id",
            columns="item_id",
            values="rating"
        )

        # Ensure all items in items_df are represented in columns
        for item_id in items_df["item_id"]:
            if item_id not in self.user_item_matrix.columns:
                self.user_item_matrix[item_id] = np.nan

        # Sort columns to preserve consistent ordering
        self.user_item_matrix = self.user_item_matrix.reindex(sorted(self.user_item_matrix.columns), axis=1)

        self.user_ids = list(self.user_item_matrix.index)
        self.item_ids = list(self.user_item_matrix.columns)

        # Compute user means for de-meaning (handling user bias)
        self.user_means = self.user_item_matrix.mean(axis=1)
        self.global_mean = float(self.ratings_df["rating"].mean()) if not self.ratings_df.empty else 3.5

        # De-mean the rating matrix: R - mu_u
        user_means_expanded = self.user_means.values.reshape(-1, 1)
        # For users with no ratings yet, use global mean
        user_means_expanded = np.nan_to_num(user_means_expanded, nan=self.global_mean)

        matrix_values = self.user_item_matrix.values
        demeaned_matrix = matrix_values - user_means_expanded

        # Missing entries are imputed with 0 (equivalent to user's average rating)
        self.imputed_matrix = np.nan_to_num(demeaned_matrix, nan=0.0)

        # Determine effective k (must not exceed matrix dimensions)
        n_users, n_items = self.imputed_matrix.shape
        max_k = min(n_users, n_items)
        eff_k = min(self.k_factors, max_k)
        if eff_k < 1:
            eff_k = 1
        self.k_factors = eff_k

        # Perform Full Singular Value Decomposition via numpy.linalg.svd
        # R_demeaned = U * Sigma * V^T
        U_full, s_full, Vt_full = np.linalg.svd(self.imputed_matrix, full_matrices=False)

        # Singular values and explained variance
        self.sigma_full = s_full
        total_energy = np.sum(s_full ** 2)
        if total_energy > 0:
            self.explained_variance_ratio = (s_full ** 2) / total_energy
        else:
            self.explained_variance_ratio = np.zeros_like(s_full)

        # Truncate to top-k latent components
        self.U = U_full[:, :eff_k]
        self.sigma = s_full[:eff_k]
        self.Vt = Vt_full[:eff_k, :]

        # Diagonal matrix of singular values
        sigma_diag = np.diag(self.sigma)

        # Low-rank reconstruction: R_hat_norm = U_k * Sigma_k * V_k^T
        reconstructed_norm = np.dot(np.dot(self.U, sigma_diag), self.Vt)

        # Add back user means: R_hat = R_hat_norm + mu_u
        reconstructed_ratings = reconstructed_norm + user_means_expanded

        # Clip predicted ratings to valid range [1.0, 5.0]
        reconstructed_ratings = np.clip(reconstructed_ratings, 1.0, 5.0)

        # Convert back to DataFrame
        self.predicted_matrix = pd.DataFrame(
            reconstructed_ratings,
            index=self.user_ids,
            columns=self.item_ids
        )

        # Calculate evaluation metrics (RMSE & MAE) on known ratings
        known_mask = ~np.isnan(matrix_values)
        if np.any(known_mask):
            errors = matrix_values[known_mask] - reconstructed_ratings[known_mask]
            self.rmse = float(np.sqrt(np.mean(errors ** 2)))
            self.mae = float(np.mean(np.abs(errors)))
        else:
            self.rmse = 0.0
            self.mae = 0.0

        return self

    def predict_rating(self, user_id: str, item_id: str) -> float:
        """Predict the rating for a specific user and item."""
        if self.predicted_matrix is None or user_id not in self.predicted_matrix.index or item_id not in self.predicted_matrix.columns:
            return round(self.global_mean, 2)
        return round(float(self.predicted_matrix.loc[user_id, item_id]), 2)

    def get_top_recommendations(
        self,
        user_id: str,
        n: int = 10,
        category_col: Optional[str] = None,
        category_val: Optional[str] = None,
        exclude_rated: bool = True
    ) -> pd.DataFrame:
        """
        Generate top personalized recommendations for a user.
        
        Args:
            user_id: Target user identifier
            n: Number of recommendations to return
            category_col: Column name in items_df to filter by (e.g. 'genre' or 'category')
            category_val: Filter value (e.g. 'Sci-Fi' or 'Electronics')
            exclude_rated: If True, exclude items already rated by the user
        """
        if self.predicted_matrix is None or user_id not in self.predicted_matrix.index:
            # Fallback to items sorted by catalogue rating
            df = self.items_df.copy()
            df["predicted_rating"] = df["rating"]
            df["match_score"] = (df["predicted_rating"] / 5.0 * 100).round(1)
            if category_col and category_val and category_val.lower() != "all":
                df = df[df[category_col].str.lower() == category_val.lower()]
            return df.sort_values(by="rating", ascending=False).head(n)

        # Get user's predicted ratings
        user_preds = self.predicted_matrix.loc[user_id].copy()

        # Identify items already rated by user
        rated_items = set()
        if user_id in self.user_item_matrix.index:
            user_ratings = self.user_item_matrix.loc[user_id]
            rated_items = set(user_ratings.dropna().index)

        # Create recommendation candidate DataFrame
        rec_df = self.items_df.copy()
        rec_df["predicted_rating"] = rec_df["item_id"].map(user_preds).fillna(self.global_mean).round(2)
        
        # User's actual rating if available
        if user_id in self.user_item_matrix.index:
            rec_df["user_actual_rating"] = rec_df["item_id"].map(self.user_item_matrix.loc[user_id]).fillna(0.0)
        else:
            rec_df["user_actual_rating"] = 0.0

        # Match percentage score
        rec_df["match_score"] = (rec_df["predicted_rating"] / 5.0 * 100).round(1)

        # Exclude rated if requested
        if exclude_rated:
            rec_df = rec_df[~rec_df["item_id"].isin(rated_items)]

        # Apply category filter if specified
        if category_col and category_val and category_val.lower() != "all":
            rec_df = rec_df[rec_df[category_col].str.lower() == category_val.lower()]

        # Sort by predicted rating descending
        rec_df = rec_df.sort_values(by="predicted_rating", ascending=False)
        return rec_df.head(n)

    def get_latent_item_factors(self) -> pd.DataFrame:
        """
        Extract item latent vectors for 2D/3D visualization.
        Returns a DataFrame of items with their coordinates along latent dimensions.
        """
        if self.Vt is None or self.items_df is None:
            return pd.DataFrame()

        # V matrix is Vt.T -> shape (n_items, k)
        # Weight by singular values sqrt(Sigma) for balanced latent distance
        scale = np.sqrt(self.sigma)
        item_factors = self.Vt.T * scale

        factor_cols = [f"Latent_Factor_{i+1}" for i in range(self.k_factors)]
        df_factors = pd.DataFrame(item_factors, index=self.item_ids, columns=factor_cols)
        df_factors.reset_index(inplace=True)
        df_factors.rename(columns={"index": "item_id"}, inplace=True)

        # Merge with item metadata (title, category/genre, etc.)
        merged = pd.merge(self.items_df, df_factors, on="item_id")
        return merged

    def get_latent_user_factors(self) -> pd.DataFrame:
        """
        Extract user latent vectors for 2D/3D visualization.
        """
        if self.U is None:
            return pd.DataFrame()

        scale = np.sqrt(self.sigma)
        user_factors = self.U * scale

        factor_cols = [f"Latent_Factor_{i+1}" for i in range(self.k_factors)]
        df_factors = pd.DataFrame(user_factors, index=self.user_ids, columns=factor_cols)
        df_factors.reset_index(inplace=True)
        df_factors.rename(columns={"index": "user_id"}, inplace=True)
        return df_factors
