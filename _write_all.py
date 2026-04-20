#!/usr/bin/env python3
"""
_write_all.py
Rewrites utils/theme.py, app.py and all 4 pages with the new design system.
Run once: python3 _write_all.py
"""
import os

base = os.path.dirname(os.path.abspath(__file__))


def wr(rel_path, content):
    full = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote  {rel_path}")


# ── utils/theme.py ────────────────────────────────────────────────────────────
wr("utils/theme.py", '''"""
utils/theme.py
Shared design tokens, CSS animations, Plotly helper, and sidebar branding
for the Spotify BI Dashboard multi-page Streamlit app.
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# ── Design tokens ─────────────────────────────────────────────────────────────
ACCENT      = "#00e5a0"
PALETTE     = ["#00e5a0", "#7b61ff", "#ff6b35", "#ffb347", "#4ecdc4", "#ff6b9d", "#c9a0dc"]
BG          = "#0f0f1a"
SURFACE     = "#13132b"
CHART_BG    = "#12122a"
MOOD_COLORS = {"Happy": "#00e5a0", "Neutral": "#ffb347", "Sad": "#7b61ff"}

# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """<style>
@import url(\'https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap\');

html, body, [class*="css"] { font-family: \'DM Sans\', sans-serif !important; }

.stApp {
    background-color: #0f0f1a !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 10% 10%, rgba(0,229,160,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 90%, rgba(123,97,255,0.05) 0%, transparent 60%);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-24px); }
    to   { opacity: 1; transform: translateX(0);     }
}
@keyframes glowPulse {
    0%,100% { box-shadow: 0 0 10px rgba(0,229,160,0.2), 0 2px 8px rgba(0,0,0,0.4); }
    50%      { box-shadow: 0 0 24px rgba(0,229,160,0.5), 0 4px 16px rgba(0,0,0,0.4); }
}
@keyframes shimmer {
    0%   { left: -75%; }
    100% { left: 125%; }
}
@keyframes gradientFlow {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}

[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0b0b1e 0%, #0f0f1a 100%) !important;
    border-right: 1px solid rgba(0,229,160,0.12) !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #13132b 0%, #1a1a38 100%) !important;
    border: 1px solid rgba(0,229,160,0.22) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
    animation: fadeInUp 0.65s ease forwards, glowPulse 5s ease-in-out infinite 0.65s;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
[data-testid="stMetric"]::after {
    content: \'\';
    position: absolute;
    top: 0; left: -75%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.07), transparent);
    transform: skewX(-15deg);
    animation: shimmer 3.5s ease-in-out infinite;
}
[data-testid="stMetric"]:hover {
    transform: perspective(900px) rotateX(4deg) translateY(-7px) scale(1.02);
    box-shadow: 0 18px 36px rgba(0,229,160,0.14), 0 4px 12px rgba(0,0,0,0.5) !important;
    border-color: rgba(0,229,160,0.55) !important;
}
[data-testid="stMetricLabel"] { font-size: 0.82rem !important; color: #8888aa !important; font-weight: 500; }
[data-testid="stMetricValue"] { font-size: 1.6rem  !important; color: #ffffff !important; font-weight: 700; }

.stPlotlyChart {
    border-radius: 16px !important;
    border: 1px solid rgba(0,229,160,0.1) !important;
    overflow: hidden;
    animation: fadeInUp 0.75s ease forwards;
    transition: box-shadow 0.3s ease;
}
.stPlotlyChart:hover { box-shadow: 0 8px 28px rgba(0,229,160,0.12); }

.stDataFrame, [data-testid="stDataFrameResizable"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0,229,160,0.15) !important;
    overflow: hidden;
    animation: fadeInUp 0.85s ease forwards;
}

h1 { font-family: \'DM Sans\', sans-serif !important; }
h2 { font-family: \'DM Sans\', sans-serif !important; animation: fadeInLeft 0.6s ease forwards; }
h3 { font-family: \'DM Sans\', sans-serif !important; }

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.35), rgba(123,97,255,0.2), transparent) !important;
    margin: 1.4rem 0 !important;
}

.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(0,229,160,0.2) !important;
    background: rgba(0,229,160,0.03) !important;
    animation: fadeInUp 0.7s ease forwards;
}

[data-baseweb="select"] > div:first-child {
    background: #13132b !important;
    border-color: rgba(0,229,160,0.28) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(0,229,160,0.6) !important;
}

[data-testid="stSlider"] [role="slider"] {
    background: #00e5a0 !important;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(0,229,160,0.7) !important;
}

.stCaption, [data-testid="stCaptionContainer"] p {
    color: #55557a !important;
    font-size: 0.82rem;
}
</style>"""

# ── Scroll animation JS (injected via hidden iframe) ──────────────────────────
_SCROLL_JS = """<script>
(function() {
    try {
        var doc = window.parent.document;
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = \'1\';
                    entry.target.style.transform = \'translateY(0)\';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08, rootMargin: \'0px 0px -30px 0px\' });
        function setup() {
            doc.querySelectorAll(\'[data-testid="element-container"]\').forEach(function(el, i) {
                if (!el.dataset.srDone) {
                    el.style.opacity = \'0\';
                    el.style.transform = \'translateY(28px)\';
                    el.style.transition = \'opacity 0.65s ease \' + (i % 6) * 0.08 + \'s, transform 0.65s ease \' + (i % 6) * 0.08 + \'s\';
                    el.dataset.srDone = \'1\';
                    observer.observe(el);
                }
            });
        }
        setTimeout(setup, 400);
        setTimeout(setup, 1200);
    } catch(e) {}
})();
</script>"""


def apply_theme() -> None:
    """Inject global CSS. Call at the top of every page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def inject_scroll_animations() -> None:
    """Inject JS scroll-reveal via a 0-height hidden iframe component."""
    components.html(_SCROLL_JS, height=0, scrolling=False)


def dark_layout(fig: go.Figure, t: int = 40) -> go.Figure:
    """Apply consistent dark Plotly layout with the project design palette."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(t=t, l=10, r=10, b=10),
        font=dict(color="#e0e0f0", family="DM Sans"),
        colorway=PALETTE,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.08)"),
    )
    return fig


def sidebar_branding() -> None:
    """Render unified sidebar branding card on every page."""
    st.sidebar.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #13132b, #1a1a38);
            border: 1px solid rgba(0,229,160,0.25);
            border-radius: 14px;
            padding: 18px 16px 14px;
            margin-bottom: 14px;
            text-align: center;
        ">
            <div style="font-size:1.6rem; margin-bottom:4px;">&#127925;</div>
            <div style="font-size:1.05rem; font-weight:700; color:#00e5a0; letter-spacing:0.3px; line-height:1.3;">
                Spotify BI Dashboard
            </div>
            <div style="font-size:0.75rem; color:#8888aa; margin-top:5px; font-weight:500;">
                BI Analyst Portfolio Project
            </div>
            <hr style="border:none; height:1px;
                background:linear-gradient(90deg,transparent,rgba(0,229,160,0.3),transparent);
                margin:10px 0 8px;">
            <div style="font-size:0.82rem; color:#6666aa; line-height:1.55;">
                Interactive analytics dashboard<br>
                built with Streamlit &amp; Plotly<br>
                on the Kaggle Spotify dataset<br>
                <span style="color:#00e5a0;">113,549 tracks &middot; 114 genres</span>
            </div>
            <hr style="border:none; height:1px;
                background:linear-gradient(90deg,transparent,rgba(0,229,160,0.3),transparent);
                margin:10px 0 8px;">
            <div style="font-size:0.8rem;">
                <a href="https://github.com/" target="_blank"
                   style="color:#00e5a0; text-decoration:none; margin-right:10px;">
                   &#9671; GitHub
                </a>
                <a href="https://linkedin.com/" target="_blank"
                   style="color:#7b61ff; text-decoration:none;">
                   in LinkedIn
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
''')

