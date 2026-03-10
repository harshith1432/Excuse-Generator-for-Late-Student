from flask import Blueprint, request, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required
import random

excuses_bp = Blueprint('excuses', __name__)

EXCUSE_TEMPLATES = {
    'Late to class': [
        "I sincerely apologize for my tardiness. My alarm didn't go off due to a sudden power outage overnight.",
        "Please excuse me for being late. There was an unexpected major traffic accident that blocked my usual route.",
        "I'm sorry I'm late. I had a sudden family emergency that I needed to attend to before coming to class."
    ],
    'Missed assignment': [
        "I deeply regret not submitting the assignment on time. My laptop crashed and I lost my recent progress. I am working to recover it.",
        "Unfortunately, I had a severe migraine yesterday that prevented me from looking at any screens. I will submit the assignment by tomorrow.",
        "Please accept my apologies for the delay. There was a misunderstanding regarding the submission deadline on my part."
    ],
    'Skipped meeting': [
        "I apologize for missing the meeting. Another urgent priority suddenly required my immediate attention.",
        "I meant to attend, but my internet connection went down completely shortly before the meeting started.",
        "I'm sorry I couldn't make it. I was feeling quite unwell and had to visit the doctor."
    ],
    'General': [
        "I apologize for the delay. An unexpected personal matter arose that I had to resolve immediately.",
        "Please excuse my absence/delay. I encountered unforeseen transportation issues.",
        "I sincerely apologize. I was dealing with a sudden family situation."
    ]
}

def generate_excuse(situation, delay_time=None, reason_category=None):
    # Simple logic-based generator
    templates = EXCUSE_TEMPLATES.get(situation, EXCUSE_TEMPLATES['General'])
    base_excuse = random.choice(templates)
    
    # Simple variation mapping
    variations = [
        base_excuse,
        f"I am writing to apologize. {base_excuse}",
        f"I deeply apologize. Although I tried my best, {base_excuse.lower()}"
    ]
    
    if delay_time:
        variations[0] += f" This caused a delay of {delay_time}."
        
    believability_score = random.randint(6, 9)
    return variations, believability_score

@excuses_bp.route('/generate', methods=['POST'])
@login_required
def generate_excuse_api():
    """Generates excuses based on inputs."""
    data = request.get_json()
    situation = data.get('situation', 'General')
    delay_time = data.get('delay_time', '')
    reason_category = data.get('reason_category', '')

    variations, score = generate_excuse(situation, delay_time, reason_category)
    
    # Save the selected/first excuse to history
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1) # Fallback to user 1
        generated_text = variations[0]
        
        cur.execute(
            "INSERT INTO excuses (user_id, situation, generated_text, believability_score) VALUES (%s, %s, %s, %s) RETURNING id",
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
