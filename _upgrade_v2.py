#!/usr/bin/env python3
"""
_upgrade_v2.py  --  Rewrites utils/theme.py, app.py and all 4 pages with
glassmorphism / hero / glowing-KPI / button-sidebar / dark-chart styling.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def wr(rel, txt):
    full = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"  wrote  {rel}")


# ════════════════════════════════════════════════════════════════════════════
# utils/theme.py
# ════════════════════════════════════════════════════════════════════════════
wr("utils/theme.py", r'''"""utils/theme.py  -  shared design system for Spotify BI Dashboard."""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# ── Design tokens ─────────────────────────────────────────────────────────────
ACCENT      = "#00e5a0"
PALETTE     = ["#00e5a0", "#7b61ff", "#ff6b35", "#ffb347", "#4ecdc4", "#ff6b9d", "#c9a0dc"]
BG          = "#0a0a0f"
SURFACE     = "#10101e"
CHART_BG    = "#0a0a0f"
GRID_COLOR  = "#2a2a3a"
MOOD_COLORS = {"Happy": "#00e5a0", "Neutral": "#ffb347", "Sad": "#7b61ff"}

# ── Global CSS ─────────────────────────────────────────────────────────────────
_CSS = """<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&display=swap');

/* ── Base ── */
html, body, [class*="css"], .stMarkdown, .stText, p, span, div {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background-color: #0a0a0f !important;
    background-image:
        radial-gradient(ellipse 70% 45% at 5% 5%,  rgba(0,229,160,0.055) 0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 95% 95%, rgba(123,97,255,0.055) 0%, transparent 65%);
}

/* ── Keyframes ── */
@keyframes heroFadeIn {
    from { opacity:0; transform:translateY(32px); }
    to   { opacity:1; transform:translateY(0);    }
}
@keyframes gradientFlow {
    0%   { background-position: 0%   60%; }
    50%  { background-position: 100% 60%; }
    100% { background-position: 0%   60%; }
}
@keyframes glowBorderPulse {
    0%,100% { box-shadow: 0 4px 0 0 rgba(0,229,160,0.35), 0 0 18px rgba(0,229,160,0.08); }
    50%      { box-shadow: 0 4px 0 0 rgba(0,229,160,0.8),  0 0 32px rgba(0,229,160,0.18); }
}
@keyframes shimmerSlide {
    0%   { left: -80%; }
    100% { left: 120%;  }
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0);    }
}
@keyframes marqueeTicker {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}
@keyframes ping {
    75%,100% { transform:scale(2); opacity:0; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #070710 0%, #0a0a0f 60%, #0d0d1a 100%) !important;
    border-right: 1px solid rgba(0,229,160,0.10) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e0e0f0 !important; }

/* ── Metric cards  — dark glass + glowing bottom border ── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #101020 0%, #151528 100%) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-bottom: 4px solid rgba(0,229,160,0.0) !important;   /* overridden by animation */
    border-radius: 18px !important;
    padding: 22px 24px !important;
    position: relative;
    overflow: hidden;
    animation: glowBorderPulse 4s ease-in-out infinite;
    transition: transform 0.28s ease, box-shadow 0.28s ease;
}
/* shimmer sweep */
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    top: 0; left: -80%;
    width: 55%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.06), transparent);
    transform: skewX(-12deg);
    animation: shimmerSlide 4s ease-in-out infinite;
    pointer-events: none;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.025);
    box-shadow: 0 20px 40px rgba(0,229,160,0.13), 0 4px 0 0 #00e5a0 !important;
    border-color: rgba(0,229,160,0.45) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.80rem !important;
    color: #7777a0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

/* ── Charts ── */
.stPlotlyChart {
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: #0a0a0f !important;
    overflow: hidden;
    animation: fadeUp 0.7s ease forwards;
    transition: box-shadow 0.28s ease, transform 0.28s ease;
}
.stPlotlyChart:hover {
    box-shadow: 0 8px 30px rgba(0,229,160,0.10);
    transform: translateY(-2px);
}

/* ── DataFrames ── */
.stDataFrame, [data-testid="stDataFrameResizable"] {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    overflow: hidden !important;
    animation: fadeUp 0.8s ease forwards;
}

/* ── Headings ── */
h1,h2,h3 { font-family: 'DM Sans', sans-serif !important; }
h2 { animation: fadeUp 0.55s ease forwards; }

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(0,229,160,0.3), rgba(123,97,255,0.15), transparent) !important;
    margin: 1.6rem 0 !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(0,229,160,0.18) !important;
    background: rgba(0,229,160,0.025) !important;
}

/* ── Select box ── */
[data-baseweb="select"] > div:first-child {
    background: #10101e !important;
    border-color: rgba(0,229,160,0.25) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(0,229,160,0.55) !important;
}

/* ── Slider thumb ── */
[data-testid="stSlider"] [role="slider"] {
    background: #00e5a0 !important;
    box-shadow: 0 0 8px rgba(0,229,160,0.8) !important;
}
[data-testid="stSlider"] [data-testid="stSlider"] div[style*="background"] {
    background: rgba(0,229,160,0.25) !important;
}

/* ── Captions ── */
.stCaption, [data-testid="stCaptionContainer"] p { color: #44445a !important; font-size: 0.81rem; }

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    color: #9999bb !important;
    font-size: 0.88rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: rgba(0,229,160,0.25); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,229,160,0.5); }