# ── app.py ────────────────────────────────────────────────────────────────────
wr("app.py", '''"""
app.py  --  Landing page for the Spotify BI multi-page dashboard.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.theme import apply_theme, sidebar_branding, inject_scroll_animations

st.set_page_config(
    page_title="Spotify BI Dashboard",
    page_icon="&#127925;",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()
sidebar_branding()

st.markdown(
    """
    <div style="
        text-align:center; padding:3rem 1rem 2rem;
        background:linear-gradient(135deg,
            rgba(0,229,160,0.06) 0%,
            rgba(123,97,255,0.06) 50%,
            rgba(0,229,160,0.04) 100%);
        border:1px solid rgba(0,229,160,0.12);
        border-radius:20px; margin-bottom:2rem; overflow:hidden;
    ">
        <div style="
            font-size:2.8rem; font-weight:800;
            background:linear-gradient(135deg,#00e5a0 0%,#7b61ff 50%,#00e5a0 100%);
            background-size:200% auto;
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text;
            animation:gradientFlow 4s linear infinite;
            letter-spacing:-1px; line-height:1.2;
        ">&#127925; Spotify Music Intelligence Dashboard</div>
        <div style="font-size:1rem; color:#8888aa; margin-top:0.8rem;">
            Interactive BI analytics &nbsp;&middot;&nbsp; 113,549 tracks
            &nbsp;&middot;&nbsp; 114 genres &nbsp;&middot;&nbsp;
            Built with Streamlit &amp; Plotly
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h3 style=\'color:#e0e0f0; margin-bottom:1rem;\'>&#128194; Dashboard Pages</h3>",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
for col, icon, title, desc, color in [
    (c1, "&#128202;", "Executive Overview",     "KPIs, genre rankings, popularity trends",           "#00e5a0"),
    (c2, "&#127919;", "Hit Predictor",          "Energy scatter, correlation heatmap, insights",     "#7b61ff"),
    (c3, "&#128176;", "Revenue Intelligence",   "Top artists, genre revenue share, sortable table",  "#ff6b35"),
    (c4, "&#128640;", "Emerging Artists Radar", "Breakout scores, popularity vs genre average",      "#ffb347"),
]:
    with col:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(145deg,#13132b,#1a1a38);
                border:1px solid {color}44;
                border-radius:14px; padding:20px 16px; text-align:center;
                transition:transform 0.3s ease, box-shadow 0.3s ease;
            ">
                <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
                <div style="font-size:0.95rem; font-weight:700; color:{color}; margin-bottom:6px;">{title}</div>
                <div style="font-size:0.78rem; color:#7777aa; line-height:1.5;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
''')

