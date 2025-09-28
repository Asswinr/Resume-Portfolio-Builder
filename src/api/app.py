# -*- coding: utf-8 -*-
from flask import Flask
from src.models.database import Base, engine
from src.models import user
from src.api.routes import auth_bp # Import the authentication blueprint

def create_app():
    app = Flask(__name__)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth') # Register the auth blueprint

    @app.route('/')
    def hello_world():
        return 'Hello, Flask API!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)