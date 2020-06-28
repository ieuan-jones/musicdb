CREATE VIEW
    v_percentage
AS
SELECT
    album.artist_id,
    album.album_id,

    artist_name,
    album_name,
    
    star,
    total,
    album.rating,
    star/(total*4.0)*100 AS percentage,

    release_date
FROM
    album
JOIN (
    SELECT
        artist_name,
        album.album_id,
        SUM(
            CASE
                WHEN grade='*' THEN 4
                WHEN grade='A' THEN 3
                WHEN grade='B' THEN 2
                WHEN grade='C' THEN 1
            END) AS star,
        COUNT(*) AS total,
        rating
    FROM
        song
    JOIN album
        ON song.album_id = album.album_id
    JOIN artist
        ON album.artist_id = artist.artist_id
    GROUP BY
        artist_name,
        album.album_id,
        rating
) AS sub
    ON album.album_id = sub.album_id
WHERE
    album.rating IS NOT NULL
ORDER BY percentage DESC
;