# ── pages/1_Executive_Overview.py ─────────────────────────────────────────────
wr("pages/1_Executive_Overview.py", '''"""
pages/1_Executive_Overview.py
Page 1 — Executive Overview of the Spotify BI Dashboard.
Loads cleaned_spotify.csv and renders 4 KPI cards and 4 charts.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, ACCENT, PALETTE, CHART_BG,
)

st.set_page_config(
    page_title="Executive Overview · Spotify BI",
    page_icon="&#127925;",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_branding()
st.sidebar.header("Filters")

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)
pop_range  = st.sidebar.slider("Popularity range", 0, 100, (0, 100))
explicit_opt = st.sidebar.radio("Explicit content", ["All", "Explicit only", "Clean only"])

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]
if explicit_opt == "Explicit only":
    filtered = filtered[filtered["explicit"].astype(bool)]
elif explicit_opt == "Clean only":
    filtered = filtered[~filtered["explicit"].astype(bool)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style=\'text-align:center; color:#00e5a0; font-size:2.2rem;\'>"
    "&#127925; Spotify Music Intelligence Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style=\'text-align:center; color:#8888aa; margin-top:-10px;\'>"
    "Executive Overview &middot; Powered by Kaggle Spotify Tracks Dataset</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("&#127925; Total Tracks",         f"{len(filtered):,}")
k2.metric("&#127908; Unique Artists",       f"{filtered[\'artists\'].nunique():,}")
k3.metric("&#11088; Avg Popularity Score",  f"{filtered[\'popularity\'].mean():.1f} / 100")
k4.metric("&#128176; Total Est. Revenue",   f"${filtered[\'estimated_revenue_usd\'].sum():,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Genre bar + Popularity line ────────────────────────────────────────
col_bar, col_line = st.columns(2)

with col_bar:
    st.subheader("Top 10 Genres by Avg Popularity")
    genre_pop = (
        filtered.groupby("track_genre")["popularity"]
        .mean().sort_values(ascending=False).head(10).reset_index()
        .rename(columns={"track_genre": "Genre", "popularity": "Avg Popularity"})
    )
    fig_bar = px.bar(
        genre_pop, x="Avg Popularity", y="Genre", orientation="h",
        text=genre_pop["Avg Popularity"].round(1), color="Avg Popularity",
        color_continuous_scale=[[0, "#0d1530"], [1, ACCENT]],
        labels={"Avg Popularity": "Avg Popularity Score"},
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#FFFFFF")
    fig_bar.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(range=[0, genre_pop["Avg Popularity"].max() * 1.18]),
    )
    dark_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_line:
    st.subheader("Track Count by Popularity Score")
    st.caption("Dataset has no release date — showing popularity distribution instead.")
    bucket_size = 5
    bracket = (filtered["popularity"] // bucket_size * bucket_size).rename("popularity_bracket")
    bracket_counts = (
        bracket.value_counts().sort_index().reset_index()
        .rename(columns={"popularity_bracket": "Popularity Score", "count": "Track Count"})
    )
    fig_line = px.line(
        bracket_counts, x="Popularity Score", y="Track Count", markers=True,
        color_discrete_sequence=[ACCENT],
        labels={"Popularity Score": "Popularity Score (0-100)", "Track Count": "Number of Tracks"},
    )
    fig_line.update_traces(line_width=2.5, marker_size=6)
    fig_line.update_xaxes(dtick=10)
    dark_layout(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Row 2: Mood pie + Explicit bar ────────────────────────────────────────────
col_mood, col_exp = st.columns(2)

with col_mood:
    st.subheader("Mood Distribution")
    mood_counts = filtered["mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]
    color_map = {"Happy": "#00e5a0", "Neutral": "#ffb347", "Sad": "#7b61ff"}
    fig_mood = px.pie(
        mood_counts, values="Count", names="Mood",
        color="Mood", color_discrete_map=color_map, hole=0.45,
    )
    fig_mood.update_traces(textinfo="percent+label", textfont_size=13)
    dark_layout(fig_mood)
    st.plotly_chart(fig_mood, use_container_width=True)

with col_exp:
    st.subheader("Explicit vs Clean Tracks")
    explicit_counts = (
        filtered["explicit"].astype(bool)
        .map({True: "Explicit", False: "Clean"})
        .value_counts().reset_index()
    )
    explicit_counts.columns = ["Type", "Count"]
    fig_exp = px.bar(
        explicit_counts, x="Type", y="Count", color="Type",
        color_discrete_map={"Explicit": "#ff6b35", "Clean": ACCENT},
        text="Count",
    )
    fig_exp.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_exp.update_layout(showlegend=False)
    dark_layout(fig_exp)
    st.plotly_chart(fig_exp, use_container_width=True)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  ·  Filtered view: {len(filtered):,} tracks  ·  "
    "Source: Kaggle Spotify Tracks Dataset"
)
''')

