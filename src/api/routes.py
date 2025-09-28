# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "Invalid JSON payload"}), 400
    db: Session = SessionLocal()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')    
    if not username or not email or not password:
        db.close()
        return jsonify({"message": "Missing username, email, or password"}), 400

    if db.query(User).filter_by(username=username).first():
        db.close()
        return jsonify({"message": "Username already registered"}), 400

    if db.query(User).filter_by(email=email).first():
        db.close()
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "Invalid JSON payload"}), 400
    db: Session = SessionLocal()
    username = data.get('username')
    password = data.get('password')   
    if not username or not password:
        db.close()
        return jsonify({"message": "Missing username or password"}), 400

    user = db.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.hashed_password, password):
        db.close()
        return jsonify({"message": "Invalid credentials"}), 401

    db.close()
    return jsonify({"message": "Login successful", "user_id": user.id}), 200