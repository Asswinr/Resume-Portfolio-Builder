# -*- coding: utf-8 -*-
from flask import Flask
from src.models.database import Base, engine
from src.api.resume_routes import resume_bp # Import the new resume blueprint
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    app.register_blueprint(resume_bp) # Register the new resume blueprint

    @app.route('/')
    def hello_flask():
        return "Hello, Flask API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)