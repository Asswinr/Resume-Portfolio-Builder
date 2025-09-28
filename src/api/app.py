# -*- coding: utf-8 -*-
from flask import Flask
from src.models.database import Base, engine # Import Base and engine
from src.models import user # Import the user model (this will ensure Base knows about User)

def create_app():
    app = Flask(__name__)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    @app.route('/')
    def hello_world():
        return 'Hello, Flask API!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)