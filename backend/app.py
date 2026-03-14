import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_fallback')

    # Import Blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.excuses import excuses_bp
    from backend.routes.letters import letters_bp
    from backend.routes.history import history_bp
    from backend.routes.export import export_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(excuses_bp, url_prefix='/api/excuses')
    app.register_blueprint(letters_bp, url_prefix='/api/letters')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    # Basic Pages
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/excuse-generator')
    def excuse_generator():
        return render_template('excuse_generator.html')

    @app.route('/letter-generator')
    def letter_generator():
        return render_template('letter_generator.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
        
    @app.route('/history')
    def history_page():
        return render_template('history.html')
        
    @app.route('/smart-reply')
    def smart_reply_page():
        return render_template('smart_reply.html')

    @app.route('/templates')
    def templates_page():
        return render_template('browse_templates.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
