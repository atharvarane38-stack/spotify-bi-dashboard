"""
pages/1_Executive_Overview.py
─────────────────────────────
Page 1 of the Spotify Music Intelligence Dashboard.
Loads cleaned_spotify.csv and renders:
  • 4 KPI metric cards
  • Top 10 genres by average popularity (bar chart)
  • Track count by popularity score bracket (line chart)
    NOTE: The dataset has no release_date column, so a release-year
    trend is not possible. The popularity-bracket distribution is used
    as a substitute time-proxy insight.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Executive Overview · Spotify BI",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — tighten metric card borders ──────────────────────────────────
st.html(
    """
    <style>
    [data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #1DB954;
        border-radius: 10px;
        padding: 16px 20px;
    }
    [data-testid="stMetricLabel"]  { font-size: 0.85rem; color: #aaaaaa; }
    [data-testid="stMetricValue"]  { font-size: 1.6rem;  color: #FFFFFF; }
    [data-testid="stMetricDelta"]  { font-size: 0.8rem; }
    div[data-testid="stHorizontalBlock"] { gap: 1rem; }
    </style>
    """)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Plotly dark template helper ───────────────────────────────────────────────
PLOTLY_THEME = "plotly_dark"
CHART_BG     = "#1E1E1E"
SPOTIFY_GREEN = "#1DB954"


def dark_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_THEME,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(t=40, l=10, r=10, b=10),
        font=dict(color="#FFFFFF"),
    )
    return fig


# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image(
    "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png",
    use_container_width=True,
)
st.sidebar.markdown("---")
st.sidebar.header("Filters")

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)

pop_range = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

explicit_opt = st.sidebar.radio("Explicit content", ["All", "Explicit only", "Clean only"])

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]
if explicit_opt == "Explicit only":
    filtered = filtered[filtered["explicit"].astype(bool)]
elif explicit_opt == "Clean only":
    filtered = filtered[~filtered["explicit"].astype(bool)]

# ── Header ────────────────────────────────────────────────────────────────────
st.html(
    "<h1 style='text-align:center; color:#1DB954; font-size:2.2rem;'>"
    "🎵 Spotify Music Intelligence Dashboard</h1>")
st.html(
    "<p style='text-align:center; color:#aaaaaa; margin-top:-10px;'>"
    "Executive Overview · Powered by Kaggle Spotify Tracks Dataset</p>")
st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
total_tracks   = f"{len(filtered):,}"
total_artists  = f"{filtered['artists'].nunique():,}"
avg_popularity = f"{filtered['popularity'].mean():.1f} / 100"
total_revenue  = f"${filtered['estimated_revenue_usd'].sum():,.0f}"

k1, k2, k3, k4 = st.columns(4)
k1.metric("🎵 Total Tracks",          total_tracks)
k2.metric("🎤 Unique Artists",        total_artists)
k3.metric("⭐ Avg Popularity Score",  avg_popularity)
k4.metric("💰 Total Est. Revenue",    total_revenue)

st.html("<br>")

# ── Row 1: Genre popularity bar chart ─────────────────────────────────────────
col_bar, col_line = st.columns(2)

with col_bar:
    st.subheader("Top 10 Genres by Avg Popularity")
    genre_pop = (
        filtered.groupby("track_genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={"track_genre": "Genre", "popularity": "Avg Popularity"})
    )
    fig_bar = px.bar(
        genre_pop,
        x="Avg Popularity",
        y="Genre",
        orientation="h",
        text=genre_pop["Avg Popularity"].round(1),
        color="Avg Popularity",
        color_continuous_scale=[[0, "#0d5c2e"], [1, SPOTIFY_GREEN]],
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

# ── Row 1: Popularity-bracket track count line chart ─────────────────────────
with col_line:
    st.subheader("Track Count by Popularity Score")
    st.caption(
        "ℹ️ Dataset has no release date — showing popularity distribution trend instead."
    )
    bucket_size = 5
    bracket = (filtered["popularity"] // bucket_size * bucket_size).rename("popularity_bracket")
    bracket_counts = (
        bracket.value_counts()
        .sort_index()
        .reset_index()
        .rename(columns={"popularity_bracket": "Popularity Score", "count": "Track Count"})
    )
    fig_line = px.line(
        bracket_counts,
        x="Popularity Score",
        y="Track Count",
        markers=True,
        color_discrete_sequence=[SPOTIFY_GREEN],
        labels={"Popularity Score": "Popularity Score (0–100)", "Track Count": "Number of Tracks"},
    )
    fig_line.update_traces(line_width=2.5, marker_size=6)
    fig_line.update_xaxes(dtick=10)
    dark_layout(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Row 2: Mood breakdown + Explicit split ────────────────────────────────────
col_mood, col_exp = st.columns(2)

with col_mood:
    st.subheader("Mood Distribution")
    mood_counts = filtered["mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]
    color_map = {"Happy": "#1DB954", "Neutral": "#f9dc5c", "Sad": "#5b9bd5"}
    fig_mood = px.pie(
        mood_counts,
        values="Count",
        names="Mood",
        color="Mood",
        color_discrete_map=color_map,
        hole=0.45,
    )
    fig_mood.update_traces(textinfo="percent+label", textfont_size=13)
    dark_layout(fig_mood)
    st.plotly_chart(fig_mood, use_container_width=True)

with col_exp:
    st.subheader("Explicit vs Clean Tracks")
    explicit_counts = (
        filtered["explicit"]
        .astype(bool)
        .map({True: "Explicit", False: "Clean"})
        .value_counts()
        .reset_index()
    )
    explicit_counts.columns = ["Type", "Count"]
    fig_exp = px.bar(
        explicit_counts,
        x="Type",
        y="Count",
        color="Type",
        color_discrete_map={"Explicit": "#e63946", "Clean": SPOTIFY_GREEN},
        text="Count",
    )
    fig_exp.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_exp.update_layout(showlegend=False)
    dark_layout(fig_exp)
    st.plotly_chart(fig_exp, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks · Filtered view: {len(filtered):,} tracks · "
    "Source: Kaggle Spotify Tracks Dataset"
)
