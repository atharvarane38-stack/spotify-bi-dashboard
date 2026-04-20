"""
pages/2_Hit_Predictor.py
────────────────────────
Page 2 of the Spotify Music Intelligence Dashboard.
Answers: "What makes a hit?"

Sections:
  • Sidebar: genre dropdown filter
  • Scatter: Energy vs Popularity, coloured by Mood, sized by estimated_streams
  • Heatmap: Pearson correlation matrix of key audio features (seaborn)
  • Insight box: "Songs with high energy + high danceability score X% higher
    popularity on average" — X computed from actual filtered data
"""

import io
import os

import matplotlib
matplotlib.use("Agg")           # headless — no display needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hit Predictor · Spotify BI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared constants ──────────────────────────────────────────────────────────
SPOTIFY_GREEN = "#1DB954"
CHART_BG      = "#1E1E1E"
PLOTLY_THEME  = "plotly_dark"

MOOD_COLORS = {
    "Happy":   "#1DB954",
    "Neutral": "#f9dc5c",
    "Sad":     "#5b9bd5",
}

HEATMAP_FEATURES = [
    "energy", "danceability", "valence",
    "tempo", "loudness", "popularity",
]

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.html(
    """
    <style>
    [data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #1DB954;
        border-radius: 10px;
        padding: 16px 20px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.85rem; color: #aaaaaa; }
    [data-testid="stMetricValue"] { font-size: 1.6rem;  color: #FFFFFF; }
    .insight-box {
        background-color: #1a3326;
        border-left: 4px solid #1DB954;
        border-radius: 6px;
        padding: 16px 20px;
        font-size: 1rem;
        color: #e0e0e0;
        margin-top: 12px;
    }
    </style>
    """)

# ── Data loading ──────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Plotly dark helper ────────────────────────────────────────────────────────
def dark_layout(fig: go.Figure, t: int = 50) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_THEME,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(t=t, l=10, r=10, b=10),
        font=dict(color="#FFFFFF"),
    )
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png",
    use_container_width=True,
)
st.sidebar.markdown("---")
st.sidebar.header("Filters")

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genre  = st.sidebar.selectbox("Genre", ["All genres"] + all_genres)

pop_range = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

# Apply filters
filtered = df.copy()
if sel_genre != "All genres":
    filtered = filtered[filtered["track_genre"] == sel_genre]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

# ── Page header ───────────────────────────────────────────────────────────────
st.html(
    "<h1 style='text-align:center; color:#1DB954; font-size:2.2rem;'>"
    "🎯 Hit Predictor</h1>")
st.html(
    "<p style='text-align:center; color:#aaaaaa; margin-top:-10px;'>"
    f"Analysing <b>{len(filtered):,}</b> tracks"
    + (f" in <b>{sel_genre}</b>" if sel_genre != "All genres" else " across <b>all genres</b>")
    + "</p>")
st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Scatter: Energy vs Popularity coloured by Mood
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("⚡ Energy vs Popularity — by Mood")
st.caption(
    "Each point is a track. Size = estimated streams. "
    "Colour shows whether the track is Happy, Sad, or Neutral (based on valence)."
)

# Sample for performance when all genres selected
scatter_df = filtered.sample(min(5_000, len(filtered)), random_state=42)

