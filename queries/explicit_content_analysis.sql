-- queries/explicit_content_analysis.sql
-- Compares average popularity between explicit and non-explicit tracks per genre.

SELECT
    track_genre,
    explicit,
    COUNT(*)                  AS track_count,
    ROUND(AVG(popularity), 2) AS avg_popularity,
    ROUND(AVG(energy), 4)     AS avg_energy,
    ROUND(AVG(danceability), 4) AS avg_danceability
FROM spotify_tracks
GROUP BY track_genre, explicit
ORDER BY track_genre, explicit;
