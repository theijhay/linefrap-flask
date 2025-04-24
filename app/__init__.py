import os
from flask import Flask

""" The function to create the Flask application instance"""
def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    
    """Load configuration from the config class or default to development"""
    if config_class:
        app.config.from_object(config_class)
    else:
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            from config import ProductionConfig as cfg
        else:
            from config import DevelopmentConfig as cfg
        app.config.from_object(cfg)

    """Set up the upload folder"""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    """Register the main blueprint"""
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
