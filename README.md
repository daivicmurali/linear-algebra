# RecomAI – Smart Recommendation System ⚡

An AI-powered, multi-domain recommendation platform built with **Python**, **Streamlit**, and **Machine Learning** utilizing **Singular Value Decomposition (SVD)** matrix factorization.

Designed and developed for presentation as a high-caliber B.Tech Computer Science capstone project and ready for instant deployment on **Streamlit Community Cloud**.

---

## 🌟 Key Highlights & Features

### 1. Three Recommendation Domains
- 🎬 **Movie Recommendations:**
  - Curated catalogue covering **Action, Comedy, Romance, Thriller, and Sci-Fi**.
  - Movie posters, release years, directors, runtimes, cast, and synopses.
  - Personalized **Top 10 Movies** dynamically computed per user profile.
- 🎵 **Music Recommendations:**
  - Tracks spanning **Melody, Pop, Hip-Hop, Classical, and Rock**.
  - Track titles, artists, albums, release years, audio vibes, and preview simulation bars.
  - Latent acoustic affinity recommendations.
- 🛍️ **Shopping Recommendations:**
  - E-Commerce products across **Electronics, Fashion, Accessories, and Home Appliances**.
  - Product images, brand names, prices, discount badges, specs, and rating predictions.

### 2. Machine Learning SVD Implementation
- **Mathematical Matrix Factorization:** Decomposes user-item interaction matrix $R$ into $U \cdot \Sigma \cdot V^T$.
- **User Bias Mitigation (De-meaning):** Subtracts each user's mean rating $\mu_u$ before decomposition to handle strict vs. generous rating tendencies, restoring $\hat{R} = \mu_u + U_k \Sigma_k V_k^T$.
- **Latent Embedding Projections:** Extracts 2D item and user latent coordinates ($V_k \sqrt{\Sigma}$) to visualize item clusters in latent space.
- **Dynamic Feedback Loop:** Users can rate any movie, song, or product; the SVD model incorporates the new ratings in real-time!
- **Tunable Rank $k$:** Interactive slider ($k = 1$ to $6$) to observe reconstruction accuracy, singular values, and RMSE.

### 3. Website Pages
1. 🏠 **Home:** Hero section, multi-domain overview, "How SVD Works" 3-step breakdown, and live top picks.
2. 🎬 **Movies:** Personalized movie dashboard, genre filters, title/director search, and rating widget.
3. 🎵 **Music:** Personalized music dashboard, genre filters, artist/track search, and audio vibe preview.
4. 🛍️ **Shopping:** Personalized e-commerce dashboard, price filter slider, category filters, and search.
5. 🌟 **My Recommendations:** Unified multi-domain dashboard with **Latent Taste Affinity Radar Chart** and cross-domain synergy insights.
6. 🔬 **SVD Analysis:** Mathematical formulas, Scree plot (singular values & explained variance), original sparse vs. reconstructed dense heatmaps, and 2D latent factor scatter plot.
7. ℹ️ **About Project:** Academic abstract, technology stack, system architecture diagram, and methodology.

---

## 📐 Mathematical Formulation of SVD

The user-item rating matrix $R \in \mathbb{R}^{M \times N}$ is normalized by centering each user's observed ratings around their mean $\mu_u$:

$$R_{u, i}^{\text{norm}} = R_{u, i} - \mu_u \quad \forall (u, i) \in \text{Observed}$$

The de-meaned matrix is decomposed via Singular Value Decomposition:

$$R^{\text{norm}} \approx U_k \Sigma_k V_k^T$$

Where:
- $U_k \in \mathbb{R}^{M \times k}$: Left singular vectors (User latent preferences)
- $\Sigma_k \in \mathbb{R}^{k \times k}$: Singular values (Energy/importance of latent concepts)
- $V_k^T \in \mathbb{R}^{k \times N}$: Right singular vectors (Item latent characteristics)

Missing rating predictions are computed by projecting back to original rating space:

$$\hat{R}_{u, i} = \mu_u + \left[ U_k \Sigma_k V_k^T \right]_{u, i}$$

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed.

### 1. Clone or Open the Repository
```bash
git clone https://github.com/your-username/recomai.git
cd recomai
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Web Application
```bash
streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Directory Structure

```text
recomai/
├── data/
│   ├── movies.csv             # Curated movie catalog with posters & metadata
│   ├── music.csv              # Curated music catalog with album art & vibes
│   ├── products.csv           # Curated shopping catalog with specs & prices
│   ├── movie_ratings.csv      # Baseline interaction matrix for movies
│   ├── music_ratings.csv      # Baseline interaction matrix for music
│   └── product_ratings.csv    # Baseline interaction matrix for shopping
├── src/
│   ├── __init__.py
│   ├── svd_engine.py          # Core SVD recommendation & factorization engine
│   ├── data_loader.py         # Data loaders, persona profiles & session state
│   ├── styles.py              # Dark navy & purple gradient theme + glassmorphism CSS
│   └── ui_components.py       # Modern card renderers, badges & interactive widgets
├── generate_data.py           # Standalone dataset generator script
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Deployment dependencies
└── README.md                  # Project documentation
```

---

## 👥 Sample User Personas Available

The system includes pre-configured sample users with distinct taste profiles for instant evaluation:
- **Alex Chen (User 1):** Sci-Fi & Action movies, Rock & Hip-Hop, High-Performance Electronics.
- **Sophia Martinez (User 2):** Romance & Comedy movies, Pop music, Designer Fashion & Accessories.
- **Marcus Vance (User 3):** Psychological Thrillers, Classical & Neoclassical Piano, Smart Home Appliances.
- **Elena Rostova (User 4):** Adrenaline Action, Hip-Hop, Urban Accessories & Streetwear.
- **David Sterling (User 5):** Balanced Cinephile, Melody & Acoustic songs, Lifestyle Tech.
- **Interactive Guest:** Fresh custom profile where any visitor can rate items and watch recommendations adapt in real time!

---

## 🌐 Deployment to Streamlit Community Cloud

1. Push this repository to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New app"**, select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **"Deploy"**! No external API keys or credentials needed.
