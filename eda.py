"""
eda.py — Spotify Tracks data cleaning & feature engineering
------------------------------------------------------------
Steps:
  1. Load CSV
  2. Check / clean nulls and duplicates
  3. Convert duration_ms → duration_min
  4. Engineer 'mood' column from valence
  5. Estimate revenue from popularity-derived stream count
  6. Save cleaned_spotify.csv
  7. Print dataset summary
"""

import os
import pandas as pd

# ── 1. Load ───────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "spotify_tracks.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "cleaned_spotify.csv")

df = pd.read_csv(DATA_PATH, index_col=0)
print(f"[load]   Rows: {len(df):,}  |  Columns: {df.shape[1]}")

# ── 2. Nulls & duplicates ─────────────────────────────────────────────────────
null_counts = df.isnull().sum()
total_nulls = null_counts.sum()

if total_nulls > 0:
    print(f"[clean]  Dropping {total_nulls:,} null value(s) across columns:")
    print(null_counts[null_counts > 0].to_string())
    df.dropna(inplace=True)
else:
    print("[clean]  No null values found.")

dupes_before = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"[clean]  Removed {dupes_before:,} duplicate row(s). Rows remaining: {len(df):,}")

# ── 3. duration_ms → duration_min ────────────────────────────────────────────
df["duration_min"] = (df["duration_ms"] / 60_000).round(4)
df.drop(columns=["duration_ms"], inplace=True)
print("[feat]   Converted duration_ms → duration_min (minutes, 4 d.p.)")

# ── 4. Mood column (based on valence) ────────────────────────────────────────
# valence > 0.6  → Happy
# valence < 0.4  → Sad
# 0.4–0.6        → Neutral
def classify_mood(v: float) -> str:
    if v > 0.6:
        return "Happy"
    elif v < 0.4:
        return "Sad"
    return "Neutral"

df["mood"] = df["valence"].apply(classify_mood)
print("[feat]   Created 'mood' column:")
print(df["mood"].value_counts().to_string(header=False))

# ── 5. Estimated revenue ──────────────────────────────────────────────────────
# The dataset has no explicit stream count. 'popularity' (0–100) is used as a
# proxy: estimated_streams = popularity * 1_000  (order-of-magnitude estimate).
# Revenue = estimated_streams × $0.004 (standard Spotify per-stream royalty).
STREAMS_PER_POPULARITY_POINT = 1_000
RATE_PER_STREAM = 0.004

df["estimated_streams"] = df["popularity"] * STREAMS_PER_POPULARITY_POINT
df["estimated_revenue_usd"] = (df["estimated_streams"] * RATE_PER_STREAM).round(2)
print(
    f"[feat]   Created 'estimated_streams' & 'estimated_revenue_usd' "
    f"(proxy: popularity × {STREAMS_PER_POPULARITY_POINT:,} × ${RATE_PER_STREAM})"
)

# ── 6. Save ───────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_PATH, index=True)
print(f"[save]   Cleaned dataset saved → {OUTPUT_PATH}")

# ── 7. Summary ────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print(f"\nShape          : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Genres         : {df['track_genre'].nunique()} unique genres")
print(f"Artists        : {df['artists'].nunique():,} unique artists")
print(f"Explicit tracks: {df['explicit'].sum():,}  "
      f"({df['explicit'].mean()*100:.1f}% of dataset)")

print("\n── Popularity ──")
print(df["popularity"].describe().round(2).to_string())

print("\n── Duration (min) ──")
print(df["duration_min"].describe().round(3).to_string())

print("\n── Mood distribution ──")
mood_pct = (df["mood"].value_counts() / len(df) * 100).round(1)
for mood, pct in mood_pct.items():
    print(f"  {mood:<8} {pct}%")

print("\n── Estimated Revenue (USD) ──")
print(df["estimated_revenue_usd"].describe().round(2).to_string())

print("\n── Top 5 tracks by estimated revenue ──")
top5 = (
    df[["track_name", "artists", "track_genre", "popularity", "estimated_revenue_usd"]]
    .sort_values("estimated_revenue_usd", ascending=False)
    .head(5)
)
print(top5.to_string(index=False))

print("\n── Sample of cleaned data (5 rows) ──")
print(df.head(5).to_string())
print("=" * 60)
