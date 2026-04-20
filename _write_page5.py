#!/usr/bin/env python3
"""_write_page5.py  --  Writes pages/5_Playlist_Curator.py"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "pages", "5_Playlist_Curator.py")

CONTENT = r'''"""
pages/5_Playlist_Curator.py
Playlist Intelligence Tool -- mood-based song picker with styled track cards.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io
import pandas as pd
import streamlit as st
from utils.theme import (
    apply_theme, sidebar_branding, inject_scroll_animations, hero_section,
    ACCENT, PALETTE, BG,
)

# ── Mood config: thresholds, colours, icons ────────────────────────────────────
MOOD_CFG = {
    "Hype":  {
        "emoji": "\U0001f525",
        "color": "#ff6b35",
        "glow":  "rgba(255,107,53,0.30)",
        "bg":    "rgba(255,107,53,0.06)",
        "border":"rgba(255,107,53,0.35)",
        "desc":  "High energy. Heavy tempo. Maximum euphoria.",
    },
    "Sad": {
        "emoji": "\U0001f622",
        "color": "#7b61ff",
        "glow":  "rgba(123,97,255,0.30)",
        "bg":    "rgba(123,97,255,0.06)",
        "border":"rgba(123,97,255,0.35)",
        "desc":  "Acoustic, melancholic, emotionally raw.",
    },
    "Focus": {
        "emoji": "\U0001f9e0",
        "color": "#4ecdc4",
        "glow":  "rgba(78,205,196,0.30)",
        "bg":    "rgba(78,205,196,0.06)",
        "border":"rgba(78,205,196,0.35)",
        "desc":  "Instrumental. Steady. Built for deep work.",
    },
    "Party": {
        "emoji": "\U0001f389",
        "color": "#00e5a0",
        "glow":  "rgba(0,229,160,0.30)",
        "bg":    "rgba(0,229,160,0.06)",
        "border":"rgba(0,229,160,0.35)",
        "desc":  "Danceability off the charts. Pure joy.",
    },
}

# ── Audio feature thresholds ───────────────────────────────────────────────────
def get_mood_mask(df: pd.DataFrame, mood: str) -> pd.Series:
    if mood == "Hype":
        return (df["energy"] > 0.8) & (df["tempo"] > 120) & (df["valence"] > 0.6)
    if mood == "Sad":
        return (df["valence"] < 0.35) & (df["energy"] < 0.5) & (df["acousticness"] > 0.5)
    if mood == "Focus":
        return (
            (df["instrumentalness"] > 0.3) &
            (df["tempo"].between(60, 100)) &
            (df["energy"].between(0.3, 0.6))
        )
    if mood == "Party":
        return (df["danceability"] > 0.75) & (df["energy"] > 0.7) & (df["valence"] > 0.65)
    return pd.Series([True] * len(df), index=df.index)


