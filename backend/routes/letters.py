from flask import Blueprint, request, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required
import datetime

letters_bp = Blueprint('letters', __name__)

LETTER_TEMPLATES = {
    'Leave letter': """
[Date]

Subject: [Subject]

Dear [Recipient],

I am writing to formally request a leave of absence for [Reason]. I am unable to attend [Context] on [Date]. 

Thank you for your understanding.

Sincerely,
[Name]
[Class/Department]
[Contact]
""",
    'Sick leave': """
[Date]

Subject: Sick Leave Application

Dear [Recipient],

Please excuse my absence from [Context] on [Date]. I was unwell and advised by my doctor to rest. I will ensure all pending work is completed promptly.

Sincerely,
[Name]
[Class/Department]
[Contact]
""",
    'Apology letter': """
[Date]

Subject: Apology for [Subject]

Dear [Recipient],

I am writing to sincerely apologize for [Reason]. It was unintentional, and I assure you it will not happen again. 

Thank you for your patience and understanding.

Sincerely,
[Name]
[Class/Department]
[Contact]
"""
}

def generate_letter(details):
    letter_type = details.get('type', 'Leave letter')
    template = LETTER_TEMPLATES.get(letter_type, LETTER_TEMPLATES['Leave letter'])
    
    # Replace placeholders
    today = datetime.date.today().strftime('%B %d, %Y')
    content = template.replace('[Date]', today)
    content = content.replace('[Subject]', details.get('subject', ''))
    content = content.replace('[Recipient]', details.get('recipient_name', 'Sir/Madam'))
    content = content.replace('[Reason]', details.get('reason', 'personal reasons'))
    content = content.replace('[Context]', details.get('college_company', 'class/office'))
    content = content.replace('[Name]', details.get('name', ''))
    content = content.replace('[Class/Department]', details.get('class_dept', ''))
    content = content.replace('[Contact]', f"{details.get('contact', '')} | {details.get('email', '')}")
    
    return content.strip()

@letters_bp.route('/generate', methods=['POST'])
@login_required
def generate_letter_api():
    """Generates formatted letters based on inputs."""
    data = request.get_json()
    
    generated_text = generate_letter(data)
    
    # Save to history & letters table
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1) # Fallback to user 1
        
        cur.execute(
            "INSERT INTO letters (user_id, recipient, subject, generated_text) VALUES (%s, %s, %s, %s) RETURNING id",
            (user_id, data.get('recipient_name', ''), data.get('subject', ''), generated_text)
        )
        
        cur.execute(
            "INSERT INTO history (user_id, type, content) VALUES (%s, %s, %s)",
            (user_id, 'letter', generated_text)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error saving letter history: {e}")
    finally:
        cur.close()
        conn.close()
        
    return jsonify({
        'generated_letter': generated_text
    }), 200
