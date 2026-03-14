from flask import Blueprint, request, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required
from backend.ai_client import ai_client
import random

excuses_bp = Blueprint('excuses', __name__)

def generate_excuse_ai(situation, delay_time=None, reason_category=None):
    prompt = f"Generate a highly believable and professional excuse for the following situation: '{situation}'."
    if delay_time:
        prompt += f" The delay involved is {delay_time}."
    if reason_category and reason_category != 'General':
        prompt += f" The reason category is {reason_category}."
    
    prompt += " Provide 3 different variations: one formal, one casual, and one concise. Return ONLY the variations separated by '---'."

    ai_response = ai_client.generate_text(prompt)
    
    if "Error" in ai_response:
        # Fallback to simple variations if AI fails
        variations = [
            f"I apologize for the {situation}. It was due to unforeseen circumstances.",
            f"Sorry about the {situation}. I'll make sure it doesn't happen again.",
            f"Please excuse me for the {situation}."
        ]
        score = 5
    else:
        variations = [v.strip() for v in ai_response.split('---') if v.strip()]
        if not variations:
            variations = [ai_response]
        score = random.randint(7, 10)
        
    return variations, score

@excuses_bp.route('/generate', methods=['POST'])
@login_required
def generate_excuse_api():
    """Generates excuses using AI."""
    data = request.get_json()
    situation = data.get('situation', 'General')
    delay_time = data.get('delay_time', '')
    reason_category = data.get('reason_category', '')

    variations, score = generate_excuse_ai(situation, delay_time, reason_category)
    
    # Save the first excuse to history
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1)
        generated_text = variations[0]
        
        cur.execute(
            "INSERT INTO excuses (user_id, situation, generated_text, believability_score) VALUES (%s, %s, %s, %s)",
            (user_id, situation, generated_text, score)
        )
        
        cur.execute(
            "INSERT INTO history (user_id, type, content) VALUES (%s, %s, %s)",
            (user_id, 'excuse', generated_text)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error saving history: {e}")
    finally:
        cur.close()
        conn.close()
        
    return jsonify({
        'variations': variations,
        'believability_score': score
    }), 200
