CREATE TABLE song (
    song_id     VARCHAR(36),
    album_id    VARCHAR(36),

    song_name   VARCHAR(80),
    song_length INT,
    position    INT,

    grade       VARCHAR(1),
    comments    TEXT
);
