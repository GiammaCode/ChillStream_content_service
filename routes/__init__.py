from flask import Blueprint
from .films import films_bp
from .actors import actors_bp

def init_routes(app):
    app.register_blueprint(films_bp, url_prefix="/films")
    app.register_blueprint(actors_bp, url_prefix="/actors")

