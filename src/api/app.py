# -*- coding: utf-8 -*-
from flask import Flask
from src.models.database import Base, engine # Removed 'db' from import
from src.api.routes import auth_bp
from src.api.ai_routes import ai_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Removed: db.init_app(app)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ai_bp)

    @app.route('/')
    def hello_flask():
        return "Hello, Flask API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)