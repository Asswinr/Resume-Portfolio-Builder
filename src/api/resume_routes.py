from flask import Blueprint, request, jsonify, send_file, current_app
from io import BytesIO
from xhtml2pdf import pisa

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

@resume_bp.route('/generate-pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        data = request.get_json()
        html_content = data.get('html_content')

        if not html_content:
            return jsonify({"error": "No HTML content provided"}), 400

        pdf_buffer = BytesIO()

        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_buffer
        )

        if pisa_status.err:
            current_app.logger.error(f"Error during PDF generation: {pisa_status.err}")
            return jsonify({"error": "Could not generate PDF", "details": pisa_status.err}), 500

        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='resume.pdf'
        )

    except Exception as e:
        current_app.logger.error(f"An unexpected error occurred during PDF generation: {e}")
        return jsonify({"error": "An unexpected error occurred during PDF generation"}), 500