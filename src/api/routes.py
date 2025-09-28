# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.user import User
from xhtml2pdf import pisa             # Import pisa for PDF conversion
from flask import request, send_file, current_app    # Import request, send_file, and current_app
from io import BytesIO                 # Import BytesIO

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON payload"}), 400
    db: Session = SessionLocal()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')    
    if not username or not email or not password:
        # …        db.close()
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
    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON payload"}), 400
    db: Session = SessionLocal()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:        db.close()
    return jsonify({"message": "Missing username or password"}), 400

    user = db.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.hashed_password, password):
        db.close()
        return jsonify({"message": "Invalid credentials"}), 401

    db.close()
    return jsonify({"message": "Login successful", "user_id": user.id}), 200

@app.route('/ai/generate-content', methods=['POST'])
def generate_content():
    data = request.get_json()
    html_content = data.get('html_content')

    if not html_content:
        return jsonify({"error": "No HTML content provided"}), 400

    # Create a BytesIO object to store the PDF
    pdf_buffer = BytesIO()

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html_content,                # the HTML to convert
        dest=pdf_buffer)             # file handle to receive result

    if pisa_status.err:
        return jsonify({"error": "Could not generate PDF", "details": pisa_status.err}), 500

    pdf_buffer.seek(0) # Rewind the buffer to the beginning

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume.pdf'
    )

        current_app.logger.error(f"Error generating resume PDF: {e}")  # Use current_app.logger


        return jsonify({"error": "An unexpected error occurred during PDF generation"}), 500

@app.route('/resume/generate-pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        data = request.get_json()
        html_content = data.get('html_content')

        if not html_content:
            return jsonify({"error": "No HTML content provided"}), 400

        # Create a BytesIO object to store the PDF
        pdf_buffer = BytesIO()

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            html_content,                # the HTML to convert
            dest=pdf_buffer)             # file handle to receive result

        if pisa_status.err:
            return jsonify({"error": "Could not generate PDF", "details": pisa_status.err}), 500

        pdf_buffer.seek(0) # Rewind the buffer to the beginning

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='resume.pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generating resume PDF: {e}") # Use current_app.logger
        return jsonify({"error": "An unexpected error occurred during PDF generation"}), 500