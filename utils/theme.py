"""utils/theme.py  -  shared design system for Spotify BI Dashboard."""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# ── Design tokens ─────────────────────────────────────────────────────────────
ACCENT      = "#1DB954"
PALETTE     = ["#1DB954", "#509BF5", "#ff6b35", "#ffb347", "#4ecdc4", "#ff6b9d", "#c9a0dc"]
BG          = "#121212"
SURFACE     = "#181818"
CHART_BG    = "#121212"
GRID_COLOR  = "#282828"
MOOD_COLORS = {"Happy": "#1DB954", "Neutral": "#ffb347", "Sad": "#509BF5"}

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
    background-color: #121212 !important;
    background-image:
        radial-gradient(ellipse 70% 45% at 5% 5%,  rgba(29,185,84,0.055) 0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 95% 95%, rgba(80,155,245,0.055) 0%, transparent 65%);
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
    0%,100% { box-shadow: 0 4px 0 0 rgba(29,185,84,0.35), 0 0 18px rgba(29,185,84,0.08); }
    50%      { box-shadow: 0 4px 0 0 rgba(29,185,84,0.8),  0 0 32px rgba(29,185,84,0.18); }
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
    background: linear-gradient(175deg, #0d0d0d 0%, #121212 60%, #161616 100%) !important;
    border-right: 1px solid rgba(29,185,84,0.10) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }

/* ── Metric cards  — dark glass + glowing bottom border ── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #181818 0%, #242424 100%) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-bottom: 4px solid rgba(29,185,84,0.0) !important;   /* overridden by animation */
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
    background: linear-gradient(90deg, transparent, rgba(29,185,84,0.06), transparent);
    transform: skewX(-12deg);
    animation: shimmerSlide 4s ease-in-out infinite;
    pointer-events: none;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.025);
    box-shadow: 0 20px 40px rgba(29,185,84,0.13), 0 4px 0 0 #1DB954 !important;
    border-color: rgba(29,185,84,0.45) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.80rem !important;
    color: #b3b3b3 !important;
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
    background: #121212 !important;
    overflow: hidden;
    animation: fadeUp 0.7s ease forwards;
    transition: box-shadow 0.28s ease, transform 0.28s ease;
}
.stPlotlyChart:hover {
    box-shadow: 0 8px 30px rgba(29,185,84,0.10);
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
    border: 1px solid rgba(29,185,84,0.18) !important;
    background: rgba(29,185,84,0.025) !important;
}

/* ── Select box ── */
[data-baseweb="select"] > div:first-child {
    background: #181818 !important;
    border-color: rgba(29,185,84,0.25) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(29,185,84,0.55) !important;
}

/* ── Slider thumb ── */
[data-testid="stSlider"] [role="slider"] {
    background: #1DB954 !important;
    box-shadow: 0 0 8px rgba(29,185,84,0.8) !important;
}
[data-testid="stSlider"] [data-testid="stSlider"] div[style*="background"] {
    background: rgba(29,185,84,0.25) !important;
}

/* ── Captions ── */
.stCaption, [data-testid="stCaptionContainer"] p { color: #727272 !important; font-size: 0.81rem; }

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    color: #b3b3b3 !important;
    font-size: 0.88rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #121212; }
::-webkit-scrollbar-thumb { background: rgba(29,185,84,0.25); border-radius: 99px; }
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
    st.html(_CSS)


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
        f'<div style="font-size:1rem;color:#b3b3b3;margin-top:8px;font-weight:400;">{subtitle}</div>'
        if subtitle else ""
    )
    st.html(
        f"""
        <div style="
            position:relative; overflow:hidden;
            background:linear-gradient(135deg,rgba(16,16,32,0.92) 0%,rgba(10,10,25,0.95) 100%);
            border:1px solid rgba(29,185,84,0.14);
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
                background:radial-gradient(circle,rgba(29,185,84,0.08) 0%,transparent 70%);
                pointer-events:none;">
            </div>
            <div style="
                position:absolute;bottom:-60px;left:-60px;
                width:220px;height:220px;border-radius:50%;
                background:radial-gradient(circle,rgba(80,155,245,0.07) 0%,transparent 70%);
                pointer-events:none;">
            </div>

            <!-- badge row -->
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
                <div style="
                    display:inline-flex;align-items:center;gap:7px;
                    border:1px solid rgba(29,185,84,0.22);
                    background:rgba(29,185,84,0.06);
                    border-radius:99px;padding:5px 14px;
                    font-size:0.72rem;font-weight:600;
                    color:#1DB954;letter-spacing:1.2px;text-transform:uppercase;">
                    <span style="position:relative;display:inline-flex;width:8px;height:8px;">
                        <span style="
                            position:absolute;inset:0;border-radius:50%;
                            background:#1DB954;opacity:0.7;
                            animation:ping 1.4s ease-in-out infinite;">
                        </span>
                        <span style="position:relative;width:8px;height:8px;border-radius:50%;background:#1DB954;display:inline-block;"></span>
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
                background:linear-gradient(135deg,#1DB954 0%,#509BF5 45%,#1DB954 100%);
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
                background:linear-gradient(90deg,transparent,rgba(29,185,84,0.25),transparent);
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
                    font-size:0.78rem;color:#727272;font-weight:500;
                ">
                    <span style="padding-right:60px;">{stats_ticker_items}</span>
                    <span style="padding-right:60px;">{stats_ticker_items}</span>
                </div>
            </div>
        </div>
        """)


