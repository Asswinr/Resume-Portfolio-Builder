from flask import Blueprint, request, jsonify
from src.utils.ai_utils import generate_ai_content

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/generate-content', methods=['POST'])
def generate_content():
    """
    Endpoint to generate AI content based on a given prompt.
    Expects a JSON body with a 'prompt' field.
    """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']
    generated_text = generate_ai_content(prompt)

    if "Error" in generated_text: # Check for error messages returned by generate_ai_content
        return jsonify({"error": generated_text}), 500
    
    return jsonify({"generated_content": generated_text}), 200