from app import db
from datetime import datetime
import uuid


class Timetable(db.Model):
    """Generated timetable entries"""
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    generation_id = db.Column(db.String(50), nullable=False)  # Batch generation identifier
    faculty_course_id = db.Column(db.Integer, db.ForeignKey('faculty_courses.id'), nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=True)  # For labs only
    is_lab_slot = db.Column(db.Boolean, default=False)
    is_second_slot = db.Column(db.Boolean, default=False)  # Second period of a 2-period lab
    linked_slot_id = db.Column(db.Integer, nullable=True)  # ID of first/second slot for labs
    is_locked = db.Column(db.Boolean, default=False)  # Manually locked slots
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'generation_id': self.generation_id,
            'faculty_course_id': self.faculty_course_id,
            'faculty_name': self.faculty_course.faculty.name if self.faculty_course else None,
            'course_code': self.faculty_course.course.code if self.faculty_course else None,
            'course_name': self.faculty_course.course.name if self.faculty_course else None,
            'course_category': self.faculty_course.course.category if self.faculty_course else None,
            'course_color': self.faculty_course.course.category_color if self.faculty_course else None,
            'session_type': self.faculty_course.session_type if self.faculty_course else None,
            'timeslot_id': self.timeslot_id,
            'day': self.timeslot.day if self.timeslot else None,
            'period': self.timeslot.period if self.timeslot else None,
            'start_time': self.timeslot.start_time if self.timeslot else None,
            'end_time': self.timeslot.end_time if self.timeslot else None,
            'room_id': self.room_id,
            'room_name': self.room.room_id if self.room else None,
            'section_id': self.section_id,
            'section_name': self.section.display_name if self.section else None,
            'batch_id': self.batch_id,
            'batch_name': self.batch.name if self.batch else None,
            'is_lab_slot': self.is_lab_slot,
            'is_second_slot': self.is_second_slot,
            'is_locked': self.is_locked
        }
    
    def __repr__(self):
        return f'<Timetable {self.id}: {self.faculty_course.course.code if self.faculty_course else "?"}>'


class GenerationLog(db.Model):
    """Log of timetable generations"""
    __tablename__ = 'generation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    generation_id = db.Column(db.String(50), unique=True, nullable=False)
    semester = db.Column(db.Integer, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=True)
    algorithm_used = db.Column(db.String(50), default='Hybrid GA+CSP')
    population_size = db.Column(db.Integer, nullable=True)
    generations_run = db.Column(db.Integer, nullable=True)
    fitness_score = db.Column(db.Float, nullable=True)
    hard_violations = db.Column(db.Integer, default=0)
    soft_violations = db.Column(db.Integer, default=0)
    time_taken_seconds = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, running, success, failed
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    @staticmethod
    def generate_id():
        return f"GEN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'generation_id': self.generation_id,
            'semester': self.semester,
            'section_id': self.section_id,
            'section_name': self.section.display_name if self.section else None,
            'algorithm_used': self.algorithm_used,
            'population_size': self.population_size,
            'generations_run': self.generations_run,
            'fitness_score': self.fitness_score,
            'hard_violations': self.hard_violations,
            'soft_violations': self.soft_violations,
            'time_taken_seconds': self.time_taken_seconds,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<GenerationLog {self.generation_id}: {self.status}>'
