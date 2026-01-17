from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db
import os


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize app directories
    Config.init_app(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.predict import predict_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(predict_bp, url_prefix='/predict')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    # Root route
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