# ── pages/2_Hit_Predictor.py ──────────────────────────────────────────────────
wr("pages/2_Hit_Predictor.py", '''"""
pages/2_Hit_Predictor.py
Page 2 — Hit Predictor. Answers: "What makes a hit?"
"""
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, ACCENT, PALETTE, CHART_BG, MOOD_COLORS,
)

HEATMAP_FEATURES = ["energy", "danceability", "valence", "tempo", "loudness", "popularity"]

st.set_page_config(
    page_title="Hit Predictor · Spotify BI",
    page_icon="&#127919;",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_branding()
st.sidebar.header("Filters")

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genre  = st.sidebar.selectbox("Genre", ["All genres"] + all_genres)
pop_range  = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

filtered = df.copy()
if sel_genre != "All genres":
    filtered = filtered[filtered["track_genre"] == sel_genre]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style=\'text-align:center; color:#00e5a0; font-size:2.2rem;\'>&#127919; Hit Predictor</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style=\'text-align:center; color:#8888aa; margin-top:-10px;\'>"
    f"Analysing <b>{len(filtered):,}</b> tracks"
    + (f" in <b>{sel_genre}</b>" if sel_genre != "All genres" else " across <b>all genres</b>")
    + "</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── SECTION 1: Scatter ────────────────────────────────────────────────────────
st.subheader("&#9889; Energy vs Popularity by Mood")
st.caption(
    "Each point is a track. Size = estimated streams. "
    "Colour shows whether the track is Happy, Sad, or Neutral (based on valence)."
)

scatter_df = filtered.sample(min(5_000, len(filtered)), random_state=42)
fig_scatter = px.scatter(
    scatter_df, x="energy", y="popularity",
    color="mood", color_discrete_map=MOOD_COLORS,
    size="estimated_streams", size_max=18,
    hover_data={
        "track_name": True, "artists": True, "track_genre": True,
        "energy": ":.2f", "popularity": True, "estimated_streams": ":,", "mood": True,
    },
    opacity=0.65,
    labels={"energy": "Energy (0-1)", "popularity": "Popularity Score", "mood": "Mood"},
    category_orders={"mood": ["Happy", "Neutral", "Sad"]},
)
fig_scatter.update_traces(marker=dict(line=dict(width=0.3, color="#333333")))
fig_scatter.update_layout(
    legend=dict(title="Mood", orientation="v", bgcolor="rgba(19,19,43,0.8)",
                bordercolor="#333", borderwidth=1),
    xaxis=dict(range=[-0.02, 1.05]),
    yaxis=dict(range=[-2, 105]),
)
dark_layout(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── SECTION 2: Heatmap + Insight ──────────────────────────────────────────────
col_heat, col_insight = st.columns([3, 2], gap="large")

with col_heat:
    st.subheader("&#128293; Audio Feature Correlation Matrix")
    corr = filtered[HEATMAP_FEATURES].corr()

    fig_heat, ax = plt.subplots(figsize=(7, 5))
    fig_heat.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
        vmin=-1, vmax=1, linewidths=0.5, linecolor="#1a1a38",
        annot_kws={"size": 10, "color": "white"}, cbar_kws={"shrink": 0.8}, ax=ax,
    )
    ax.tick_params(colors="white", labelsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", color="white")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color="white")
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")
    plt.tight_layout()
    buf = io.BytesIO()
    fig_heat.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor=CHART_BG)
    buf.seek(0)
    st.image(buf, use_container_width=True)
    plt.close(fig_heat)

with col_insight:
    st.subheader("&#128161; Data Insight")
    HIGH_THRESHOLD = 0.7
    high_mask = (filtered["energy"] > HIGH_THRESHOLD) & (filtered["danceability"] > HIGH_THRESHOLD)
    rest_mask = ~high_mask
    high_pop = filtered.loc[high_mask, "popularity"].mean()
    rest_pop = filtered.loc[rest_mask, "popularity"].mean()

    if rest_pop > 0 and not np.isnan(high_pop):
        pct_diff  = ((high_pop - rest_pop) / rest_pop) * 100
        direction = "higher" if pct_diff >= 0 else "lower"
        pct_label = f"{abs(pct_diff):.1f}%"
        high_count = int(high_mask.sum())
        insight_html = f"""
        <div style="background:rgba(0,229,160,0.05); border-left:4px solid #00e5a0;
                    border-radius:10px; padding:16px 20px; color:#e0e0e0; margin-top:12px;">
            <p style="font-size:1.05rem; font-weight:600; color:#00e5a0; margin-bottom:8px;">
                &#127925; High-Energy Dance Tracks
            </p>
            <p>Songs with <b>energy &gt; {HIGH_THRESHOLD}</b> and
               <b>danceability &gt; {HIGH_THRESHOLD}</b> score
               <b style="color:#00e5a0; font-size:1.2rem;">{pct_label} {direction}</b>
               popularity vs. other tracks.
            </p>
            <hr style="border-color:rgba(0,229,160,0.2); margin:10px 0;">
            <p style="color:#8888aa; font-size:0.85rem; margin:0;">
                High-energy dance tracks: <b style="color:white">{high_count:,}</b><br>
                Avg popularity (high E+D): <b style="color:#00e5a0">{high_pop:.1f}</b><br>
                Avg popularity (others):   <b style="color:#8888aa">{rest_pop:.1f}</b>
            </p>
        </div>"""
    else:
        insight_html = """<div style="background:rgba(0,229,160,0.03);
                border-left:4px solid rgba(0,229,160,0.3); border-radius:10px; padding:16px 20px;">
            <p style="color:#8888aa;">Not enough data. Try selecting "All genres" or widening the range.</p>
        </div>"""

    st.markdown(insight_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("&#128208; Feature Correlation with Popularity")
    corr_with_pop = (
        filtered[HEATMAP_FEATURES].corr()["popularity"]
        .drop("popularity")
        .sort_values(key=abs, ascending=True)
        .reset_index()
        .rename(columns={"index": "Feature", "popularity": "Pearson r"})
    )
    corr_with_pop["color"] = corr_with_pop["Pearson r"].apply(
        lambda v: ACCENT if v >= 0 else "#ff6b35"
    )
    fig_corr = px.bar(
        corr_with_pop, x="Pearson r", y="Feature", orientation="h",
        color="color", color_discrete_map="identity",
        text=corr_with_pop["Pearson r"].apply(lambda v: f"{v:+.3f}"),
        labels={"Pearson r": "Correlation with Popularity"}, range_x=[-1, 1],
    )
    fig_corr.add_vline(x=0, line_color="#333355", line_width=1)
    fig_corr.update_traces(textposition="outside", textfont_color="white")
    fig_corr.update_layout(showlegend=False)
    dark_layout(fig_corr, t=20)
    st.plotly_chart(fig_corr, use_container_width=True)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  ·  Filtered view: {len(filtered):,} tracks  ·  "
    "Scatter capped at 5,000 points for performance."
)
''')