def build_why(row: pd.Series, mood: str) -> str:
    """Return a short HTML string explaining which features matched."""
    tags = []
    checks = {
        "Hype": [
            ("energy",          lambda v: v > 0.8,          "\u26a1 Energy",          f"{row.energy:.2f}",          "> 0.80"),
            ("tempo",           lambda v: v > 120,          "\U0001f941 Tempo",        f"{row.tempo:.0f} BPM",       "> 120"),
            ("valence",         lambda v: v > 0.6,          "\U0001f642 Valence",      f"{row.valence:.2f}",         "> 0.60"),
        ],
        "Sad": [
            ("valence",         lambda v: v < 0.35,         "\U0001f614 Valence",      f"{row.valence:.2f}",         "< 0.35"),
            ("energy",          lambda v: v < 0.5,          "\U0001f90d Energy",        f"{row.energy:.2f}",          "< 0.50"),
            ("acousticness",    lambda v: v > 0.5,          "\U0001f3b8 Acousticness", f"{row.acousticness:.2f}",    "> 0.50"),
        ],
        "Focus": [
            ("instrumentalness",lambda v: v > 0.3,          "\U0001f3bc Instrumental", f"{row.instrumentalness:.2f}","> 0.30"),
            ("tempo",           lambda v: 60 <= v <= 100,   "\u23f1 Tempo",            f"{row.tempo:.0f} BPM",       "60\u2013100"),
            ("energy",          lambda v: 0.3 <= v <= 0.6,  "\U0001f4a1 Energy",       f"{row.energy:.2f}",          "0.30\u20130.60"),
        ],
        "Party": [
            ("danceability",    lambda v: v > 0.75,         "\U0001f483 Danceability", f"{row.danceability:.2f}",    "> 0.75"),
            ("energy",          lambda v: v > 0.7,          "\u26a1 Energy",           f"{row.energy:.2f}",          "> 0.70"),
            ("valence",         lambda v: v > 0.65,         "\U0001f60d Valence",      f"{row.valence:.2f}",         "> 0.65"),
        ],
    }
    color = MOOD_CFG[mood]["color"]
    for feat, test, label, val, threshold in checks.get(mood, []):
        feat_val = getattr(row, feat, None)
        if feat_val is not None and test(feat_val):
            tags.append(
                f'<span style="display:inline-flex;align-items:center;gap:4px;'
                f'background:rgba(255,255,255,0.04);border:1px solid {color}44;'
                f'border-radius:6px;padding:3px 9px;font-size:0.75rem;color:{color};'
                f'font-weight:600;white-space:nowrap;">'
                f'\u2713 {label} <b style="color:#e0e0f0;">{val}</b>'
                f'<span style="color:#44445a;font-weight:400;">&nbsp;({threshold})</span>'
                f'</span>'
            )
    return " ".join(tags)


def feature_bar(label: str, value: float, color: str, fmt: str = ".2f") -> str:
    """Render a single mini progress bar row as HTML."""
    pct = min(max(value * 100, 0), 100)
    return (
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">'
        f'<span style="font-size:0.75rem;color:#55557a;width:92px;flex-shrink:0;'
        f'font-weight:500;">{label}</span>'
        f'<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:99px;'
        f'height:6px;overflow:hidden;">'
        f'<div style="width:{pct:.1f}%;height:100%;border-radius:99px;'
        f'background:linear-gradient(90deg,{color}88,{color});'
        f'transition:width 0.6s ease;"></div>'
        f'</div>'
        f'<span style="font-size:0.75rem;color:#7777a0;width:34px;text-align:right;'
        f'font-weight:600;">{value:{fmt}}</span>'
        f'</div>'
    )