def dark_layout(fig: go.Figure, t: int = 40) -> go.Figure:
    """Apply consistent dark Plotly layout with #121212 background and #282828 gridlines."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(t=t, l=10, r=10, b=10),
        font=dict(color="#e0e0e0", family="DM Sans"),
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
    st.sidebar.html(
        f"""
        <style>
        .sb-card {{
            background: linear-gradient(145deg, #181818, #242424);
            border: 1px solid rgba(29,185,84,0.20);
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
            color: #b3b3b3;
            font-size: 0.83rem;
            font-weight: 500;
            text-decoration: none;
            transition: background 0.2s, border-color 0.2s, color 0.2s;
            text-align: left;
        }}
        .sb-nav-btn:hover {{
            background: rgba(29,185,84,0.08);
            border-color: rgba(29,185,84,0.35);
            color: #1DB954;
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
        .sb-gh  {{ background:rgba(29,185,84,0.08); border:1px solid rgba(0,229,160,0.28); color:#1DB954; }}
        .sb-li  {{ background:rgba(80,155,245,0.08); border:1px solid rgba(80,155,245,0.28); color:#509BF5; }}
        .sb-gh:hover {{ background:rgba(29,185,84,0.18); }}
        .sb-li:hover {{ background:rgba(80,155,245,0.18); }}
        </style>

        <div class="sb-card">
            <div style="font-size:2rem;margin-bottom:4px;">&#127925;</div>
            <div style="font-size:1rem;font-weight:700;color:#1DB954;letter-spacing:0.3px;">Spotify BI</div>
            <div style="font-size:0.72rem;color:#727272;margin-top:3px;font-weight:500;text-transform:uppercase;letter-spacing:0.8px;">Music Intelligence Dashboard</div>
            <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,229,160,0.2),transparent);margin:12px 0 10px;"></div>
            <div style="font-size:0.80rem;color:#727272;line-height:1.6;">
                Built by <b style="color:#e0e0e0;">{name}</b><br>
                <span style="color:#1DB954;">113,549 tracks&nbsp;&middot;&nbsp;114 genres</span>
            </div>
            <div class="sb-link-row">
                <a class="sb-ext-btn sb-gh" href="https://github.com/" target="_blank">&#9671;&nbsp;GitHub</a>
                <a class="sb-ext-btn sb-li" href="https://linkedin.com/" target="_blank">in&nbsp;LinkedIn</a>
            </div>
        </div>

        <div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:1px;color:#535353;margin:0 4px 6px;font-weight:600;">Pages</div>
        <a class="sb-nav-btn" href="/Executive_Overview">&#128202;&nbsp;&nbsp;Executive Overview</a>
        <a class="sb-nav-btn" href="/Hit_Predictor">&#127919;&nbsp;&nbsp;Hit Predictor</a>
        <a class="sb-nav-btn" href="/Revenue_Intelligence">&#128176;&nbsp;&nbsp;Revenue Intelligence</a>
        <a class="sb-nav-btn" href="/Emerging_Artists_Radar">&#128640;&nbsp;&nbsp;Emerging Artists Radar</a>
        <a class="sb-nav-btn" href="/Playlist_Curator" style="border-color:rgba(29,185,84,0.18);">&#127911;&nbsp;&nbsp;Playlist Curator</a>
        <div style="height:1px;background:rgba(255,255,255,0.04);margin:12px 4px;"></div>
        """)
