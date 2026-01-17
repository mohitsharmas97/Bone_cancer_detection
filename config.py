import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ORIGINAL_FOLDER = os.path.join(UPLOAD_FOLDER, 'original')
    HEATMAP_FOLDER = os.path.join(UPLOAD_FOLDER, 'heatmaps')
    REPORTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'reports')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model configuration
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'best.pt')
    
    @staticmethod
    def init_app(app):
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.ORIGINAL_FOLDER, exist_ok=True)
        os.makedirs(Config.HEATMAP_FOLDER, exist_ok=True)
        os.makedirs(Config.REPORTS_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance'), exist_ok=True)
