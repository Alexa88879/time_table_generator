import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'timetable.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Export settings
    EXPORT_FOLDER = os.path.join(basedir, 'exports')
    
    # Algorithm settings
    GA_POPULATION_SIZE = 50
    GA_MAX_GENERATIONS = 500
    GA_CROSSOVER_RATE = 0.85
    GA_MUTATION_RATE = 0.15
    GA_ELITISM_COUNT = 5
    GA_TOURNAMENT_SIZE = 5
    GA_TIME_LIMIT_SECONDS = 60


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
