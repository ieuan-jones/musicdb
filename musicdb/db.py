import traceback
import psycopg2
import psycopg2.extras
import uuid

schema_history = [
    {
        'version': 3,
        'scripts': [
            'v_percentage.sql'
        ]
    },
    {
        'version': 2,
        'scripts': [
            'genre.sql'
        ]
    },
    {
        'version': 1,
        'scripts': [
            'schema.sql',
            'album.sql',
            'song.sql',
            'artist.sql'
        ]
    }
]

'''def connect():
    #Connect to postgres instance running in local docker container.
    #Return: database connection, schema version of database

    # Only local development variables, please no one get too excited!
    conn = psycopg2.connect('host=localhost dbname=postgres user=postgres password=docker')

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema;')
        records = cursor.fetchall()

        return records[0][0]
    except psycopg2.errors.UndefinedTable:
        # The database hasn't been set up for the first time yet
        conn.rollback()
        return 1
    finally:
        cursor.close()
        conn.close()
    
    return version'''

def connect_db():
    conn = psycopg2.connect('host=localhost dbname=musicdb user=postgres password=docker')

    return conn

def close_db(conn):
    conn.close()

def get_schema_version(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema;')
        records = cursor.fetchall()

        return records[0][0]
    except psycopg2.errors.UndefinedTable:
        # The database hasn't been set up for the first time yet
        conn.rollback()
        return -1
    finally:
        cursor.close()

def initialise_db(conn):
    # Now set up the database. We'll do this by applying every version
    # sequentially for the history of the project
    cursor = conn.cursor()
    version = get_schema_version(conn)

    for schema in schema_history[::-1]:
        if schema['version'] > version:
            for script in schema['scripts']:
                with open(f'sql/{script}', 'r') as schema_file:    
                    sql = schema_file.read()
                try:
                    cursor.execute(sql)
                except:
                    conn.rollback()
                    print(f'Error loading {script}')
                    traceback.print_exc()
                    return False
            cursor.execute('DELETE FROM schema;')
            cursor.execute('INSERT INTO schema (SELECT %s AS version);', (schema['version'],))

            version = schema['version']

    conn.commit()
    return version

def add_artist(conn, artist):
    artist_id = str(uuid.uuid4())

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO artist VALUES
        (%s, %s, NULL, NULL)''',
        (
            artist_id,
            artist['name']
        )
    )

    conn.commit()
    return artist_id

def add_album(conn, album):
    album_id = str(uuid.uuid4())

    songs = []
    for pos, song in enumerate(album['songs']):
        songs.append({
            'song_id': str(uuid.uuid4()),
            'position': pos,
            'grade': song
        })

    genres = [(album_id,album['genre'],True)]
    for genre in album.get('subgenres', []):
        genres.append((album_id, genre, False))

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO album VALUES
        (%s, %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s, NULL, NULL);''',
        (
            album_id,
            album['artist_id'],
            album['name'],
            album['format'],
            album.get('release_date'),
            album.get('first_listen'),
            album.get('rating'),
            album.get('pitchfork'),
            album.get('metacritic'),
            album.get('fantano')
        )
    )

    psycopg2.extras.execute_values(cursor, '''
        INSERT INTO genre VALUES %s;''',
        genres
    )
   
    psycopg2.extras.execute_values(cursor, '''
        INSERT INTO song VALUES %s;''',
        ((
            song['song_id'],
            album_id,
            None,
            None,
            song['position'],
            song['grade'],
            None
        ) for song in songs)
    )
    
    conn.commit()
    return album_id