def song_card(rank: int, row: pd.Series, mood: str, color: str) -> str:
    """Build the full HTML for one song card."""
    pop_pct = row.popularity
    track   = str(row.track_name)[:48] + ("..." if len(str(row.track_name)) > 48 else "")
    artist  = str(row.artists)[:40]   + ("..." if len(str(row.artists)) > 40 else "")
    why     = build_why(row, mood)

    bars = (
        feature_bar("Danceability", row.danceability, color)
        + feature_bar("Energy",      row.energy,       color)
        + feature_bar("Valence",     row.valence,      MOOD_CFG[mood]["color"])
    )
    # popularity arc
    pop_color = (
        "#00e5a0" if pop_pct >= 70 else
        "#ffb347" if pop_pct >= 40 else
        "#7b61ff"
    )

    return f"""
<div style="
    background:linear-gradient(145deg,#101020,#141430);
    border:1px solid {color}2a;
    border-left:3px solid {color};
    border-radius:18px;padding:20px 20px 16px;
    margin-bottom:14px;
    transition:transform 0.25s ease,box-shadow 0.25s ease;
    animation:fadeUp 0.6s ease {rank * 0.05:.2f}s both;
">
    <!-- header row -->
    <div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:14px;">
        <!-- rank -->
        <div style="
            min-width:32px;height:32px;border-radius:10px;
            background:{color}18;border:1px solid {color}44;
            display:flex;align-items:center;justify-content:center;
            font-size:0.78rem;font-weight:700;color:{color};flex-shrink:0;
        ">{rank:02d}</div>
        <!-- text -->
        <div style="flex:1;min-width:0;">
            <div style="font-size:0.97rem;font-weight:700;color:#e8e8f8;
                        line-height:1.25;word-break:break-word;">{track}</div>
            <div style="font-size:0.80rem;color:#6666aa;margin-top:3px;">{artist}</div>
        </div>
        <!-- popularity -->
        <div style="text-align:center;flex-shrink:0;">
            <div style="
                font-size:1.1rem;font-weight:800;color:{pop_color};
                line-height:1;">{pop_pct}</div>
            <div style="font-size:0.62rem;color:#44445a;text-transform:uppercase;
                        letter-spacing:0.6px;margin-top:2px;">POP</div>
        </div>
    </div>
    <!-- feature bars -->
    <div style="margin-bottom:13px;">{bars}</div>
    <!-- divider -->
    <div style="height:1px;background:rgba(255,255,255,0.04);margin-bottom:11px;"></div>
    <!-- why explainer -->
    <div>
        <div style="font-size:0.68rem;color:#33334a;text-transform:uppercase;
                    letter-spacing:0.9px;font-weight:600;margin-bottom:6px;">
            Why this song?
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:5px;">{why}</div>
    </div>
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Playlist Curator \u00b7 Spotify BI",
    page_icon="\U0001f3a7",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

# Extra page-level CSS
st.markdown("""
<style>
/* mood radio styled as big toggle cards */
div[data-testid="stRadio"] > label { display:none !important; }
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display:flex !important; gap:12px !important; flex-wrap:wrap;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    flex:1; min-width:130px; max-width:220px;
    display:flex !important; align-items:center; justify-content:center;
    flex-direction:column; gap:5px;
    padding:18px 14px;
    background:linear-gradient(145deg,#101020,#141430);
    border:2px solid rgba(255,255,255,0.08);
    border-radius:16px; cursor:pointer;
    transition:all 0.22s ease;
    font-size:1rem; font-weight:600; color:#7777a0;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
    display:none !important;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(1):has(input:checked) {
    border-color:#ff6b35aa !important; color:#ff6b35 !important;
    background:rgba(255,107,53,0.08) !important;
    box-shadow:0 0 20px rgba(255,107,53,0.15), 0 4px 0 0 #ff6b35;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(2):has(input:checked) {
    border-color:#7b61ffaa !important; color:#7b61ff !important;
    background:rgba(123,97,255,0.08) !important;
    box-shadow:0 0 20px rgba(123,97,255,0.15), 0 4px 0 0 #7b61ff;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(3):has(input:checked) {
    border-color:#4ecdc4aa !important; color:#4ecdc4 !important;
    background:rgba(78,205,196,0.08) !important;
    box-shadow:0 0 20px rgba(78,205,196,0.15), 0 4px 0 0 #4ecdc4;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(4):has(input:checked) {
    border-color:#00e5a0aa !important; color:#00e5a0 !important;
    background:rgba(0,229,160,0.08) !important;
    box-shadow:0 0 20px rgba(0,229,160,0.15), 0 4px 0 0 #00e5a0;
}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color:rgba(255,255,255,0.20) !important;
    background:rgba(255,255,255,0.04) !important;
    transform:translateY(-3px);
}
/* Download button */
div[data-testid="stDownloadButton"] button {
    background:linear-gradient(135deg,rgba(0,229,160,0.15),rgba(0,229,160,0.08)) !important;
    border:1px solid rgba(0,229,160,0.40) !important;
    color:#00e5a0 !important;
    border-radius:12px !important;
    font-weight:600 !important;
    font-size:0.90rem !important;
    padding:10px 22px !important;
    transition:all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background:rgba(0,229,160,0.22) !important;
    border-color:rgba(0,229,160,0.70) !important;
    transform:translateY(-2px);
    box-shadow:0 6px 20px rgba(0,229,160,0.20) !important;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0);    }
}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

# ── Sidebar ────────────────────────────────────────────────────────────────────
sidebar_branding()
st.sidebar.header("Curator Settings")
playlist_size = st.sidebar.slider("Playlist size", 5, 40, 10, step=5)
sort_col_map  = {
    "Popularity":   "popularity",
    "Danceability": "danceability",
    "Energy":       "energy",
    "Valence":      "valence",
}
sort_by = st.sidebar.selectbox("Sort results by", list(sort_col_map.keys()))
st.sidebar.markdown("---")
st.sidebar.caption("Matching songs are sorted by the chosen metric (descending).")

