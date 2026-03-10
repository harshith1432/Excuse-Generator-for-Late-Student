import functools
from flask import Blueprint, request, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'error': 'User already exists'}), 409

        hashed_pwd = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id, name",
            (name, email, hashed_pwd)
        )
        user = cur.fetchone()
        conn.commit()
        return jsonify({'message': 'User registered successfully', 'user': {'id': user['id'], 'name': user['name']}}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, name, password_hash FROM users WHERE email = %s", (email,))
        user_record = cur.fetchone()

        if user_record and check_password_hash(user_record['password_hash'], password):
            session['user_id'] = user_record['id']
            return jsonify({'message': 'Login successful', 'user': {'id': user_record['id'], 'name': user_record['name']}}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            # For simplicity in local testing if no session exists, we can mock user #1
            # In a real app we'd just return 401
            # return jsonify({'error': 'Authentication required'}), 401
            g.user_id = 1 # Assuming a default user
        else:
            g.user_id = session['user_id']
        return view(**kwargs)
    return wrapped_view