fig_scatter = px.scatter(
    scatter_df,
    x="energy",
    y="popularity",
    color="mood",
    color_discrete_map=MOOD_COLORS,
    size="estimated_streams",
    size_max=18,
    hover_data={
        "track_name":          True,
        "artists":             True,
        "track_genre":         True,
        "energy":              ":.2f",
        "popularity":          True,
        "estimated_streams":   ":,",
        "mood":                True,
    },
    opacity=0.65,
    labels={
        "energy":     "Energy (0–1)",
        "popularity": "Popularity Score",
        "mood":       "Mood",
    },
    category_orders={"mood": ["Happy", "Neutral", "Sad"]},
)
fig_scatter.update_traces(marker=dict(line=dict(width=0.3, color="#333333")))
fig_scatter.update_layout(
    legend=dict(
        title="Mood",
        orientation="v",
        bgcolor="rgba(30,30,30,0.8)",
        bordercolor="#444",
        borderwidth=1,
    ),
    xaxis=dict(range=[-0.02, 1.05]),
    yaxis=dict(range=[-2, 105]),
)
dark_layout(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Heatmap + Insight box (side by side)
# ═════════════════════════════════════════════════════════════════════════════
col_heat, col_insight = st.columns([3, 2], gap="large")

# ── Correlation heatmap ───────────────────────────────────────────────────────
with col_heat:
    st.subheader("🔥 Audio Feature Correlation Matrix")

    corr = filtered[HEATMAP_FEATURES].corr()

    fig_heat, ax = plt.subplots(figsize=(7, 5))
    fig_heat.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        linecolor="#333333",
        annot_kws={"size": 10, "color": "white"},
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.tick_params(colors="white", labelsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", color="white")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color="white")

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white")

    plt.tight_layout()

    buf = io.BytesIO()
    fig_heat.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                     facecolor=CHART_BG)
    buf.seek(0)
    st.image(buf, use_container_width=True)
    plt.close(fig_heat)

# ── Computed insight box ──────────────────────────────────────────────────────
with col_insight:
    st.subheader("💡 Data Insight")

    # Define "high energy + high danceability" as both > 0.7
    HIGH_THRESHOLD = 0.7
    high_mask = (
        (filtered["energy"]       > HIGH_THRESHOLD) &
        (filtered["danceability"] > HIGH_THRESHOLD)
    )
    rest_mask = ~high_mask

    high_pop = filtered.loc[high_mask, "popularity"].mean()
    rest_pop = filtered.loc[rest_mask, "popularity"].mean()

    if rest_pop > 0 and not np.isnan(high_pop):
        pct_diff = ((high_pop - rest_pop) / rest_pop) * 100
        direction = "higher" if pct_diff >= 0 else "lower"
        pct_label = f"{abs(pct_diff):.1f}%"
        high_count = int(high_mask.sum())

        insight_html = f"""
        <div class="insight-box">
            <p style="font-size:1.05rem; font-weight:600; color:#1DB954; margin-bottom:8px;">
                🎵 High-Energy Dance Tracks
            </p>
            <p>
                Songs with <b>energy &gt; {HIGH_THRESHOLD}</b> and
                <b>danceability &gt; {HIGH_THRESHOLD}</b>
                score <b style="color:#1DB954; font-size:1.2rem;">{pct_label} {direction}</b>
                popularity on average compared to other tracks.
            </p>
            <hr style="border-color:#2a5a3a; margin: 10px 0;">
            <p style="color:#aaaaaa; font-size:0.85rem; margin:0;">
                High-energy dance tracks: <b style="color:white">{high_count:,}</b><br>
                Avg popularity (high E+D): <b style="color:#1DB954">{high_pop:.1f}</b><br>
                Avg popularity (others):   <b style="color:#aaaaaa">{rest_pop:.1f}</b>
            </p>
        </div>
        """
    else:
        insight_html = """
        <div class="insight-box">
            <p style="color:#aaaaaa;">
                Not enough data in the current filter to compute this insight.
                Try selecting "All genres" or widening the popularity range.
            </p>
        </div>
        """

    st.html(insight_html)

    st.html("<br>")

    # ── Bonus: feature importance bar mini-chart ──────────────────────────────
    st.subheader("📐 Feature Correlation with Popularity")
    corr_with_pop = (
        filtered[HEATMAP_FEATURES]
        .corr()["popularity"]
        .drop("popularity")
        .sort_values(key=abs, ascending=True)
        .reset_index()
        .rename(columns={"index": "Feature", "popularity": "Pearson r"})
    )
    corr_with_pop["color"] = corr_with_pop["Pearson r"].apply(
        lambda v: SPOTIFY_GREEN if v >= 0 else "#e63946"
    )
    fig_corr = px.bar(
        corr_with_pop,
        x="Pearson r",
        y="Feature",
        orientation="h",
        color="color",
        color_discrete_map="identity",
        text=corr_with_pop["Pearson r"].apply(lambda v: f"{v:+.3f}"),
        labels={"Pearson r": "Correlation with Popularity"},
        range_x=[-1, 1],
    )
    fig_corr.add_vline(x=0, line_color="#555555", line_width=1)
    fig_corr.update_traces(textposition="outside", textfont_color="white")
    fig_corr.update_layout(showlegend=False)
    dark_layout(fig_corr, t=20)
    st.plotly_chart(fig_corr, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks · Filtered view: {len(filtered):,} tracks · "
    "Scatter capped at 5,000 points for performance."
)
