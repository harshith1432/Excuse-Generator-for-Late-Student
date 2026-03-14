from flask import Blueprint, request, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required
import datetime

letters_bp = Blueprint('letters', __name__)

from flask import Blueprint, request, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required
from backend.ai_client import ai_client
import datetime

letters_bp = Blueprint('letters', __name__)

def generate_letter_ai(details):
    letter_type = details.get('type', 'Leave letter')
    subject = details.get('subject', 'General')
    reason = details.get('reason', '')
    recipient = details.get('recipient_name', 'Sir/Madam')
    context = details.get('college_company', 'class/college')
    user_name = details.get('name', 'Student')
    
    prompt = (
        "Write a professional formal letter/application based on these details:\n"
        f"- Recipient: {recipient}\n"
        f"- Subject: {subject}\n"
        f"- Reason/Context: {reason}\n"
        f"- Sender Name: {user_name}\n"
        f"- Sender Credentials: {context}\n"
        f"- Date: {datetime.date.today().strftime('%B %d, %Y')}\n\n"
        "The letter MUST follow this EXACT structure:\n"
        "1. FROM ADDRESS: Sender Name and Credentials at the top.\n"
        "2. DATE: Current date.\n"
        "3. TO ADDRESS: Recipient details.\n"
        "4. SUBJECT: Clear 'Subject:' line.\n"
        "5. SALUTATION: Professional greeting (e.g., Respected Sir/Madam or Dear [Name]).\n"
        "6. BODY: Well-structured paragraphs addressing the reason.\n"
        "7. CLOSING: Professional sign-off (e.g., Thanking you, Best regards) followed by Sender Name.\n\n"
        "Return ONLY the formatted letter content. Do not include any extra text."
    )

    content = ai_client.generate_text(prompt)
    return content.strip()

@letters_bp.route('/generate', methods=['POST'])
@login_required
def generate_letter_api():
    """Generates formatted letters using AI."""
    data = request.get_json()
    generated_text = generate_letter_ai(data)
    
    # Save to history & letters table
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1)
        cur.execute(
            "INSERT INTO letters (user_id, recipient, subject, generated_text) VALUES (%s, %s, %s, %s)",
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
        
    return jsonify({'generated_letter': generated_text}), 200

@letters_bp.route('/smart-reply', methods=['POST'])
@login_required
def smart_reply_api():
    """Generates a smart reply to a message using AI."""
    data = request.get_json()
    incoming_message = data.get('message', '')
    tone = data.get('tone', 'Professional')
    
    prompt = f"Generate an intelligent and {tone} reply to the following message:\n\"{incoming_message}\"\n"
    prompt += "The reply should be helpful, clear, and maintain the specified tone. Return ONLY the reply text."
    
    reply_text = ai_client.generate_text(prompt)
    
    # Save to history
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1)
        cur.execute(
            "INSERT INTO history (user_id, type, content) VALUES (%s, %s, %s)",
            (user_id, 'reply', reply_text)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        
    return jsonify({'reply': reply_text}), 200
