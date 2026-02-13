from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    # db-configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # routes
    from .routes import main
    app.register_blueprint(main)

    return app