"""
Custom Styling and Themes for RecomAI
Provides a sleek, premium dark navy and purple gradient theme with glassmorphism,
neon accents, animated cards, and responsive layouts.
"""

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e2e8f0;
    }

    /* Streamlit Main Viewport Background */
    .stApp {
        background: radial-gradient(circle at 10% 10%, #16103c 0%, #0c0a20 40%, #060511 100%) !important;
        background-attachment: fixed !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0a24 0%, #140e34 100%) !important;
        border-right: 1px solid rgba(138, 43, 226, 0.2) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(138, 43, 226, 0.2) !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Gradient Brand Title */
    .brand-title {
        background: linear-gradient(135deg, #ffffff 0%, #d8b4fe 40%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        display: inline-block;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.6;
    }

    /* Neon Purple Glow Accents */
    .neon-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background: rgba(139, 92, 246, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.2);
    }

    .neon-badge-cyan {
        background: rgba(6, 182, 212, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }

    .neon-badge-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.35);
    }

    /* Hero Card */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 24, 74, 0.7) 0%, rgba(17, 13, 44, 0.9) 100%);
        border: 1px solid rgba(147, 51, 234, 0.25);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 25px -5px rgba(139, 92, 246, 0.2);
        position: relative;
        overflow: hidden;
    }

    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -20%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.25) 0%, transparent 70%);
        pointer-events: none;
        border-radius: 50%;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(20, 16, 51, 0.7);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 14px;
        padding: 1.25rem 1rem;
        text-align: center;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.25);
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Item Card Container */
    .item-card {
        background: linear-gradient(180deg, rgba(27, 22, 65, 0.65) 0%, rgba(16, 13, 40, 0.85) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        height: 100%;
        margin-bottom: 1rem;
    }

    .item-card:hover {
        transform: translateY(-6px);
        border-color: rgba(168, 85, 247, 0.55);
        box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.6), 0 0 20px rgba(139, 92, 246, 0.25);
    }

    .item-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-bottom: 1px solid rgba(139, 92, 246, 0.15);
        transition: transform 0.4s ease;
    }

    .item-card:hover .item-card-image {
        transform: scale(1.03);
    }

    .item-card-body {
        padding: 1.1rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }

    .item-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.4rem;
        line-height: 1.35;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .item-card-subtitle {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 0.65rem;
    }

    .item-card-desc {
        font-size: 0.8rem;
        color: #cbd5e1;
        line-height: 1.45;
        margin-bottom: 0.85rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        flex-grow: 1;
    }

    .predicted-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.25) 0%, rgba(139, 92, 246, 0.3) 100%);
        color: #f472b6;
        border: 1px solid rgba(236, 72, 153, 0.4);
    }

    .match-percent {
        font-weight: 700;
        color: #34d399;
        font-size: 0.8rem;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(18, 14, 46, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
        border: none !important;
        background-color: transparent !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4) !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px -2px rgba(124, 58, 237, 0.35) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    /* Input & Select Fields */
    .stSelectbox, .stTextInput, .stSlider {
        color: #e2e8f0;
    }

    div[data-baseweb="select"] {
        background-color: rgba(22, 18, 54, 0.7) !important;
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(22, 18, 54, 0.7) !important;
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        border-radius: 10px !important;
    }

    /* Feature Banner Section */
    .feature-box {
        background: rgba(20, 16, 51, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 14px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease;
    }

    .feature-box:hover {
        border-color: rgba(168, 85, 247, 0.45);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        display: inline-block;
    }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.4rem;
    }

    .feature-text {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.55;
    }

    /* Formula Box for SVD Analysis */
    .formula-card {
        background: rgba(15, 12, 40, 0.8);
        border-left: 4px solid #a855f7;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #090a16;
    }
    ::-webkit-scrollbar-thumb {
        background: #3730a3;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4f46e5;
    }
    </style>
    """
