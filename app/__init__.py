from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Ensure upload and export directories exist
    import os
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(app.config.get('EXPORT_FOLDER', 'exports'), exist_ok=True)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.faculty import faculty_bp
    from app.routes.room import room_bp
    from app.routes.section import section_bp
    from app.routes.mapping import mapping_bp
    from app.routes.timetable import timetable_bp
    from app.routes.upload import upload_bp
    from app.routes.export import export_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(room_bp, url_prefix='/rooms')
    app.register_blueprint(section_bp, url_prefix='/sections')
    app.register_blueprint(mapping_bp, url_prefix='/mappings')
    app.register_blueprint(timetable_bp, url_prefix='/timetable')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(export_bp, url_prefix='/export')
    
    # Register API routes
    register_api_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_api_routes(app):
    """Register additional API routes"""
    from app.models import Course, Batch
    
    @app.route('/api/courses/<int:semester>')
    def get_courses_by_semester(semester):
        """Get courses for a specific semester"""
        courses = Course.query.filter_by(semester=semester).all()
        return jsonify([{
            'id': c.id,
            'code': c.code,
            'name': c.name,
            'credits': c.credits,
            'is_lab': c.is_lab,
            'is_elective': c.is_elective,
            'lecture_hours': c.lecture_hours,
            'tutorial_hours': c.tutorial_hours,
            'practical_hours': c.practical_hours
        } for c in courses])
    
    @app.route('/api/batches/<int:section_id>')
    def get_batches_by_section(section_id):
        """Get batches for a specific section"""
        batches = Batch.query.filter_by(section_id=section_id).all()
        return jsonify([{
            'id': b.id,
            'name': b.name,
            'strength': b.strength
        } for b in batches])
    
    # Exempt API routes from CSRF
    csrf.exempt(get_courses_by_semester)
    csrf.exempt(get_batches_by_section)
