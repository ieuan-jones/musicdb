import functools
import json
import os
from flask import Blueprint

from musicdb.db import connect_db, initialise_db, close_db

bp = Blueprint('album', __name__, url_prefix='/album')

@bp.route('/initialise_db')
def initialise():
    conn = connect_db()
    success = initialise_db(conn)
    close_db(conn)

    return str(success)

@bp.route('/')
def index():
    return os.getcwd()
