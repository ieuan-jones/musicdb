import functools
import json
import os
from flask import Blueprint, request, jsonify, abort

import musicdb.db as db
#from musicdb.model import load_json_album

bp = Blueprint('catalogue', __name__, url_prefix='/catalogue')

@bp.route('/initialise_db')
def initialise():
    conn = db.connect_db()
    schema_version = db.initialise_db(conn)
    db.close_db(conn)

    if schema_version:
        return {'schema': schema_version}
    else:
        abort(500)

@bp.route('/artist', methods=['POST'])
def add_artist():
    conn = db.connect_db()
    artist_id = db.add_artist(conn, request.get_json())
    db.close_db(conn)

    return {
        'artist_id': artist_id
    }

@bp.route('/album', methods=['POST'])
def add_album():
    conn = db.connect_db()
    album_id = db.add_album(conn, request.get_json())
    db.close_db(conn)

    return {
        'album_id': album_id
    }

@bp.route('/song', methods=['POST'])
def add_song():
    content = request.get_json()
    
    return jsonify(content)

@bp.route('/')
def index():
    return os.getcwd()
