from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from app.routes.poll_routes import poll_bp
    from app.routes.vote_routes import vote_bp

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(poll_bp, url_prefix="/polls")
    app.register_blueprint(vote_bp, url_prefix="/vote")

    return app