</style>"""

# ── Scroll-reveal JS injected via hidden iframe ────────────────────────────────
_SCROLL_JS = """<script>
(function() {
    try {
        var doc = window.parent.document;
        var io = new IntersectionObserver(function(entries) {
            entries.forEach(function(e) {
                if (e.isIntersecting) {
                    e.target.style.opacity  = '1';
                    e.target.style.transform = 'translateY(0)';
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.06, rootMargin: '0px 0px -24px 0px' });
        function run() {
            doc.querySelectorAll('[data-testid="element-container"]').forEach(function(el, i) {
                if (el.dataset.srv2) return;
                el.style.opacity    = '0';
                el.style.transform  = 'translateY(22px)';
                el.style.transition = 'opacity 0.6s ease ' + (i % 8) * 0.07 + 's, transform 0.6s ease ' + (i % 8) * 0.07 + 's';
                el.dataset.srv2 = '1';
                io.observe(el);
            });
        }
        setTimeout(run, 350);
        setTimeout(run, 1100);
    } catch(ignore) {}
})();
</script>"""


def apply_theme() -> None:
    """Inject global CSS. Call once at the top of every page after set_page_config."""
    st.markdown(_CSS, unsafe_allow_html=True)


def inject_scroll_animations() -> None:
    """Inject JS scroll-reveal animation via a zero-height hidden component."""
    components.html(_SCROLL_JS, height=0, scrolling=False)


def hero_section(subtitle: str = "") -> None:
    """
    Render the animated glassmorphism hero banner.
    Inspired by the glassmorphism-trust-hero design pattern:
    - frosted glass card background
    - animated gradient heading
    - live stats ticker
    - glowing accent pings
    """
    stats_ticker_items = (
        "113,549 Tracks&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "114 Genres&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "Artists: 31,437&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "Avg Popularity: 33.2&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "Est. Revenue: $16.2M&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "Top Mood: Happy (42%)&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
        "Built with Streamlit &amp; Plotly&nbsp;&nbsp;&bull;&nbsp;&nbsp;"
    )
    sub_html = (
        f'<div style="font-size:1rem;color:#7777a0;margin-top:8px;font-weight:400;">{subtitle}</div>'
        if subtitle else ""
    )
    st.markdown(
        f"""
        <div style="
            position:relative; overflow:hidden;
            background:linear-gradient(135deg,rgba(16,16,32,0.92) 0%,rgba(10,10,25,0.95) 100%);
            border:1px solid rgba(0,229,160,0.14);
            border-radius:24px;
            padding:3rem 2.5rem 2.2rem;
            margin-bottom:2rem;
            backdrop-filter:blur(16px);
            -webkit-backdrop-filter:blur(16px);
        ">
            <!-- ambient blobs -->
            <div style="
                position:absolute;top:-80px;right:-80px;
                width:280px;height:280px;border-radius:50%;
                background:radial-gradient(circle,rgba(0,229,160,0.08) 0%,transparent 70%);
                pointer-events:none;">
            </div>
            <div style="
                position:absolute;bottom:-60px;left:-60px;
                width:220px;height:220px;border-radius:50%;
                background:radial-gradient(circle,rgba(123,97,255,0.07) 0%,transparent 70%);
                pointer-events:none;">
            </div>

            <!-- badge row -->
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
                <div style="
                    display:inline-flex;align-items:center;gap:7px;
                    border:1px solid rgba(0,229,160,0.22);
                    background:rgba(0,229,160,0.06);
                    border-radius:99px;padding:5px 14px;
                    font-size:0.72rem;font-weight:600;
                    color:#00e5a0;letter-spacing:1.2px;text-transform:uppercase;">
                    <span style="position:relative;display:inline-flex;width:8px;height:8px;">
                        <span style="
                            position:absolute;inset:0;border-radius:50%;
                            background:#00e5a0;opacity:0.7;
                            animation:ping 1.4s ease-in-out infinite;">
                        </span>
                        <span style="position:relative;width:8px;height:8px;border-radius:50%;background:#00e5a0;display:inline-block;"></span>
                    </span>
                    Live Analytics
                </div>
                <div style="
                    display:inline-flex;align-items:center;gap:6px;
                    border:1px solid rgba(255,179,71,0.22);
                    background:rgba(255,179,71,0.05);
                    border-radius:99px;padding:5px 14px;
                    font-size:0.72rem;font-weight:600;
                    color:#ffb347;letter-spacing:1.2px;text-transform:uppercase;">
                    &#9733; Portfolio Project
                </div>
            </div>

            <!-- heading -->
            <div style="
                font-size:clamp(1.9rem,4vw,2.9rem);
                font-weight:800;
                line-height:1.12;
                letter-spacing:-1.2px;
                background:linear-gradient(135deg,#00e5a0 0%,#7b61ff 45%,#00e5a0 100%);
                background-size:250% auto;
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
                background-clip:text;
                animation:gradientFlow 5s linear infinite, heroFadeIn 0.8s ease forwards;
                margin-bottom:10px;
            ">&#127925; Spotify Music Intelligence Dashboard</div>

            {sub_html}

            <!-- divider -->
            <div style="height:1px;
                background:linear-gradient(90deg,transparent,rgba(0,229,160,0.25),transparent);
                margin:20px 0 16px;">
            </div>

            <!-- stats ticker -->
            <div style="
                position:relative;overflow:hidden;
                mask-image:linear-gradient(to right,transparent,black 12%,black 88%,transparent);
                -webkit-mask-image:linear-gradient(to right,transparent,black 12%,black 88%,transparent);
            ">
                <div style="
                    display:inline-flex;white-space:nowrap;
                    animation:marqueeTicker 30s linear infinite;
                    font-size:0.78rem;color:#55557a;font-weight:500;
                ">
                    <span style="padding-right:60px;">{stats_ticker_items}</span>
                    <span style="padding-right:60px;">{stats_ticker_items}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dark_layout(fig: go.Figure, t: int = 40) -> go.Figure:
    """Apply consistent dark Plotly layout with #0a0a0f background and #2a2a3a gridlines."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(t=t, l=10, r=10, b=10),
        font=dict(color="#c0c0d8", family="DM Sans"),
        colorway=PALETTE,
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            linecolor=GRID_COLOR,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=GRID_COLOR,
            linecolor=GRID_COLOR,
        ),
    )
    return fig


def sidebar_branding(name: str = "Atharva") -> None:
    """Render unified sidebar: branding card + name + nav button links."""
    st.sidebar.markdown(
        f"""
        <style>
        .sb-card {{
            background: linear-gradient(145deg, #10101e, #161628);
            border: 1px solid rgba(0,229,160,0.20);
            border-radius: 18px;
            padding: 20px 16px 16px;
            margin-bottom: 16px;
            text-align: center;
        }}
        .sb-nav-btn {{
            display: block;
            width: 100%;
            margin: 5px 0;
            padding: 9px 14px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            color: #9999cc;
            font-size: 0.83rem;
            font-weight: 500;
            text-decoration: none;
            transition: background 0.2s, border-color 0.2s, color 0.2s;
            text-align: left;
        }}
        .sb-nav-btn:hover {{
            background: rgba(0,229,160,0.08);
            border-color: rgba(0,229,160,0.35);
            color: #00e5a0;
        }}
        .sb-link-row {{ display:flex; gap:8px; justify-content:center; margin-top:10px; }}
        .sb-ext-btn {{
            flex:1;
            padding:7px 0;
            border-radius:9px;
            text-align:center;
            font-size:0.78rem;
            font-weight:600;
            text-decoration:none;
            transition:all 0.2s;
        }}
        .sb-gh  {{ background:rgba(0,229,160,0.08); border:1px solid rgba(0,229,160,0.28); color:#00e5a0; }}
        .sb-li  {{ background:rgba(123,97,255,0.08); border:1px solid rgba(123,97,255,0.28); color:#7b61ff; }}
        .sb-gh:hover {{ background:rgba(0,229,160,0.18); }}
        .sb-li:hover {{ background:rgba(123,97,255,0.18); }}
        </style>

        <div class="sb-card">
            <div style="font-size:2rem;margin-bottom:4px;">&#127925;</div>
            <div style="font-size:1rem;font-weight:700;color:#00e5a0;letter-spacing:0.3px;">Spotify BI</div>
            <div style="font-size:0.72rem;color:#55557a;margin-top:3px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;">Music Intelligence Dashboard</div>
            <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,160,0.2),transparent);margin:12px 0 10px;"></div>
            <div style="font-size:0.80rem;color:#5a5a80;line-height:1.6;">
                Built by <b style="color:#c0c0d8;">{name}</b><br>
                <span style="color:#00e5a0;">113,549 tracks&nbsp;&middot;&nbsp;114 genres</span>
            </div>
            <div class="sb-link-row">
                <a class="sb-ext-btn sb-gh" href="https://github.com/" target="_blank">&#9671;&nbsp;GitHub</a>
                <a class="sb-ext-btn sb-li" href="https://linkedin.com/" target="_blank">in&nbsp;LinkedIn</a>
            </div>
        </div>

        <div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:1px;color:#33334a;margin:0 4px 6px;font-weight:600;">Pages</div>
        <a class="sb-nav-btn" href="/Executive_Overview">&#128202;&nbsp;&nbsp;Executive Overview</a>
        <a class="sb-nav-btn" href="/Hit_Predictor">&#127919;&nbsp;&nbsp;Hit Predictor</a>
        <a class="sb-nav-btn" href="/Revenue_Intelligence">&#128176;&nbsp;&nbsp;Revenue Intelligence</a>
        <a class="sb-nav-btn" href="/Emerging_Artists_Radar">&#128640;&nbsp;&nbsp;Emerging Artists Radar</a>
        <div style="height:1px;background:rgba(255,255,255,0.04);margin:12px 4px;"></div>
        """,
        unsafe_allow_html=True,
    )
''')

# ════════════════════════════════════════════════════════════════════════════
# app.py  — landing page
# ════════════════════════════════════════════════════════════════════════════
wr("app.py", '''"""app.py  --  Landing page."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.theme import apply_theme, sidebar_branding, inject_scroll_animations, hero_section

st.set_page_config(
    page_title="Spotify BI Dashboard",
    page_icon="\U0001f3b5",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()
sidebar_branding()

hero_section(subtitle="Interactive music intelligence for 113,549 Spotify tracks across 114 genres")

# ── page cards ──────────────────────────────────────────────────────────────
st.markdown(
    "<h3 style=\'color:#e0e0f0;margin-bottom:1rem;font-weight:700;\'>&#128194;&nbsp;Dashboard Pages</h3>",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "&#128202;", "Executive Overview",      "KPIs, genre rankings &amp; popularity distribution",         "#00e5a0"),
    (c2, "&#127919;", "Hit Predictor",           "Energy scatter, correlation heatmap &amp; audio insights",   "#7b61ff"),
    (c3, "&#128176;", "Revenue Intelligence",    "Top artists, genre revenue share &amp; sortable table",      "#ff6b35"),
    (c4, "&#128640;", "Emerging Artists Radar",  "Breakout scores &amp; popularity vs genre average",          "#ffb347"),
]
for col, icon, title, desc, color in cards:
    with col:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(145deg,#101020,#161628);
                border:1px solid {color}33;
                border-bottom:3px solid {color}88;
                border-radius:18px;padding:24px 18px;text-align:center;
                transition:transform 0.25s,box-shadow 0.25s;
                cursor:default;
            ">
                <div style="font-size:2rem;margin-bottom:10px;">{icon}</div>
                <div style="font-size:0.95rem;font-weight:700;color:{color};margin-bottom:8px;letter-spacing:0.2px;">{title}</div>
                <div style="font-size:0.78rem;color:#55557a;line-height:1.55;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── tech strip ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        background:rgba(255,255,255,0.02);
        border:1px solid rgba(255,255,255,0.06);
        border-radius:14px;padding:16px 24px;
        display:flex;gap:24px;flex-wrap:wrap;align-items:center;
    ">
        <span style="font-size:0.75rem;color:#33334a;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Built with</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;Streamlit</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;Plotly</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;Pandas</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;SQLite</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;Seaborn</span>
        <span style="font-size:0.82rem;color:#5a5a80;">&#9679;&nbsp;DM Sans font</span>
        <span style="font-size:0.82rem;color:#00e5a0;margin-left:auto;">Kaggle Spotify Tracks Dataset</span>
    </div>
    """,
    unsafe_allow_html=True,
)
''')

# ════════════════════════════════════════════════════════════════════════════
# pages/1_Executive_Overview.py
# ════════════════════════════════════════════════════════════════════════════
wr("pages/1_Executive_Overview.py", r'''"""Page 1 — Executive Overview."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, hero_section,
    ACCENT, PALETTE, CHART_BG, GRID_COLOR,
)

st.set_page_config(
    page_title="Executive Overview \u00b7 Spotify BI",
    page_icon="\U0001f3b5",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

sidebar_branding()
st.sidebar.header("Filters")
all_genres   = sorted(df["track_genre"].dropna().unique())
sel_genres   = st.sidebar.multiselect("Genre", all_genres, default=all_genres)
pop_range    = st.sidebar.slider("Popularity range", 0, 100, (0, 100))
explicit_opt = st.sidebar.radio("Explicit content", ["All", "Explicit only", "Clean only"])

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]
if explicit_opt == "Explicit only":
    filtered = filtered[filtered["explicit"].astype(bool)]
elif explicit_opt == "Clean only":
    filtered = filtered[~filtered["explicit"].astype(bool)]

hero_section(subtitle="Executive Overview \u00b7 Powered by Kaggle Spotify Tracks Dataset")

k1, k2, k3, k4 = st.columns(4)
k1.metric("\U0001f3b5 Total Tracks",        f"{len(filtered):,}")
k2.metric("\U0001f3a4 Unique Artists",      f"{filtered['artists'].nunique():,}")
k3.metric("\u2b50 Avg Popularity",          f"{filtered['popularity'].mean():.1f} / 100")
k4.metric("\U0001f4b0 Total Est. Revenue",  f"${filtered['estimated_revenue_usd'].sum():,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

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
        color_continuous_scale=[[0, "#0d1025"], [1, ACCENT]],
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#c0c0d8")
    fig_bar.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(range=[0, genre_pop["Avg Popularity"].max() * 1.18]),
    )
    dark_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_line:
    st.subheader("Track Count by Popularity Score")
    st.caption("No release date in dataset \u2014 showing popularity distribution instead.")
    bucket_size = 5
    bracket = (filtered["popularity"] // bucket_size * bucket_size).rename("popularity_bracket")
    bracket_counts = (
        bracket.value_counts().sort_index().reset_index()
        .rename(columns={"popularity_bracket": "Popularity Score", "count": "Track Count"})
    )
    fig_line = px.line(
        bracket_counts, x="Popularity Score", y="Track Count", markers=True,
        color_discrete_sequence=[ACCENT],
    )
    fig_line.update_traces(
        line_width=2.5, marker_size=6,
        fill="tozeroy",
        fillcolor="rgba(0,229,160,0.06)",
    )
    fig_line.update_xaxes(dtick=10)
    dark_layout(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

col_mood, col_exp = st.columns(2)

with col_mood:
    st.subheader("Mood Distribution")
    mood_counts = filtered["mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]
    color_map = {"Happy": "#00e5a0", "Neutral": "#ffb347", "Sad": "#7b61ff"}
    fig_mood = px.pie(
        mood_counts, values="Count", names="Mood",
        color="Mood", color_discrete_map=color_map, hole=0.48,
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
    f"Dataset: {len(df):,} total tracks  \u00b7  Filtered: {len(filtered):,} tracks  \u00b7  "
    "Source: Kaggle Spotify Tracks Dataset"
)
''')

# ════════════════════════════════════════════════════════════════════════════
# pages/2_Hit_Predictor.py
# ════════════════════════════════════════════════════════════════════════════
wr("pages/2_Hit_Predictor.py", r'''"""Page 2 — Hit Predictor."""
import io, os, sys
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
    inject_scroll_animations, hero_section,
    ACCENT, PALETTE, CHART_BG, GRID_COLOR, MOOD_COLORS,
)

HEATMAP_FEATURES = ["energy", "danceability", "valence", "tempo", "loudness", "popularity"]

st.set_page_config(
    page_title="Hit Predictor \u00b7 Spotify BI",
    page_icon="\U0001f3af",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

sidebar_branding()
st.sidebar.header("Filters")
all_genres = sorted(df["track_genre"].dropna().unique())
sel_genre  = st.sidebar.selectbox("Genre", ["All genres"] + all_genres)
pop_range  = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

filtered = df.copy()
if sel_genre != "All genres":
    filtered = filtered[filtered["track_genre"] == sel_genre]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

hero_section(
    subtitle=f"Hit Predictor  \u00b7  Analysing {len(filtered):,} tracks"
    + (f" in {sel_genre}" if sel_genre != "All genres" else " across all genres")
)

st.divider()

# ── Scatter ──────────────────────────────────────────────────────────────────
st.subheader("\u26a1 Energy vs Popularity by Mood")
st.caption("Each point is a track. Size = estimated streams.")

scatter_df = filtered.sample(min(5_000, len(filtered)), random_state=42)
fig_scatter = px.scatter(
    scatter_df, x="energy", y="popularity",
    color="mood", color_discrete_map=MOOD_COLORS,
    size="estimated_streams", size_max=18,
    hover_data={"track_name": True, "artists": True, "track_genre": True,
                "energy": ":.2f", "popularity": True,
                "estimated_streams": ":,", "mood": True},
    opacity=0.65,
    labels={"energy": "Energy (0\u20131)", "popularity": "Popularity Score", "mood": "Mood"},
    category_orders={"mood": ["Happy", "Neutral", "Sad"]},
)
fig_scatter.update_traces(marker=dict(line=dict(width=0.3, color="#111120")))
fig_scatter.update_layout(
    legend=dict(title="Mood", orientation="v",
                bgcolor="rgba(10,10,20,0.9)", bordercolor="#2a2a3a", borderwidth=1),
    xaxis=dict(range=[-0.02, 1.05]),
    yaxis=dict(range=[-2, 105]),
)
dark_layout(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── Heatmap + insight ─────────────────────────────────────────────────────────
col_heat, col_insight = st.columns([3, 2], gap="large")

with col_heat:
    st.subheader("\U0001f525 Audio Feature Correlation Matrix")
    corr = filtered[HEATMAP_FEATURES].corr()
    fig_heat, ax = plt.subplots(figsize=(7, 5))
    fig_heat.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
        vmin=-1, vmax=1, linewidths=0.5, linecolor="#1a1a2e",
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
    st.subheader("\U0001f4a1 Data Insight")
    HIGH_THRESHOLD = 0.7
    high_mask = (filtered["energy"] > HIGH_THRESHOLD) & (filtered["danceability"] > HIGH_THRESHOLD)
    high_pop  = filtered.loc[high_mask,  "popularity"].mean()
    rest_pop  = filtered.loc[~high_mask, "popularity"].mean()

    if rest_pop > 0 and not np.isnan(high_pop):
        pct_diff  = ((high_pop - rest_pop) / rest_pop) * 100
        direction = "higher" if pct_diff >= 0 else "lower"
        pct_label = f"{abs(pct_diff):.1f}%"
        high_count = int(high_mask.sum())
        insight_html = f"""
        <div style="background:linear-gradient(145deg,rgba(0,229,160,0.05),rgba(0,229,160,0.02));
                    border-left:4px solid #00e5a0; border-radius:12px;
                    padding:18px 20px; color:#d0d0e8; margin-top:8px;">
            <p style="font-size:1rem;font-weight:700;color:#00e5a0;margin-bottom:10px;">
                \U0001f3b5 High-Energy Dance Tracks
            </p>
            <p style="margin:0 0 10px;">
                Songs with <b>energy &gt; {HIGH_THRESHOLD}</b> and
                <b>danceability &gt; {HIGH_THRESHOLD}</b> score
                <b style="color:#00e5a0;font-size:1.15rem;">{pct_label}&nbsp;{direction}</b>
                popularity vs. other tracks.
            </p>
            <div style="height:1px;background:rgba(0,229,160,0.15);margin:10px 0;"></div>
            <p style="color:#55557a;font-size:0.83rem;margin:0;">
                Qualifying tracks:&nbsp;<b style="color:#c0c0d8;">{high_count:,}</b><br>
                Avg popularity (high E+D):&nbsp;<b style="color:#00e5a0;">{high_pop:.1f}</b><br>
                Avg popularity (others):&nbsp;&nbsp;<b style="color:#55557a;">{rest_pop:.1f}</b>
            </p>
        </div>"""
    else:
        insight_html = """<div style="background:rgba(0,229,160,0.03);
                border-left:4px solid rgba(0,229,160,0.3);border-radius:12px;padding:16px 20px;">
            <p style="color:#55557a;">Not enough data. Try selecting All genres.</p></div>"""

    st.markdown(insight_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("\U0001f4d0 Correlation with Popularity")
    corr_with_pop = (
        filtered[HEATMAP_FEATURES].corr()["popularity"].drop("popularity")
        .sort_values(key=abs, ascending=True).reset_index()
        .rename(columns={"index": "Feature", "popularity": "Pearson r"})
    )
    corr_with_pop["color"] = corr_with_pop["Pearson r"].apply(lambda v: ACCENT if v >= 0 else "#ff6b35")
    fig_corr = px.bar(
        corr_with_pop, x="Pearson r", y="Feature", orientation="h",
        color="color", color_discrete_map="identity",
        text=corr_with_pop["Pearson r"].apply(lambda v: f"{v:+.3f}"),
        range_x=[-1, 1],
    )
    fig_corr.add_vline(x=0, line_color=GRID_COLOR, line_width=1)
    fig_corr.update_traces(textposition="outside", textfont_color="white")
    fig_corr.update_layout(showlegend=False)
    dark_layout(fig_corr, t=20)
    st.plotly_chart(fig_corr, use_container_width=True)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  \u00b7  Filtered: {len(filtered):,} tracks  \u00b7  "
    "Scatter capped at 5,000 points."
)
''')

# ════════════════════════════════════════════════════════════════════════════
# pages/3_Revenue_Intelligence.py
# ════════════════════════════════════════════════════════════════════════════
wr("pages/3_Revenue_Intelligence.py", r'''"""Page 3 — Revenue Intelligence."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, hero_section,
    ACCENT, PALETTE, CHART_BG,
)

st.set_page_config(
    page_title="Revenue Intelligence \u00b7 Spotify BI",
    page_icon="\U0001f4b0",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

sidebar_branding()
st.sidebar.header("Filters")
all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)
pop_range  = st.sidebar.slider("Popularity range", 0, 100, (0, 100))

filtered = df[df["track_genre"].isin(sel_genres)]
filtered = filtered[filtered["popularity"].between(pop_range[0], pop_range[1])]

hero_section(subtitle=f"Revenue Intelligence  \u00b7  {len(filtered):,} tracks analysed")

# ── Aggregates ────────────────────────────────────────────────────────────────
artist_rev = (
    filtered.groupby("artists")
    .agg(total_revenue=("estimated_revenue_usd","sum"),
         track_count=("track_name","count"),
         avg_popularity=("popularity","mean"))
    .sort_values("total_revenue", ascending=False).reset_index()
)
genre_rev = (
    filtered.groupby("track_genre")["estimated_revenue_usd"]
    .sum().sort_values(ascending=False).reset_index()
    .rename(columns={"track_genre":"Genre","estimated_revenue_usd":"Revenue"})
)
total_rev     = filtered["estimated_revenue_usd"].sum()
top_artist    = artist_rev.iloc[0]["artists"] if len(artist_rev) else "N/A"
top_genre     = genre_rev.iloc[0]["Genre"]    if len(genre_rev)  else "N/A"
avg_track_rev = filtered["estimated_revenue_usd"].mean()
top_genre_rev = genre_rev.iloc[0]["Revenue"]  if len(genre_rev) else 0
avg_genre_rev = genre_rev["Revenue"].mean()    if len(genre_rev) else 1
genre_mult    = top_genre_rev / avg_genre_rev  if avg_genre_rev else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("\U0001f4b5 Total Est. Revenue",  f"${total_rev:,.0f}")
k2.metric("\U0001f947 Top Earning Artist",  top_artist)
k3.metric("\U0001f3b8 Top Earning Genre",   top_genre)
k4.metric("\U0001f4c0 Avg Rev / Track",     f"${avg_track_rev:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Callout ───────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#0d1025 0%,#10182a 100%);
                border:1px solid rgba(0,229,160,0.30);
                border-left:4px solid #00e5a0;
                border-radius:16px;padding:20px 26px;margin-bottom:4px;">
        <div style="font-size:2.6rem;font-weight:800;color:#00e5a0;line-height:1.0;">{genre_mult:.1f}&times;</div>
        <div style="font-size:0.9rem;color:#7777a0;margin-top:6px;">
            Top earning genre <b style="color:#00e5a0;">{top_genre}</b>
            earns <b style="color:#00e5a0;">{genre_mult:.1f}&times;</b> the average genre revenue
            &nbsp;&middot;&nbsp; Top:&nbsp;<b style="color:#c0c0d8;">${top_genre_rev:,.0f}</b>
            &nbsp;vs&nbsp; Avg:&nbsp;<b style="color:#55557a;">${avg_genre_rev:,.0f}</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

col_bar, col_pie = st.columns([3, 2], gap="large")

with col_bar:
    st.subheader("\U0001f3a4 Top 15 Artists by Estimated Revenue")
    top15 = artist_rev.head(15).copy()
    top15["label"] = top15["total_revenue"].apply(lambda v: f"${v:,.0f}")
    fig_bar = px.bar(
        top15, x="total_revenue", y="artists", orientation="h", text="label",
        color="total_revenue",
        color_continuous_scale=[[0, "#0d1025"], [1, ACCENT]],
        hover_data={"artists":True,"total_revenue":":,.0f","track_count":True,"avg_popularity":":.1f"},
        labels={"total_revenue":"Estimated Revenue (USD)","artists":"Artist"},
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#c0c0d8")
    fig_bar.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        xaxis=dict(range=[0, top15["total_revenue"].max() * 1.2]),
    )
    dark_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.subheader("\U0001f3b5 Revenue Share by Genre")
    TOP_N = 8
    top_genres_df = genre_rev.head(TOP_N).copy()
    other_rev = genre_rev.iloc[TOP_N:]["Revenue"].sum()
    if other_rev > 0:
        pie_df = pd.concat(
            [top_genres_df, pd.DataFrame([{"Genre":"Other","Revenue":other_rev}])],
            ignore_index=True)
    else:
        pie_df = top_genres_df
    pie_colors = list(PALETTE[:TOP_N]) + (["#333348"] if other_rev > 0 else [])
    fig_pie = px.pie(pie_df, values="Revenue", names="Genre",
                     color_discrete_sequence=pie_colors, hole=0.42)
    fig_pie.update_traces(textinfo="percent+label", textfont_size=12, pull=[0.03]*len(pie_df))
    fig_pie.update_layout(
        legend=dict(orientation="v", bgcolor="rgba(10,10,20,0.9)",
                    bordercolor="#2a2a3a", borderwidth=1),
        margin=dict(t=20,l=0,r=0,b=0),
    )
    dark_layout(fig_pie, t=20)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

st.subheader("\U0001f3c6 Top 20 Tracks by Est. Revenue")
st.caption("Click any column header to sort.")
top20 = (
    filtered[["track_name","artists","track_genre",
               "estimated_streams","estimated_revenue_usd","popularity"]]
    .sort_values("estimated_revenue_usd", ascending=False).head(20).reset_index(drop=True)
)
top20.index += 1
top20.columns = ["Track","Artist","Genre","Est. Streams","Est. Revenue (USD)","Popularity"]
st.dataframe(
    top20.style
        .format({"Est. Streams":"{:,.0f}","Est. Revenue (USD)":"${:,.2f}"})
        .background_gradient(subset=["Est. Revenue (USD)"], cmap="Greens"),
    use_container_width=True, height=560,
)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  \u00b7  Filtered: {len(filtered):,} tracks  \u00b7  "
    "Revenue = popularity \u00d7 1,000 streams \u00d7 $0.004."
)
''')

# ════════════════════════════════════════════════════════════════════════════
# pages/4_Emerging_Artists_Radar.py
# ════════════════════════════════════════════════════════════════════════════
wr("pages/4_Emerging_Artists_Radar.py", r'''"""Page 4 — Emerging Artists Radar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.theme import (
    apply_theme, dark_layout, sidebar_branding,
    inject_scroll_animations, hero_section,
    ACCENT, PALETTE, CHART_BG,
)

POP_THRESHOLD = 60
MAX_TRACKS    = 5

st.set_page_config(
    page_title="Emerging Artists Radar \u00b7 Spotify BI",
    page_icon="\U0001f680",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
inject_scroll_animations()

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned_spotify.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path, index_col=0)

df = load_data(DATA_PATH)

sidebar_branding()
st.sidebar.header("Filters")
pop_min = st.sidebar.slider("Min popularity threshold", 50, 90, POP_THRESHOLD, step=5)
max_tracks = st.sidebar.slider("Max tracks in dataset", 1, 10, MAX_TRACKS, step=1)
all_genres = sorted(df["track_genre"].dropna().unique())
sel_genres = st.sidebar.multiselect("Genre filter", all_genres, default=all_genres)

# ── Compute ───────────────────────────────────────────────────────────────────
track_counts       = df.groupby("artists")["track_name"].count()
low_volume_artists = track_counts[track_counts < max_tracks].index
emerging_tracks    = df[
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
    .sort_values("breakout_score", ascending=False).reset_index()
)
for col, dp in [("avg_popularity",1),("avg_danceability",3),("avg_energy",3),
                ("breakout_score",4),("total_revenue",2)]:
    artist_agg[col] = artist_agg[col].round(dp)

genre_avg_pop = df.groupby("track_genre")["popularity"].mean().to_dict()
artist_agg["genre_avg_popularity"] = artist_agg["dominant_genre"].map(genre_avg_pop).round(1)
artist_agg["vs_genre_avg"] = (artist_agg["avg_popularity"] - artist_agg["genre_avg_popularity"]).round(1)

hero_section(
    subtitle=f"Emerging Artists Radar  \u00b7  {artist_agg['artists'].nunique():,} artists  \u00b7  {len(emerging_tracks):,} qualifying tracks"
)

# ── Definition note ───────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="background:rgba(255,179,71,0.04);border-left:4px solid #ffb347;
                border-radius:10px;padding:12px 18px;color:#9999bb;
                font-size:0.87rem;margin-bottom:6px;">
        <b style="color:#ffb347;">\u26a0\ufe0f Dataset note:</b>
        No <code>release_date</code> column available.
        <b>Emerging</b> = popularity &gt; <b>{pop_min}</b>
        AND fewer than <b>{max_tracks}</b> tracks in the dataset.
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

if artist_agg.empty:
    st.warning("No emerging artists match the current filters. Try loosening the sidebar thresholds.")
    st.stop()

top1 = artist_agg.iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("\U0001f680 Emerging Artists",      f"{artist_agg['artists'].nunique():,}")
k2.metric("\u2b50 Avg Breakout Score",        f"{artist_agg['breakout_score'].mean():.3f}")
k3.metric("\U0001f3b8 Top Genre",             artist_agg["dominant_genre"].mode()[0])
k4.metric("\U0001f947 #1 Breakout Artist",    top1["artists"])

st.markdown("<br>", unsafe_allow_html=True)

# ── #1 Callout ────────────────────────────────────────────────────────────────
vs_color = "#00e5a0" if top1["vs_genre_avg"] >= 0 else "#ff6b35"
vs_sign  = "+" if top1["vs_genre_avg"] >= 0 else ""
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#0a1020 0%,#0f1830 100%);
                border:1px solid rgba(123,97,255,0.35);
                border-left:4px solid #7b61ff;
                border-radius:16px;padding:22px 28px;margin-bottom:4px;">
        <div style="font-size:0.72rem;color:#55557a;text-transform:uppercase;
                    letter-spacing:1.2px;margin-bottom:8px;">\U0001f3c6 #1 Breakout Artist</div>
        <div style="font-size:1.9rem;font-weight:800;color:#00e5a0;line-height:1.15;">{top1["artists"]}</div>
        <div style="font-size:1.05rem;color:#ffb347;font-weight:600;margin-top:2px;">
            Breakout Score:&nbsp;{top1["breakout_score"]:.4f}
        </div>
        <div style="font-size:0.90rem;color:#9999bb;margin-top:10px;line-height:1.7;">
            Genre:&nbsp;<b style="color:#00e5a0;">{top1["dominant_genre"]}</b>
            &nbsp;&middot;&nbsp;
            Popularity:&nbsp;<b style="color:#e0e0f0;">{top1["avg_popularity"]:.0f}/100</b>
            &nbsp;&middot;&nbsp;
            vs genre avg:&nbsp;<b style="color:{vs_color};">{vs_sign}{top1["vs_genre_avg"]:.1f}&nbsp;pts</b><br>
            Energy:&nbsp;<b>{top1["avg_energy"]:.2f}</b>
            &nbsp;&middot;&nbsp;
            Danceability:&nbsp;<b>{top1["avg_danceability"]:.2f}</b>
            &nbsp;&middot;&nbsp;
            Est. Revenue:&nbsp;<b style="color:#00e5a0;">${top1["total_revenue"]:,.2f}</b><br>
            <span style="color:#ffb347;">\u2728&nbsp;Why?&nbsp;</span>
            Top on <b>Breakout Score</b> = (popularity &times; danceability &times; energy) / 100.
            Only <b>{int(top1["track_count"])} track(s)</b> in dataset &mdash; significant headroom to grow.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

col_bp, col_cmp = st.columns(2, gap="large")

with col_bp:
    st.subheader("\U0001f525 Top 20 by Breakout Score")
    top20 = artist_agg.head(20).sort_values("breakout_score", ascending=True)
    fig_bp = px.bar(
        top20, x="breakout_score", y="artists", orientation="h",
        text=top20["breakout_score"].apply(lambda v: f"{v:.3f}"),
        color="breakout_score",
        color_continuous_scale=[[0, "#0d1025"], [1, ACCENT]],
        hover_data={"artists":True,"breakout_score":":.4f","avg_popularity":":.1f",
                    "dominant_genre":True,"avg_energy":":.3f","avg_danceability":":.3f"},
        labels={"breakout_score":"Breakout Score","artists":"Artist"},
    )
    fig_bp.update_traces(textposition="outside", textfont_color="#c0c0d8")
    fig_bp.update_layout(coloraxis_showscale=False,
                         xaxis=dict(range=[0, top20["breakout_score"].max() * 1.22]))
    dark_layout(fig_bp)
    st.plotly_chart(fig_bp, use_container_width=True)

with col_cmp:
    st.subheader("\U0001f4ca Popularity vs Genre Average")
    top20_cmp = artist_agg.head(20).copy()
    cmp_df = pd.DataFrame({
        "Artist":    top20_cmp["artists"].tolist() * 2,
        "Popularity": top20_cmp["avg_popularity"].tolist() + top20_cmp["genre_avg_popularity"].tolist(),
        "Type":      (["Artist"] * len(top20_cmp)) + (["Genre Avg"] * len(top20_cmp)),
    })
    fig_cmp = px.bar(
        cmp_df, x="Popularity", y="Artist", color="Type", orientation="h", barmode="group",
        color_discrete_map={"Artist": ACCENT, "Genre Avg": "#7b61ff"},
        category_orders={"Artist": top20_cmp.sort_values("avg_popularity")["artists"].tolist()},
    )
    fig_cmp.update_layout(
        legend=dict(title="", orientation="h", yanchor="bottom", y=1.01, bgcolor="rgba(0,0,0,0)"),
    )
    dark_layout(fig_cmp)
    st.plotly_chart(fig_cmp, use_container_width=True)

st.divider()

st.subheader("\U0001f4cb Full Emerging Artists Table")
st.caption("Click any column to sort  \u00b7  Breakout Score = (popularity \u00d7 danceability \u00d7 energy) / 100")
display_df = artist_agg[[
    "artists","dominant_genre","track_count",
    "avg_popularity","genre_avg_popularity","vs_genre_avg",
    "avg_energy","avg_danceability","avg_valence",
    "total_revenue","breakout_score",
]].copy()
display_df.columns = [
    "Artist","Genre","Tracks",
    "Avg Popularity","Genre Avg Pop","vs Genre Avg",
    "Avg Energy","Avg Dance.","Avg Valence",
    "Est. Revenue (USD)","Breakout Score",
]
display_df = display_df.reset_index(drop=True)
display_df.index += 1
st.dataframe(
    display_df.style
        .format({"Avg Popularity":"{:.1f}","Genre Avg Pop":"{:.1f}","vs Genre Avg":"{:+.1f}",
                 "Avg Energy":"{:.3f}","Avg Dance.":"{:.3f}","Avg Valence":"{:.3f}",
                 "Est. Revenue (USD)":"${:,.2f}","Breakout Score":"{:.4f}"})
        .background_gradient(subset=["Breakout Score"], cmap="Greens")
        .background_gradient(subset=["vs Genre Avg"],   cmap="RdYlGn", vmin=-20, vmax=20),
    use_container_width=True, height=600,
)

st.divider()
st.caption(
    f"Dataset: {len(df):,} total tracks  \u00b7  "
    f"Emerging: popularity > {pop_min}, tracks < {max_tracks}  \u00b7  "
    "No release_date available."
)
''')

print("\nAll 6 files written successfully.")
for f in ["utils/theme.py","app.py",
          "pages/1_Executive_Overview.py","pages/2_Hit_Predictor.py",
          "pages/3_Revenue_Intelligence.py","pages/4_Emerging_Artists_Radar.py"]:
    print(f"  {f}")
