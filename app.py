"""
app.py — Home / landing page for the Spotify BI multi-page app.
Navigate to pages via the sidebar.
"""

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify BI Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html(
    "<h1 style='text-align:center; color:#1DB954; font-size:2.5rem;'>"
    "🎵 Spotify Music Intelligence Dashboard</h1>")
st.html(
    "<p style='text-align:center; color:#aaaaaa;'>"
    "A multi-page BI analytics app built with Streamlit & Plotly.<br>"
    "Select a page from the <b>sidebar</b> to explore the data.</p>")
st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info("**📊 Page 1 — Executive Overview**\nKPIs, genre rankings, and popularity trends.")
with c2:
    st.info("**🎯 Page 2 — Hit Predictor**\nEnergy vs popularity scatter, correlation heatmap, and data insights.")
with c3:
    st.info("**🏆 Page 3 — Artist Deep Dive** *(coming soon)*\nTop artists, revenue, and track breakdowns.")