# ── Hero ───────────────────────────────────────────────────────────────────────
hero_section(subtitle="Playlist Curator \u00b7 Drop a mood, get a playlist")

# ── Mood selector ──────────────────────────────────────────────────────────────
st.markdown(
    "<h2 style='color:#e0e0f0;margin-bottom:6px;font-weight:700;'>"
    "\U0001f3a7 Pick Your Mood</h2>"
    "<p style='color:#55557a;font-size:0.88rem;margin-top:0;margin-bottom:18px;'>"
    "We\u2019ll match songs to your vibe using real audio features from Spotify.</p>",
    unsafe_allow_html=True,
)

mood_labels = [
    f"{MOOD_CFG[m]['emoji']} {m}" for m in ["Hype", "Sad", "Focus", "Party"]
]
selected_label = st.radio(
    "mood_radio",
    mood_labels,
    index=3,                      # default: Party
    horizontal=True,
    label_visibility="collapsed",
)
mood_key = selected_label.split(" ", 1)[1]  # strip emoji
cfg      = MOOD_CFG[mood_key]
color    = cfg["color"]

# ── Mood summary banner ────────────────────────────────────────────────────────
thresholds_html = {
    "Hype":  "Energy <b>&gt; 0.80</b> &nbsp;&middot;&nbsp; Tempo <b>&gt; 120 BPM</b> &nbsp;&middot;&nbsp; Valence <b>&gt; 0.60</b>",
    "Sad":   "Valence <b>&lt; 0.35</b> &nbsp;&middot;&nbsp; Energy <b>&lt; 0.50</b> &nbsp;&middot;&nbsp; Acousticness <b>&gt; 0.50</b>",
    "Focus": "Instrumentalness <b>&gt; 0.30</b> &nbsp;&middot;&nbsp; Tempo <b>60&#8211;100 BPM</b> &nbsp;&middot;&nbsp; Energy <b>0.30&#8211;0.60</b>",
    "Party": "Danceability <b>&gt; 0.75</b> &nbsp;&middot;&nbsp; Energy <b>&gt; 0.70</b> &nbsp;&middot;&nbsp; Valence <b>&gt; 0.65</b>",
}
st.markdown(
    f"""
    <div style="
        background:{cfg['bg']};
        border:1px solid {cfg['border']};
        border-left:4px solid {color};
        border-radius:14px;padding:16px 22px;
        margin:12px 0 24px;
    ">
        <div style="font-size:1.3rem;font-weight:800;color:{color};margin-bottom:4px;">
            {cfg['emoji']} {mood_key} Mode
        </div>
        <div style="font-size:0.84rem;color:#9999bb;">{cfg['desc']}</div>
        <div style="font-size:0.78rem;color:#55557a;margin-top:8px;">
            {thresholds_html[mood_key]}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Filter songs ───────────────────────────────────────────────────────────────
mask     = get_mood_mask(df, mood_key)
matches  = (
    df[mask]
    .sort_values(sort_col_map[sort_by], ascending=False)
    .drop_duplicates(subset=["track_name", "artists"])
    .head(playlist_size)
    .reset_index(drop=True)
)

# ── Stats row ──────────────────────────────────────────────────────────────────
total_matches = int(mask.sum())
st.markdown(
    f"""
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;align-items:center;">
        <div style="
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:12px;padding:10px 20px;text-align:center;
        ">
            <div style="font-size:1.4rem;font-weight:800;color:{color};">{total_matches:,}</div>
            <div style="font-size:0.70rem;color:#44445a;text-transform:uppercase;
                        letter-spacing:0.7px;font-weight:600;">matching songs</div>
        </div>
        <div style="
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:12px;padding:10px 20px;text-align:center;
        ">
            <div style="font-size:1.4rem;font-weight:800;color:#e0e0f0;">{playlist_size}</div>
            <div style="font-size:0.70rem;color:#44445a;text-transform:uppercase;
                        letter-spacing:0.7px;font-weight:600;">in playlist</div>
        </div>
        <div style="
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:12px;padding:10px 20px;text-align:center;
        ">
            <div style="font-size:1.4rem;font-weight:800;color:#e0e0f0;">
                {matches['popularity'].mean():.0f}
            </div>
            <div style="font-size:0.70rem;color:#44445a;text-transform:uppercase;
                        letter-spacing:0.7px;font-weight:600;">avg popularity</div>
        </div>
        <div style="
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-radius:12px;padding:10px 20px;text-align:center;
        ">
            <div style="font-size:1.4rem;font-weight:800;color:#e0e0f0;">
                {matches['energy'].mean():.2f}
            </div>
            <div style="font-size:0.70rem;color:#44445a;text-transform:uppercase;
                        letter-spacing:0.7px;font-weight:600;">avg energy</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if matches.empty:
    st.warning(
        f"No songs matched the {mood_key} filters with the current playlist size. "
        "Try increasing the playlist size in the sidebar."
    )
    st.stop()

# ── Song cards — 2 columns ─────────────────────────────────────────────────────
st.markdown(
    f"<h3 style='color:#e0e0f0;font-weight:700;margin-bottom:4px;'>"
    f"Your {mood_key} Playlist</h3>",
    unsafe_allow_html=True,
)
st.caption(f"Sorted by {sort_by} (descending) \u00b7 {len(matches)} tracks")

col_a, col_b = st.columns(2, gap="medium")
for i, row in matches.iterrows():
    rank = i + 1
    card = song_card(rank, row, mood_key, color)
    if rank % 2 == 1:
        col_a.markdown(card, unsafe_allow_html=True)
    else:
        col_b.markdown(card, unsafe_allow_html=True)

st.divider()

# ── Download button ────────────────────────────────────────────────────────────
export_cols = [
    "track_name", "artists", "track_genre",
    "popularity", "danceability", "energy", "valence",
    "tempo", "acousticness", "instrumentalness",
    "estimated_streams", "estimated_revenue_usd",
]
available_cols = [c for c in export_cols if c in matches.columns]
export_df = matches[available_cols].copy()
export_df.insert(0, "playlist_position", range(1, len(export_df) + 1))
export_df.columns = [
    c.replace("_", " ").title() for c in export_df.columns
]

csv_bytes = export_df.to_csv(index=False).encode("utf-8")

dl_col, info_col = st.columns([2, 5], gap="medium")
with dl_col:
    st.download_button(
        label=f"\u2193 Download {mood_key} Playlist CSV",
        data=csv_bytes,
        file_name=f"spotify_{mood_key.lower()}_playlist.csv",
        mime="text/csv",
        use_container_width=True,
    )
with info_col:
    st.markdown(
        """
        <div style="padding:10px 0;font-size:0.82rem;color:#55557a;line-height:1.6;">
            The exported CSV includes track name, artist, genre, audio features, and
            estimated stream data. Import it into Spotify via a playlist tool like
            <b style="color:#9999bb;">Soundiiz</b> or <b style="color:#9999bb;">TuneMyMusic</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ── Radar chart overview ───────────────────────────────────────────────────────
import plotly.graph_objects as go
from utils.theme import dark_layout, CHART_BG, GRID_COLOR

st.subheader(f"\U0001f4ca {mood_key} Playlist \u2014 Audio Feature Profile")
st.caption("Average audio feature values across all songs in your playlist.")

feat_cols = ["danceability", "energy", "valence", "acousticness", "instrumentalness"]
feat_avgs = [matches[f].mean() for f in feat_cols]
feat_labels = ["Danceability", "Energy", "Valence", "Acousticness", "Instrumentalness"]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=feat_avgs + [feat_avgs[0]],          # close the polygon
    theta=feat_labels + [feat_labels[0]],
    fill="toself",
    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
    line=dict(color=color, width=2.5),
    name=mood_key,
))
fig_radar.update_layout(
    polar=dict(
        bgcolor="rgba(255,255,255,0.02)",
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickfont=dict(color="#44445a", size=10),
            tickvals=[0.25, 0.5, 0.75, 1.0],
        ),
        angularaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickfont=dict(color="#9999bb", size=11),
        ),
    ),
    showlegend=False,
    margin=dict(t=40, b=40, l=60, r=60),
)
dark_layout(fig_radar)
fig_col, _ = st.columns([1, 1])
with fig_col:
    st.plotly_chart(fig_radar, use_container_width=True)
'''

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(CONTENT)
print(f"Wrote {TARGET}")