# ── pages/3_Revenue_Intelligence.py ───────────────────────────────────────────
wr("pages/3_Revenue_Intelligence.py", '''"""
pages/3_Revenue_Intelligence.py
Page 3 — Revenue Intelligence. Answers: "Who earns the most?"
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, ACCENT, PALETTE, CHART_BG,
)

st.set_page_config(
    page_title="Revenue Intelligence · Spotify BI",
    page_icon="&#128176;",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_branding()
st.sidebar.header("Filters")

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)
pop_range  = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style=\'text-align:center; color:#00e5a0; font-size:2.2rem;\'>"
    "&#128176; Revenue Intelligence</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style=\'text-align:center; color:#8888aa; margin-top:-10px;\'>"
    f"Analysing estimated streaming revenue across <b>{len(filtered):,}</b> tracks</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── Pre-compute aggregates ────────────────────────────────────────────────────
artist_rev = (
    filtered.groupby("artists")
    .agg(
        total_revenue=("estimated_revenue_usd", "sum"),
        track_count=("track_name", "count"),
        avg_popularity=("popularity", "mean"),
    )
    .sort_values("total_revenue", ascending=False)
    .reset_index()
)

genre_rev = (
    filtered.groupby("track_genre")["estimated_revenue_usd"]
    .sum().sort_values(ascending=False).reset_index()
    .rename(columns={"track_genre": "Genre", "estimated_revenue_usd": "Revenue"})
)

total_revenue  = filtered["estimated_revenue_usd"].sum()
top_artist     = artist_rev.iloc[0]["artists"] if len(artist_rev) else "N/A"
top_genre      = genre_rev.iloc[0]["Genre"]    if len(genre_rev)  else "N/A"
avg_track_rev  = filtered["estimated_revenue_usd"].mean()
top_genre_rev  = genre_rev.iloc[0]["Revenue"]  if len(genre_rev) else 0
avg_genre_rev  = genre_rev["Revenue"].mean()    if len(genre_rev) else 1
genre_multiple = top_genre_rev / avg_genre_rev  if avg_genre_rev else 0

# ── KPI strip ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("&#128181; Total Est. Revenue",   f"${total_revenue:,.0f}")
k2.metric("&#129351; Top Earning Artist",   top_artist)
k3.metric("&#127928; Top Earning Genre",    top_genre)
k4.metric("&#128192; Avg Revenue / Track",  f"${avg_track_rev:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#0d1530 0%,#0d2845 100%);
                border:1px solid rgba(0,229,160,0.35); border-radius:14px;
                padding:18px 24px; margin-bottom:8px;">
        <div style="font-size:2.4rem; font-weight:700; color:#00e5a0; line-height:1.1;">{genre_multiple:.1f}x</div>
        <div style="font-size:0.9rem; color:#8888aa; margin-top:4px;">
            Top earning genre (<b style="color:#00e5a0">{top_genre}</b>)
            makes <b style="color:#00e5a0">{genre_multiple:.1f}x</b> more than the average genre
            &nbsp;&middot;&nbsp; Top: <b>${top_genre_rev:,.0f}</b>
            &nbsp;vs&nbsp; Avg: <b>${avg_genre_rev:,.0f}</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── Charts: artist bar + genre pie ────────────────────────────────────────────
col_bar, col_pie = st.columns([3, 2], gap="large")

with col_bar:
    st.subheader("&#127908; Top 15 Artists by Estimated Revenue")
    top15 = artist_rev.head(15).copy()
    top15["label"] = top15["total_revenue"].apply(lambda v: f"${v:,.0f}")
    fig_bar = px.bar(
        top15, x="total_revenue", y="artists", orientation="h", text="label",
        color="total_revenue",
        color_continuous_scale=[[0, "#0d1530"], [1, ACCENT]],
        hover_data={"artists": True, "total_revenue": ":,.0f",
                    "track_count": True, "avg_popularity": ":.1f"},
        labels={"total_revenue": "Estimated Revenue (USD)", "artists": "Artist",
                "track_count": "Tracks", "avg_popularity": "Avg Popularity"},
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#FFFFFF")
    fig_bar.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(range=[0, top15["total_revenue"].max() * 1.2]),
    )
    dark_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.subheader("&#127925; Revenue Share by Genre")
    TOP_N = 8
    top_genres_df = genre_rev.head(TOP_N).copy()
    other_rev = genre_rev.iloc[TOP_N:]["Revenue"].sum()
    if other_rev > 0:
        pie_df = pd.concat(
            [top_genres_df, pd.DataFrame([{"Genre": "Other", "Revenue": other_rev}])],
            ignore_index=True,
        )
    else:
        pie_df = top_genres_df

    pie_colors = list(PALETTE[:TOP_N]) + (["#444466"] if other_rev > 0 else [])
    fig_pie = px.pie(
        pie_df, values="Revenue", names="Genre",
        color_discrete_sequence=pie_colors, hole=0.4,
    )
    fig_pie.update_traces(textinfo="percent+label", textfont_size=12, pull=[0.03] * len(pie_df))
    fig_pie.update_layout(
        legend=dict(orientation="v", bgcolor="rgba(19,19,43,0.8)", bordercolor="#333", borderwidth=1),
        margin=dict(t=20, l=0, r=0, b=0),
    )
    dark_layout(fig_pie, t=20)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── Top 20 tracks table ───────────────────────────────────────────────────────
st.subheader("&#127942; Top 20 Tracks by Estimated Revenue")
st.caption("Click any column header to sort the table.")

top20_tracks = (
    filtered[["track_name", "artists", "track_genre",
               "estimated_streams", "estimated_revenue_usd", "popularity"]]
    .sort_values("estimated_revenue_usd", ascending=False)
    .head(20).reset_index(drop=True)
)
top20_tracks.index += 1
top20_tracks.columns = ["Track", "Artist", "Genre", "Est. Streams", "Est. Revenue (USD)", "Popularity"]

st.dataframe(
    top20_tracks.style
        .format({"Est. Streams": "{:,.0f}", "Est. Revenue (USD)": "${:,.2f}"})
        .background_gradient(subset=["Est. Revenue (USD)"], cmap="Greens"),
    use_container_width=True, height=560,
)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  ·  Filtered view: {len(filtered):,} tracks  ·  "
    "Revenue estimated as popularity x 1,000 streams x $0.004 per stream."
)
''')

