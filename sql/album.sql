CREATE TABLE album (
    album_id          VARCHAR(36),
    artist_id         VARCHAR(36),

    album_name        VARCHAR(80),
    format            VARCHAR(8),
    release_date      DATE,

    first_listen      DATE,
    rating            INT,
    comments          TEXT,

    pitchfork         VARCHAR(3),
    metacritic        VARCHAR(3),
    fantano           VARCHAR(12),

    background_colour VARCHAR(6),
    foreground_colour VARCHAR(6)
);
