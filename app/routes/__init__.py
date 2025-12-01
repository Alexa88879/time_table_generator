"""Routes package - Blueprint exports"""
from app.routes.main import main_bp
from app.routes.faculty import faculty_bp
from app.routes.room import room_bp
from app.routes.section import section_bp
from app.routes.mapping import mapping_bp
from app.routes.upload import upload_bp
from app.routes.timetable import timetable_bp
from app.routes.export import export_bp

__all__ = [
    'main_bp',
    'faculty_bp',
    'room_bp',
    'section_bp',
    'mapping_bp',
    'upload_bp',
    'timetable_bp',
    'export_bp'
]
