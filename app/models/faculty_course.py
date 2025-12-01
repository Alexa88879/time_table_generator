from app import db
from datetime import datetime


class FacultyCourse(db.Model):
    """Faculty-Course-Section mapping"""
    __tablename__ = 'faculty_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    session_type = db.Column(db.String(5), nullable=False)  # L (Lecture), T (Tutorial), P (Practical)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=True)
    academic_year = db.Column(db.String(10), nullable=False, default='2024-25')
    is_primary = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='faculty_course', lazy='dynamic')
    batch = db.relationship('Batch', backref='faculty_courses')
    
    __table_args__ = (
        db.UniqueConstraint('faculty_id', 'course_id', 'section_id', 'session_type', 'batch_id', 'academic_year',
                          name='uq_faculty_course_section_session'),
    )
    
    @property
    def session_type_name(self):
        names = {
            'L': 'Lecture',
            'T': 'Tutorial',
            'P': 'Practical'
        }
        return names.get(self.session_type, self.session_type)
    
    @property
    def hours_per_week(self):
        """Get required hours per week based on session type"""
        if self.session_type == 'L':
            return self.course.lecture_hours
        elif self.session_type == 'T':
            return self.course.tutorial_hours
        elif self.session_type == 'P':
            return self.course.practical_hours
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'faculty_id': self.faculty_id,
            'faculty_name': self.faculty.name if self.faculty else None,
            'course_id': self.course_id,
            'course_code': self.course.code if self.course else None,
            'course_name': self.course.name if self.course else None,
            'section_id': self.section_id,
            'section_name': self.section.display_name if self.section else None,
            'session_type': self.session_type,
            'session_type_name': self.session_type_name,
            'academic_year': self.academic_year,
            'is_primary': self.is_primary,
            'hours_per_week': self.hours_per_week
        }
    
    def __repr__(self):
        return f'<FacultyCourse {self.faculty.name if self.faculty else "?"} -> {self.course.code if self.course else "?"}>'
