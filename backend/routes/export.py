import os
import tempfile
import pdfkit
from docx import Document
from flask import Blueprint, request, send_file, jsonify

export_bp = Blueprint('export', __name__)

@export_bp.route('/pdf', methods=['POST'])
def export_pdf():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400

    html_content = f"<html><body><pre style='font-family: Arial, sans-serif; white-space: pre-wrap;'>{content}</pre></body></html>"
    
    try:
        # Create a temporary file to save the PDF
        fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        # wkhtmltopdf might require path configuration on Windows. Assuming it is in PATH
        # if pdfkit fails due to missing executable, the user will need to install wkhtmltopdf and add to PATH.
        pdfkit.from_string(html_content, temp_path)
        
        return send_file(temp_path, as_attachment=True, download_name='document.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@export_bp.route('/docx', methods=['POST'])
def export_docx():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400

    try:
        doc = Document()
        doc.add_paragraph(content)
        
        fd, temp_path = tempfile.mkstemp(suffix='.docx')
        os.close(fd)
        
        doc.save(temp_path)
        return send_file(temp_path, as_attachment=True, download_name='document.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
