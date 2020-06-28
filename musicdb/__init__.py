import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import catalogue 
    app.register_blueprint(catalogue.bp)

    return app
