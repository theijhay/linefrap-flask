import os
from flask import Flask

def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    
    # Load config
    if config_class:
        app.config.from_object(config_class)
    else:
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            from config import ProductionConfig as cfg
        else:
            from config import DevelopmentConfig as cfg
        app.config.from_object(cfg)

    # Ensure upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