# ── pages/4_Emerging_Artists_Radar.py ─────────────────────────────────────────
wr("pages/4_Emerging_Artists_Radar.py", '''"""
pages/4_Emerging_Artists_Radar.py
Page 4 — Emerging Artists Radar.
Emerging = popularity > 60 AND fewer than 5 tracks in the dataset.
Breakout Score = (popularity x danceability x energy) / 100
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, ACCENT, PALETTE, CHART_BG,
)

POP_THRESHOLD = 60
MAX_TRACKS    = 5

st.set_page_config(
    page_title="Emerging Artists Radar · Spotify BI",
    page_icon="&#128640;",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_branding()
st.sidebar.header("Filters")

pop_min = st.sidebar.slider(
    "Min popularity threshold", 50, 90, POP_THRESHOLD, step=5,
    help="Artists must have at least one track above this popularity score.",
)
max_tracks = st.sidebar.slider(
    "Max tracks in dataset", 1, 10, MAX_TRACKS, step=1,
    help="Artists with fewer than this many tracks are considered emerging.",
)
all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre filter", all_genres, default=all_genres)

# ── Compute emerging artists ──────────────────────────────────────────────────
track_counts       = df.groupby("artists")["track_name"].count()
low_volume_artists = track_counts[track_counts < max_tracks].index

emerging_tracks = df[
    (df["popularity"] > pop_min) &
    (df["artists"].isin(low_volume_artists)) &
    (df["track_genre"].isin(sel_genres))
].copy()
emerging_tracks["breakout_score"] = (
    (emerging_tracks["popularity"] * emerging_tracks["danceability"] * emerging_tracks["energy"]) / 100
).round(4)

artist_agg = (
    emerging_tracks.groupby("artists").agg(
        avg_popularity   =("popularity",            "mean"),
        avg_danceability =("danceability",          "mean"),
        avg_energy       =("energy",                "mean"),
        avg_valence      =("valence",               "mean"),
        total_revenue    =("estimated_revenue_usd", "sum"),
        track_count      =("track_name",            "count"),
        dominant_genre   =("track_genre",           lambda x: x.mode()[0]),
        breakout_score   =("breakout_score",        "mean"),
    )
    .sort_values("breakout_score", ascending=False)
    .reset_index()
)
for col in ("avg_popularity", "avg_danceability", "avg_energy", "breakout_score", "total_revenue"):
    artist_agg[col] = artist_agg[col].round(4 if col == "breakout_score" else
                                             2 if col == "total_revenue" else
                                             3 if col in ("avg_danceability", "avg_energy") else 1)

genre_avg_pop = df.groupby("track_genre")["popularity"].mean().to_dict()
artist_agg["genre_avg_popularity"] = artist_agg["dominant_genre"].map(genre_avg_pop).round(1)
artist_agg["vs_genre_avg"] = (artist_agg["avg_popularity"] - artist_agg["genre_avg_popularity"]).round(1)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style=\'text-align:center; color:#00e5a0; font-size:2.2rem;\'>"
    "&#128640; Emerging Artists Radar</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style=\'text-align:center; color:#8888aa; margin-top:-10px;\'>"
    f"<b>{artist_agg[\'artists\'].nunique():,}</b> emerging artists  &middot;  "
    f"<b>{len(emerging_tracks):,}</b> qualifying tracks</p>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="background:rgba(255,179,71,0.05); border-left:4px solid #ffb347;
                border-radius:8px; padding:12px 18px; color:#cccccc;
                font-size:0.88rem; margin-bottom:4px;">
        &#9888;&#65039; <b>Dataset note:</b> No <code>release_date</code> column available.
        <b>Emerging</b> = popularity &gt; <b>{pop_min}</b>
        AND fewer than <b>{max_tracks}</b> tracks in dataset.
        Adjust sidebar sliders to explore different thresholds.
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

if artist_agg.empty:
    st.warning("No emerging artists match the current filters. Try loosening the sidebar thresholds.")
    st.stop()

# ── KPI strip ─────────────────────────────────────────────────────────────────
top1 = artist_agg.iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("&#128640; Emerging Artists",      f"{artist_agg[\'artists\'].nunique():,}")
k2.metric("&#11088; Avg Breakout Score",     f"{artist_agg[\'breakout_score\'].mean():.3f}")
k3.metric("&#127928; Top Genre (emerging)",  artist_agg["dominant_genre"].mode()[0])
k4.metric("&#129351; #1 Breakout Artist",    top1["artists"])

st.markdown("<br>", unsafe_allow_html=True)

# ── #1 Breakout callout ───────────────────────────────────────────────────────
vs_sign  = "+" if top1["vs_genre_avg"] >= 0 else ""
vs_color = "#00e5a0" if top1["vs_genre_avg"] >= 0 else "#ff6b35"
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#0a1f2e 0%,#0d2845 100%);
                border:1px solid rgba(123,97,255,0.4); border-radius:14px;
                padding:20px 26px; margin-bottom:4px;">
        <div style="font-size:0.8rem; color:#8888aa; text-transform:uppercase;
                    letter-spacing:1px; margin-bottom:6px;">&#127942; #1 Breakout Artist</div>
        <div style="font-size:1.8rem; font-weight:700; color:#00e5a0; line-height:1.2;">{top1["artists"]}</div>
        <div style="font-size:1.1rem; color:#ffb347; font-weight:600;">Breakout Score: {top1["breakout_score"]:.4f}</div>
        <div style="font-size:0.92rem; color:#cccccc; margin-top:8px; line-height:1.6;">
            Genre: <b style="color:#00e5a0">{top1["dominant_genre"]}</b>
            &nbsp;&middot;&nbsp;
            Popularity: <b style="color:white">{top1["avg_popularity"]:.0f} / 100</b>
            &nbsp;&middot;&nbsp;
            vs genre avg: <b style="color:{vs_color}">{vs_sign}{top1["vs_genre_avg"]:.1f} pts</b><br>
            Energy: <b>{top1["avg_energy"]:.2f}</b>
            &nbsp;&middot;&nbsp;
            Danceability: <b>{top1["avg_danceability"]:.2f}</b>
            &nbsp;&middot;&nbsp;
            Est. Revenue: <b style="color:#00e5a0">${top1["total_revenue"]:,.2f}</b><br><br>
            <span style="color:#ffb347">Why?</span>
            Top on <b>Breakout Potential Score</b> = (popularity x danceability x energy) / 100.
            With only <b>{int(top1["track_count"])} track(s)</b> in the dataset, significant headroom to grow.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ── SECTION 1: Breakout bar + Popularity comparison ───────────────────────────
col_bp, col_cmp = st.columns(2, gap="large")

with col_bp:
    st.subheader("&#128293; Top 20 by Breakout Potential Score")
    top20 = artist_agg.head(20).sort_values("breakout_score", ascending=True)
    fig_bp = px.bar(
        top20, x="breakout_score", y="artists", orientation="h",
        text=top20["breakout_score"].apply(lambda v: f"{v:.3f}"),
        color="breakout_score",
        color_continuous_scale=[[0, "#0d1530"], [1, ACCENT]],
        hover_data={"artists": True, "breakout_score": ":.4f", "avg_popularity": ":.1f",
                    "dominant_genre": True, "avg_energy": ":.3f", "avg_danceability": ":.3f"},
        labels={"breakout_score": "Breakout Score", "artists": "Artist",
                "avg_popularity": "Avg Popularity", "dominant_genre": "Genre"},
    )
    fig_bp.update_traces(textposition="outside", textfont_color="#FFFFFF")
    fig_bp.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, top20["breakout_score"].max() * 1.22]),
    )
    dark_layout(fig_bp)
    st.plotly_chart(fig_bp, use_container_width=True)

with col_cmp:
    st.subheader("&#128202; Emerging Popularity vs Genre Average")
    top20_cmp = artist_agg.head(20).copy()
    cmp_df = pd.DataFrame({
        "Artist":    top20_cmp["artists"].tolist() * 2,
        "Popularity": top20_cmp["avg_popularity"].tolist() + top20_cmp["genre_avg_popularity"].tolist(),
        "Type":      (["Artist"] * len(top20_cmp)) + (["Genre Avg"] * len(top20_cmp)),
    })
    fig_cmp = px.bar(
        cmp_df, x="Popularity", y="Artist", color="Type", orientation="h", barmode="group",
        color_discrete_map={"Artist": ACCENT, "Genre Avg": "#7b61ff"},
        labels={"Popularity": "Popularity Score", "Artist": "Artist"},
        category_orders={"Artist": top20_cmp.sort_values("avg_popularity")["artists"].tolist()},
    )
    fig_cmp.update_layout(
        legend=dict(title="", orientation="h", yanchor="bottom", y=1.01, bgcolor="rgba(0,0,0,0)"),
    )
    dark_layout(fig_cmp)
    st.plotly_chart(fig_cmp, use_container_width=True)

st.divider()

# ── SECTION 2: Full sortable table ────────────────────────────────────────────
st.subheader("&#128203; Full Emerging Artists Table")
st.caption("Click any column header to sort  ·  Breakout Score = (popularity x danceability x energy) / 100")

display_df = artist_agg[[
    "artists", "dominant_genre", "track_count",
    "avg_popularity", "genre_avg_popularity", "vs_genre_avg",
    "avg_energy", "avg_danceability", "avg_valence",
    "total_revenue", "breakout_score",
]].copy()
display_df.columns = [
    "Artist", "Genre", "Tracks",
    "Avg Popularity", "Genre Avg Pop", "vs Genre Avg",
    "Avg Energy", "Avg Dance.", "Avg Valence",
    "Est. Revenue (USD)", "Breakout Score",
]
display_df = display_df.reset_index(drop=True)
display_df.index += 1

st.dataframe(
    display_df.style
        .format({
            "Avg Popularity":     "{:.1f}",
            "Genre Avg Pop":      "{:.1f}",
            "vs Genre Avg":       "{:+.1f}",
            "Avg Energy":         "{:.3f}",
            "Avg Dance.":         "{:.3f}",
            "Avg Valence":        "{:.3f}",
            "Est. Revenue (USD)": "${:,.2f}",
            "Breakout Score":     "{:.4f}",
        })
        .background_gradient(subset=["Breakout Score"], cmap="Greens")
        .background_gradient(subset=["vs Genre Avg"],   cmap="RdYlGn", vmin=-20, vmax=20),
    use_container_width=True,
    height=600,
)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  ·  "
    f"Emerging criteria: popularity > {pop_min}, tracks in dataset < {max_tracks}.  ·  "
    "No release_date column available in this dataset."
)
''')

print("\nAll 6 files written successfully.")
print("  utils/theme.py")
print("  app.py")
print("  pages/1_Executive_Overview.py")
print("  pages/2_Hit_Predictor.py")
print("  pages/3_Revenue_Intelligence.py")
print("  pages/4_Emerging_Artists_Radar.py")
