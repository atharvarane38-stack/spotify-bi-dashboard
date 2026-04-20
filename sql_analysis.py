"""
sql_analysis.py — SQLite in-memory analysis of cleaned Spotify data
--------------------------------------------------------------------
Loads cleaned_spotify.csv → in-memory SQLite DB ("spotify" table).
Runs 5 analytical queries and saves each result to results/.
Raw SQL is mirrored in queries/analysis.sql for GitHub reference.
"""

import os
import sqlite3
import textwrap
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(BASE_DIR, "data", "cleaned_spotify.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Load CSV → SQLite ─────────────────────────────────────────────────────────
print("[db]  Loading cleaned_spotify.csv into in-memory SQLite …")
df = pd.read_csv(DATA_PATH, index_col=0)
con = sqlite3.connect(":memory:")
df.to_sql("spotify", con, if_exists="replace", index=False)
print(f"[db]  Table 'spotify' ready — {len(df):,} rows, {df.shape[1]} columns\n")

# ── Helper ────────────────────────────────────────────────────────────────────
def run_query(label: str, sql: str, filename: str) -> pd.DataFrame:
    """Execute sql, print result, save to results/<filename>."""
    print(f"{'─'*60}")
    print(f"[q]  {label}")
    result = pd.read_sql_query(textwrap.dedent(sql), con)
    out_path = os.path.join(RESULTS_DIR, filename)
    result.to_csv(out_path, index=False)
    print(result.to_string(index=False))
    print(f"[✓]  Saved → {out_path}\n")
    return result

# ── Query 1: Top 10 genres by average popularity ──────────────────────────────
run_query(
    label    = "Top 10 genres by average popularity score",
    filename = "q1_top_genres_by_popularity.csv",
    sql      = """
        SELECT
            track_genre,
            COUNT(*)                       AS track_count,
            ROUND(AVG(popularity), 2)      AS avg_popularity,
            ROUND(MIN(popularity), 2)      AS min_popularity,
            ROUND(MAX(popularity), 2)      AS max_popularity
        FROM spotify
        GROUP BY track_genre
        ORDER BY avg_popularity DESC
        LIMIT 10
    """,
)

# ── Query 2: Top 20 artists by total estimated revenue ───────────────────────
run_query(
    label    = "Top 20 artists by total estimated revenue",
    filename = "q2_top_artists_by_revenue.csv",
    sql      = """
        SELECT
            artists,
            COUNT(*)                                AS track_count,
            ROUND(SUM(estimated_revenue_usd), 2)    AS total_revenue_usd,
            ROUND(AVG(estimated_revenue_usd), 2)    AS avg_revenue_usd,
            ROUND(AVG(popularity), 2)               AS avg_popularity
        FROM spotify
        GROUP BY artists
        ORDER BY total_revenue_usd DESC
        LIMIT 20
    """,
)

# ── Query 3: Audio features — top 100 vs bottom 100 by popularity ─────────────
run_query(
    label    = "Avg audio features: top 100 vs bottom 100 by popularity",
    filename = "q3_audio_features_top_vs_bottom.csv",
    sql      = """
        SELECT
            tier,
            ROUND(AVG(energy), 4)        AS avg_energy,
            ROUND(AVG(danceability), 4)  AS avg_danceability,
            ROUND(AVG(valence), 4)       AS avg_valence,
            ROUND(AVG(acousticness), 4)  AS avg_acousticness,
            ROUND(AVG(tempo), 2)         AS avg_tempo,
            ROUND(AVG(loudness), 2)      AS avg_loudness
        FROM (
            SELECT *, 'Top 100'    AS tier
            FROM (SELECT * FROM spotify ORDER BY popularity DESC LIMIT 100)
            UNION ALL
            SELECT *, 'Bottom 100' AS tier
            FROM (SELECT * FROM spotify ORDER BY popularity ASC  LIMIT 100)
        )
        GROUP BY tier
    """,
)

# ── Query 4: Monthly release trends ──────────────────────────────────────────
# The dataset has no release_date column — skip execution, log a clear note.
print("─" * 60)
print("[q]  Monthly release trends (tracks per month/year)")
print("[!]  SKIPPED — 'release_date' column not present in this dataset.")
print("     SQL template is available in queries/analysis.sql.\n")

# ── Query 5: Tempo ↔ Popularity Pearson correlation by genre ─────────────────
run_query(
    label    = "Pearson correlation: tempo vs popularity, by genre (min 30 tracks)",
    filename = "q5_tempo_popularity_correlation_by_genre.csv",
    sql      = """
        SELECT
            track_genre,
            COUNT(*)                                                              AS n,
            ROUND(AVG(tempo), 2)                                                  AS avg_tempo,
            ROUND(AVG(popularity), 2)                                             AS avg_popularity,
            ROUND(
                (COUNT(*) * SUM(tempo * popularity) - SUM(tempo) * SUM(popularity))
                / NULLIF(
                    SQRT(
                        (COUNT(*) * SUM(tempo * tempo) - SUM(tempo) * SUM(tempo)) *
                        (COUNT(*) * SUM(popularity * popularity) - SUM(popularity) * SUM(popularity))
                    ), 0
                ), 6
            ) AS pearson_r_tempo_popularity
        FROM spotify
        GROUP BY track_genre
        HAVING n >= 30
        ORDER BY ABS(pearson_r_tempo_popularity) DESC
    """,
)

# ── Wrap-up ───────────────────────────────────────────────────────────────────
con.close()
saved = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".csv")]
print("=" * 60)
print(f"Done. {len(saved)} result file(s) in results/:")
for f in sorted(saved):
    path = os.path.join(RESULTS_DIR, f)
    rows = sum(1 for _ in open(path)) - 1  # subtract header
    print(f"  {f}  ({rows} rows)")
print("=" * 60)
