-- queries/audio_features_by_genre.sql
-- Aggregates average audio feature scores per genre, ordered by danceability.

SELECT
    track_genre,
    COUNT(*)                        AS track_count,
    ROUND(AVG(popularity), 2)       AS avg_popularity,
    ROUND(AVG(danceability), 4)     AS avg_danceability,
    ROUND(AVG(energy), 4)           AS avg_energy,
    ROUND(AVG(valence), 4)          AS avg_valence,
    ROUND(AVG(acousticness), 4)     AS avg_acousticness,
    ROUND(AVG(instrumentalness), 4) AS avg_instrumentalness,
    ROUND(AVG(liveness), 4)         AS avg_liveness,
    ROUND(AVG(speechiness), 4)      AS avg_speechiness,
    ROUND(AVG(tempo), 2)            AS avg_tempo,
    ROUND(AVG(loudness), 2)         AS avg_loudness,
    ROUND(AVG(duration_ms) / 60000.0, 2) AS avg_duration_min
FROM spotify_tracks
GROUP BY track_genre
ORDER BY avg_danceability DESC;
