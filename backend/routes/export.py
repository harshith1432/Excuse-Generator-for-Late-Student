import os
import tempfile
from fpdf import FPDF
from docx import Document
from flask import Blueprint, request, send_file, jsonify

export_bp = Blueprint('export', __name__)

@export_bp.route('/pdf', methods=['POST'])
def export_pdf():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400

    try:
        # Create PDF using fpdf2
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Use a standard font. Note: fpdf2 handles UTF-8 better but we use a core font for simplicity 
        # unless custom fonts are required. Latin-1 is default for core fonts.
        pdf.set_font("Arial", size=12)
        
        # Split content by lines and write
        # We replace some common non-latin1 chars if any appear from AI
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 10, txt=safe_content)
        
        fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        pdf.output(temp_path)
        
        return send_file(temp_path, as_attachment=True, download_name='letter.pdf', mimetype='application/pdf')
    except Exception as e:
        print(f"PDF Export Error: {e}")
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
