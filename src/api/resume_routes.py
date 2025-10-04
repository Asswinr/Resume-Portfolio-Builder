from flask import Blueprint, request, jsonify, send_file, current_app
from io import BytesIO
from weasyprint import HTML, CSS

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

@resume_bp.route('/generate-pdf', methods=['POST'])
def generate_resume_pdf():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Generate HTML content from the provided data
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume</title>
            <style>
                body {
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    font-size: 10pt;
                }
                .container {
                    width: 100%;
                    margin: auto;
                    padding: 20px;
                    box-sizing: border-box;
                }
                .header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .header h1 {
                    margin: 0;
                    color: #222;
                    font-size: 24pt;
                }
                .header p {
                    margin: 5px 0;
                    font-size: 12pt;
                }
                .section {
                    margin-bottom: 15px;
                }
                .section-title {
                    font-size: 14pt;
                    color: #555;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 5px;
                    margin-bottom: 10px;
                }
                .item-title {
                    font-weight: bold;
                    font-size: 11pt;
                }
                .item-details {
                    margin-left: 15px;
                    font-size: 10pt;
                }
                ul {
                    list-style-type: disc;
                    margin-left: 20px;
                    padding-left: 0;
                }
                ul li {
                    margin-bottom: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{data.get('personal_info', {}).get('name', '')}</h1>
                    <p>{data.get('personal_info', {}).get('role', '')}</p>
                    <p>{data.get('personal_info', {}).get('email', '')} | {data.get('personal_info', {}).get('phone', '')} | {data.get('personal_info', {}).get('linkedin', '')} | {data.get('personal_info', {}).get('github', '')}</p>
                </div>

                <div class="section">
                    <div class="section-title">Area of Expertise</div>
                    <ul>
                        {''.join([f'<li>{item}</li>' for item in data.get('area_of_expertise', [])])}
                    </ul>
                </div>
                <div class="section">
                    <div class="section-title">Key Achievements</div>
                    <ul>
                        {''.join([f'<li>{item}</li>' for item in data.get('key_achievements', [])])}
                    </ul>
                </div>
                <div class="section">
                    <div class="section-title">Experience</div>
                    {''.join([f'<div class="item-title">{exp.get('title', '')} at {exp.get('company', '')} ({exp.get('years', '')})</div><div class="item-details">{exp.get('description', '')}</div>' for exp in data.get('experience', [])])}
                </div>
                <div class="section">
                    <div class="section-title">Education</div>
                    {''.join([f'<div class="item-title">{edu.get('degree', '')} from {edu.get('university', '')} ({edu.get('years', '')})</div>' for edu in data.get('education', [])])}
                </div>
            </div>
        </body>
        </html>
        """

        pdf_buffer = BytesIO()

        HTML(string=html_content).write_pdf(pdf_buffer)

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