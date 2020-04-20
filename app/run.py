import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    from app.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from database.models import db, flask_bcrypt
    db.init_app(app)

    flask_bcrypt.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)