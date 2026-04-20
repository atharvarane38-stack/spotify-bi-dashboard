"""
pages/4_Emerging_Artists_Radar.py
──────────────────────────────────
Page 4 of the Spotify Music Intelligence Dashboard.

"Emerging Artist" definition (dataset has no release_date column):
  • popularity > 60  (high resonance)
  • fewer than 5 tracks in the dataset  (not yet mainstream / high catalog volume)
  • These are artists punching above their weight relative to catalog size.

Sections:
  • Definition banner + dataset note
  • KPI strip: # emerging artists, avg breakout score, top genre, top artist
  • Callout: #1 Breakout Artist card
  • Bar chart: top 20 emerging artists by Breakout Potential Score
  • Bar chart: emerging avg popularity vs their genre average
  • Full sortable table with Breakout Score column
"""

import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Emerging Artists Radar · Spotify BI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
SPOTIFY_GREEN  = "#1DB954"
CHART_BG       = "#1E1E1E"
PLOTLY_THEME   = "plotly_dark"
POP_THRESHOLD  = 60
MAX_TRACKS     = 5

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
    [data-testid="stMetricValue"] { font-size: 1.5rem;  color: #FFFFFF; }
    .callout-box {
        background: linear-gradient(135deg, #0a1f2e 0%, #0d3348 100%);
        border: 1px solid #1a9bdc;
        border-radius: 10px;
        padding: 20px 26px;
        margin-bottom: 4px;
    }
    .callout-artist {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1DB954;
        line-height: 1.2;
    }
    .callout-score {
        font-size: 1.1rem;
        color: #f9dc5c;
        font-weight: 600;
    }
    .callout-body {
        font-size: 0.92rem;
        color: #cccccc;
        margin-top: 8px;
        line-height: 1.6;
    }
    .definition-box {
        background-color: #1a1a2e;
        border-left: 4px solid #f9dc5c;
        border-radius: 6px;
        padding: 12px 18px;
        font-size: 0.88rem;
        color: #cccccc;
        margin-bottom: 4px;
    }
    </style>
    """)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Plotly dark helper ────────────────────────────────────────────────────────
def dark_layout(fig: go.Figure, t: int = 40) -> go.Figure:
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

pop_min = st.sidebar.slider(
    "Min popularity threshold", 50, 90, POP_THRESHOLD, step=5,
    help="Artists must have at least one track above this popularity score."
)
max_tracks = st.sidebar.slider(
    "Max tracks in dataset", 1, 10, MAX_TRACKS, step=1,
    help="Artists with fewer than this many tracks are considered 'emerging'."
)
all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre filter", all_genres, default=all_genres)

# ── Compute emerging artists ──────────────────────────────────────────────────
track_counts = df.groupby("artists")["track_name"].count()
low_volume_artists = track_counts[track_counts < max_tracks].index

emerging_tracks = df[
    (df["popularity"] > pop_min) &
    (df["artists"].isin(low_volume_artists)) &
    (df["track_genre"].isin(sel_genres))
].copy()
emerging_tracks["breakout_score"] = (
    (emerging_tracks["popularity"] * emerging_tracks["danceability"] * emerging_tracks["energy"]) / 100
).round(4)

# Artist-level aggregation
artist_agg = (
    emerging_tracks.groupby("artists").agg(
        avg_popularity   = ("popularity",           "mean"),
        avg_danceability = ("danceability",         "mean"),
        avg_energy       = ("energy",               "mean"),
        avg_valence      = ("valence",              "mean"),
        total_revenue    = ("estimated_revenue_usd","sum"),
        track_count      = ("track_name",           "count"),
        dominant_genre   = ("track_genre",          lambda x: x.mode()[0]),
        breakout_score   = ("breakout_score",       "mean"),
    )
    .sort_values("breakout_score", ascending=False)
    .reset_index()
)
artist_agg["avg_popularity"]   = artist_agg["avg_popularity"].round(1)
artist_agg["avg_danceability"] = artist_agg["avg_danceability"].round(3)
artist_agg["avg_energy"]       = artist_agg["avg_energy"].round(3)
artist_agg["breakout_score"]   = artist_agg["breakout_score"].round(4)
artist_agg["total_revenue"]    = artist_agg["total_revenue"].round(2)

# Genre average popularity (from full dataset, for comparison)
genre_avg_pop = df.groupby("track_genre")["popularity"].mean().to_dict()
artist_agg["genre_avg_popularity"] = (
    artist_agg["dominant_genre"].map(genre_avg_pop).round(1)
)
artist_agg["vs_genre_avg"] = (
    artist_agg["avg_popularity"] - artist_agg["genre_avg_popularity"]
).round(1)

# ── Page header ───────────────────────────────────────────────────────────────
st.html(
    "<h1 style='text-align:center; color:#1DB954; font-size:2.2rem;'>"
    "🚀 Emerging Artists Radar</h1>")
st.html(
    f"<p style='text-align:center; color:#aaaaaa; margin-top:-10px;'>"
    f"<b>{artist_agg['artists'].nunique():,}</b> emerging artists identified · "
    f"<b>{len(emerging_tracks):,}</b> qualifying tracks</p>")

# Definition banner
st.html(
    f"""
    <div class="definition-box">
        ⚠️ <b>Dataset note:</b> This dataset has no <code>release_date</code> column,
        so the "last 2 years" filter cannot be applied directly.
        <b>Emerging artist</b> is defined here as:
        popularity &gt; <b>{pop_min}</b>
        AND fewer than <b>{max_tracks}</b> tracks in the dataset (not yet high catalog volume).
        Adjust the sidebar sliders to explore different thresholds.
    </div>
    """)
st.divider()

if artist_agg.empty:
    st.warning("No emerging artists match the current filters. Try loosening the sidebar thresholds.")
    st.stop()

# ── KPI strip ─────────────────────────────────────────────────────────────────
top1 = artist_agg.iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("🚀 Emerging Artists",       f"{artist_agg['artists'].nunique():,}")
k2.metric("⭐ Avg Breakout Score",      f"{artist_agg['breakout_score'].mean():.3f}")
k3.metric("🎸 Top Genre (emerging)",   artist_agg["dominant_genre"].mode()[0])
k4.metric("🥇 #1 Breakout Artist",     top1["artists"])

st.html("<br>")

# ── #1 Breakout Callout ───────────────────────────────────────────────────────
vs_sign = "+" if top1["vs_genre_avg"] >= 0 else ""
st.html(
    f"""
    <div class="callout-box">
        <div style="font-size:0.8rem; color:#aaaaaa; text-transform:uppercase;
                    letter-spacing:1px; margin-bottom:6px;">🏆 #1 Breakout Artist</div>
        <div class="callout-artist">{top1["artists"]}</div>
        <div class="callout-score">Breakout Score: {top1["breakout_score"]:.4f}</div>
        <div class="callout-body">
            Genre: <b style="color:#1DB954">{top1["dominant_genre"]}</b>
            &nbsp;·&nbsp;
            Popularity: <b style="color:white">{top1["avg_popularity"]:.0f} / 100</b>
            &nbsp;·&nbsp;
            vs genre avg: <b style="color:{'#1DB954' if top1['vs_genre_avg'] >= 0 else '#e63946'}">
                {vs_sign}{top1["vs_genre_avg"]:.1f} pts</b><br>
            Energy: <b>{top1["avg_energy"]:.2f}</b>
            &nbsp;·&nbsp;
            Danceability: <b>{top1["avg_danceability"]:.2f}</b>
            &nbsp;·&nbsp;
            Est. Revenue: <b style="color:#1DB954">${top1["total_revenue"]:,.2f}</b><br><br>
            <span style="color:#f9dc5c">Why?</span>
            This artist scores top on <b>Breakout Potential Score</b>
            = (popularity × danceability × energy) / 100,
            combining raw popularity with the audio qualities that drive
            repeat plays — energy and danceability.
            With only <b>{int(top1["track_count"])} track(s)</b> in the dataset,
            they have significant headroom to grow.
        </div>
    </div>
    """)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Breakout Score bar + Popularity vs genre avg bar (side by side)
# ═════════════════════════════════════════════════════════════════════════════
col_bp, col_cmp = st.columns(2, gap="large")

with col_bp:
    st.subheader("🔥 Top 20 by Breakout Potential Score")
    top20 = artist_agg.head(20).sort_values("breakout_score", ascending=True)
    fig_bp = px.bar(
        top20,
        x="breakout_score",
        y="artists",
        orientation="h",
        text=top20["breakout_score"].apply(lambda v: f"{v:.3f}"),
        color="breakout_score",
        color_continuous_scale=[[0, "#0d5c2e"], [1, SPOTIFY_GREEN]],
        hover_data={
            "artists":         True,
            "breakout_score":  ":.4f",
            "avg_popularity":  ":.1f",
            "dominant_genre":  True,
            "avg_energy":      ":.3f",
            "avg_danceability":":.3f",
        },
        labels={
            "breakout_score":  "Breakout Score",
            "artists":         "Artist",
            "avg_popularity":  "Avg Popularity",
            "dominant_genre":  "Genre",
        },
    )
    fig_bp.update_traces(textposition="outside", textfont_color="#FFFFFF")
    fig_bp.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(range=[0, top20["breakout_score"].max() * 1.22]),
    )
    dark_layout(fig_bp)
    st.plotly_chart(fig_bp, use_container_width=True)

with col_cmp:
    st.subheader("📊 Emerging Popularity vs Genre Average")
    top20_cmp = artist_agg.head(20).copy()

    # Melt for grouped bar
    cmp_df = pd.DataFrame({
        "Artist":          top20_cmp["artists"].tolist() * 2,
        "Popularity":      top20_cmp["avg_popularity"].tolist() +
                           top20_cmp["genre_avg_popularity"].tolist(),
        "Type":            (["Artist"] * len(top20_cmp)) +
                           (["Genre Avg"] * len(top20_cmp)),
    })

    fig_cmp = px.bar(
        cmp_df,
        x="Popularity",
        y="Artist",
        color="Type",
        orientation="h",
        barmode="group",
        color_discrete_map={"Artist": SPOTIFY_GREEN, "Genre Avg": "#5b9bd5"},
        labels={"Popularity": "Popularity Score", "Artist": "Artist"},
        category_orders={"Artist": top20_cmp.sort_values("avg_popularity")["artists"].tolist()},
    )
    fig_cmp.update_layout(
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom", y=1.01,
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    dark_layout(fig_cmp)
    st.plotly_chart(fig_cmp, use_container_width=True)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Full sortable table
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("📋 Full Emerging Artists Table")
st.caption("Click any column header to sort · Breakout Score = (popularity × danceability × energy) / 100")

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
            "Avg Popularity":    "{:.1f}",
            "Genre Avg Pop":     "{:.1f}",
            "vs Genre Avg":      "{:+.1f}",
            "Avg Energy":        "{:.3f}",
            "Avg Dance.":        "{:.3f}",
            "Avg Valence":       "{:.3f}",
            "Est. Revenue (USD)":"${:,.2f}",
            "Breakout Score":    "{:.4f}",
        })
        .background_gradient(subset=["Breakout Score"], cmap="Greens")
        .background_gradient(subset=["vs Genre Avg"],   cmap="RdYlGn", vmin=-20, vmax=20),
    use_container_width=True,
    height=600,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks · "
    f"Emerging criteria: popularity > {pop_min}, tracks in dataset < {max_tracks}. "
    "No release_date column available in this dataset."
)
