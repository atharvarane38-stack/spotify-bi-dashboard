-- queries/top_tracks_by_genre.sql
-- Returns the top N most popular tracks per genre.

SELECT
    track_genre,
    track_name,
    artists,
    album_name,
    popularity,
    ROUND(duration_ms / 60000.0, 2) AS duration_min,
    explicit
FROM spotify_tracks
WHERE popularity > 50
ORDER BY track_genre, popularity DESC;
