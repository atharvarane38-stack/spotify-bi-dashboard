-- queries/analysis.sql
-- All SQL queries used in sql_analysis.py
-- Run against an in-memory SQLite database loaded from cleaned_spotify.csv
-- Table name: spotify
-- ─────────────────────────────────────────────────────────────────────────────


-- ── Query 1: Top 10 genres by average popularity score ───────────────────────
-- q1_top_genres_by_popularity.csv
SELECT
    track_genre,
    COUNT(*)                       AS track_count,
    ROUND(AVG(popularity), 2)      AS avg_popularity,
    ROUND(MIN(popularity), 2)      AS min_popularity,
    ROUND(MAX(popularity), 2)      AS max_popularity
FROM spotify
GROUP BY track_genre
ORDER BY avg_popularity DESC
LIMIT 10;


-- ── Query 2: Top 20 artists by total estimated revenue ───────────────────────
-- q2_top_artists_by_revenue.csv
SELECT
    artists,
    COUNT(*)                                AS track_count,
    ROUND(SUM(estimated_revenue_usd), 2)    AS total_revenue_usd,
    ROUND(AVG(estimated_revenue_usd), 2)    AS avg_revenue_usd,
    ROUND(AVG(popularity), 2)               AS avg_popularity
FROM spotify
GROUP BY artists
ORDER BY total_revenue_usd DESC
LIMIT 20;


-- ── Query 3: Avg audio features — top 100 vs bottom 100 by popularity ────────
-- q3_audio_features_top_vs_bottom.csv
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
) ranked
GROUP BY tier;


-- ── Query 4: Monthly release trends (tracks released per month/year) ─────────
-- NOTE: The Spotify Tracks dataset does not include a release_date column.
-- This query is provided as a reference template for datasets that do.
-- To use it, add a 'release_date' column (TEXT, format 'YYYY-MM-DD') to the table.
-- q4_monthly_release_trends.csv  ← skipped at runtime; column not available
SELECT
    SUBSTR(release_date, 1, 4)   AS release_year,
    SUBSTR(release_date, 6, 2)   AS release_month,
    COUNT(*)                     AS track_count
FROM spotify
WHERE release_date IS NOT NULL
GROUP BY release_year, release_month
ORDER BY release_year, release_month;


-- ── Query 5: Correlation between tempo and popularity by genre ────────────────
-- SQLite has no native CORR(). We compute Pearson r manually:
--   r = (n·Σxy − Σx·Σy) / SQRT((n·Σx²−(Σx)²) · (n·Σy²−(Σy)²))
-- q5_tempo_popularity_correlation_by_genre.csv
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
ORDER BY ABS(pearson_r_tempo_popularity) DESC;
