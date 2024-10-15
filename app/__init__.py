from flask import Flask
from app.database import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_db(app)

    from app.routes import bp
    app.register_blueprint(bp)

    return app