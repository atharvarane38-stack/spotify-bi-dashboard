"""
pages/3_Revenue_Intelligence.py
────────────────────────────────
Page 3 of the Spotify Music Intelligence Dashboard.
Answers: "Who earns the most and where does the money go?"

Sections:
  • KPI strip: Total revenue, Top artist, Top genre, Avg per track
  • Metric callout: "Top earning genre makes Xx more than average"
  • Horizontal bar: Top 15 artists by estimated revenue
  • Pie chart: Revenue share by genre (top 8 + Other)
  • Sortable table: Top 20 tracks — Track, Artist, Genre, Streams, Revenue
"""

import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Intelligence · Spotify BI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
SPOTIFY_GREEN = "#1DB954"
CHART_BG      = "#1E1E1E"
PLOTLY_THEME  = "plotly_dark"

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
        background: linear-gradient(135deg, #0d3320 0%, #1a5c38 100%);
        border: 1px solid #1DB954;
        border-radius: 10px;
        padding: 18px 24px;
        margin-bottom: 8px;
    }
    .callout-number {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1DB954;
        line-height: 1.1;
    }
    .callout-label {
        font-size: 0.9rem;
        color: #aaaaaa;
        margin-top: 4px;
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

all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)

pop_range = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

# ── Page header ───────────────────────────────────────────────────────────────
st.html(
    "<h1 style='text-align:center; color:#1DB954; font-size:2.2rem;'>"
    "💰 Revenue Intelligence</h1>")
st.html(
    f"<p style='text-align:center; color:#aaaaaa; margin-top:-10px;'>"
    f"Analysing estimated streaming revenue across "
    f"<b>{len(filtered):,}</b> tracks</p>")
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
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"track_genre": "Genre", "estimated_revenue_usd": "Revenue"})
)

total_revenue   = filtered["estimated_revenue_usd"].sum()
top_artist      = artist_rev.iloc[0]["artists"] if len(artist_rev) else "—"
top_genre       = genre_rev.iloc[0]["Genre"]    if len(genre_rev)  else "—"
avg_track_rev   = filtered["estimated_revenue_usd"].mean()

# Genre multiple vs average
top_genre_rev   = genre_rev.iloc[0]["Revenue"]  if len(genre_rev) else 0
avg_genre_rev   = genre_rev["Revenue"].mean()    if len(genre_rev) else 1
genre_multiple  = top_genre_rev / avg_genre_rev  if avg_genre_rev else 0

# ── KPI strip ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("💵 Total Est. Revenue",    f"${total_revenue:,.0f}")
k2.metric("🥇 Top Earning Artist",    top_artist)
k3.metric("🎸 Top Earning Genre",     top_genre)
k4.metric("📀 Avg Revenue / Track",  f"${avg_track_rev:,.2f}")

st.html("<br>")

# ── Callout metric ────────────────────────────────────────────────────────────
st.html(
    f"""
    <div class="callout-box">
        <div class="callout-number">{genre_multiple:.1f}×</div>
        <div class="callout-label">
            Top earning genre (<b style="color:#1DB954">{top_genre}</b>)
            makes <b style="color:#1DB954">{genre_multiple:.1f}×</b> more
            than the average genre revenue
            &nbsp;·&nbsp;
            Top: <b>${top_genre_rev:,.0f}</b>
            &nbsp;vs&nbsp;
            Avg: <b>${avg_genre_rev:,.0f}</b>
        </div>
    </div>
    """)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Top 15 artists (bar) + Revenue share by genre (pie)
# ═════════════════════════════════════════════════════════════════════════════
col_bar, col_pie = st.columns([3, 2], gap="large")

with col_bar:
    st.subheader("🎤 Top 15 Artists by Estimated Revenue")

    top15 = artist_rev.head(15).copy()
    top15["label"] = top15["total_revenue"].apply(lambda v: f"${v:,.0f}")

    fig_bar = px.bar(
        top15,
        x="total_revenue",
        y="artists",
        orientation="h",
        text="label",
        color="total_revenue",
        color_continuous_scale=[[0, "#0d5c2e"], [1, SPOTIFY_GREEN]],
        hover_data={
            "artists":       True,
            "total_revenue": ":,.0f",
            "track_count":   True,
            "avg_popularity": ":.1f",
        },
        labels={
            "total_revenue":   "Estimated Revenue (USD)",
            "artists":         "Artist",
            "track_count":     "Tracks",
            "avg_popularity":  "Avg Popularity",
        },
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
    st.subheader("🎵 Revenue Share by Genre")

    # Top 8 genres + "Other"
    TOP_N = 8
    top_genres_df = genre_rev.head(TOP_N).copy()
    other_rev     = genre_rev.iloc[TOP_N:]["Revenue"].sum()
    if other_rev > 0:
        other_row = pd.DataFrame([{"Genre": "Other", "Revenue": other_rev}])
        pie_df = pd.concat([top_genres_df, other_row], ignore_index=True)
    else:
        pie_df = top_genres_df

    # Build a colour list: Spotify green for top, grey for Other
    palette = px.colors.sequential.Greens_r[:TOP_N]
    if other_rev > 0:
        palette = list(palette) + ["#555555"]

    fig_pie = px.pie(
        pie_df,
        values="Revenue",
        names="Genre",
        color_discrete_sequence=palette,
        hole=0.4,
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        textfont_size=12,
        pull=[0.03] * len(pie_df),
    )
    fig_pie.update_layout(
        legend=dict(
            orientation="v",
            bgcolor="rgba(30,30,30,0.8)",
            bordercolor="#444",
            borderwidth=1,
        ),
        margin=dict(t=20, l=0, r=0, b=0),
    )
    dark_layout(fig_pie, t=20)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Top 20 tracks table (sortable)
# ═════════════════════════════════════════════════════════════════════════════
st.subheader("🏆 Top 20 Tracks by Estimated Revenue")
st.caption("Click any column header to sort the table.")

top20_tracks = (
    filtered[["track_name", "artists", "track_genre",
               "estimated_streams", "estimated_revenue_usd", "popularity"]]
    .sort_values("estimated_revenue_usd", ascending=False)
    .head(20)
    .reset_index(drop=True)
)
top20_tracks.index += 1
top20_tracks.columns = ["Track", "Artist", "Genre",
                         "Est. Streams", "Est. Revenue (USD)", "Popularity"]

st.dataframe(
    top20_tracks.style
        .format({
            "Est. Streams":      "{:,.0f}",
            "Est. Revenue (USD)": "${:,.2f}",
        })
        .background_gradient(
            subset=["Est. Revenue (USD)"],
            cmap="Greens",
        ),
    use_container_width=True,
    height=560,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks · Filtered view: {len(filtered):,} tracks · "
    "Revenue estimated as popularity × 1,000 streams × $0.004 per stream."
)
