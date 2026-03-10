from flask import Blueprint, jsonify, g
from backend.database.db import get_db_connection
from backend.routes.auth import login_required

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
@login_required
def get_history():
    """Retrieves user history for excuses and letters."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        user_id = getattr(g, 'user_id', 1)
        cur.execute(
            "SELECT id, type, content, created_at FROM history WHERE user_id = %s ORDER BY created_at DESC LIMIT 50",
            (user_id,)
        )
        records = cur.fetchall()
        
        # Convert datetime to string for JSON serialization
        results = []
        for r in records:
            r_dict = dict(r)
            r_dict['created_at'] = r_dict['created_at'].isoformat()
            results.append(r_dict)
            
        return jsonify({'history': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
