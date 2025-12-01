from app import db
from datetime import datetime


class Course(db.Model):
    """Course model for storing curriculum data (80 hardcoded courses)"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(10), nullable=False)  # BS, ES, PC, HS, VA, OE, DE
    course_type = db.Column(db.String(10), nullable=False)  # T (Theory), P (Practical)
    lecture_hours = db.Column(db.Integer, default=0)  # L
    tutorial_hours = db.Column(db.Integer, default=0)  # T
    practical_hours = db.Column(db.Integer, default=0)  # P
    is_lab = db.Column(db.Boolean, default=False)
    is_elective = db.Column(db.Boolean, default=False)
    elective_group = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    faculty_mappings = db.relationship('FacultyCourse', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def total_hours_per_week(self):
        return self.lecture_hours + self.tutorial_hours + self.practical_hours
    
    @property
    def category_color(self):
        colors = {
            'BS': '#3b82f6',   # Blue - Basic Science
            'ES': '#10b981',   # Emerald - Engineering Science
            'PC': '#8b5cf6',   # Violet - Professional Core
            'HS': '#f59e0b',   # Amber - Humanities
            'VA': '#ec4899',   # Pink - Value Added
            'OE': '#06b6d4',   # Cyan - Open Elective
            'DE': '#f97316'    # Orange - Discipline Elective
        }
        return colors.get(self.category, '#6b7280')
    
    @property
    def category_name(self):
        names = {
            'BS': 'Basic Science',
            'ES': 'Engineering Science',
            'PC': 'Professional Core',
            'HS': 'Humanities & Social Science',
            'VA': 'Value Added',
            'OE': 'Open Elective',
            'DE': 'Departmental Elective'
        }
        return names.get(self.category, 'Other')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'semester': self.semester,
            'credits': self.credits,
            'category': self.category,
            'category_name': self.category_name,
            'category_color': self.category_color,
            'course_type': self.course_type,
            'lecture_hours': self.lecture_hours,
            'tutorial_hours': self.tutorial_hours,
            'practical_hours': self.practical_hours,
            'total_hours': self.total_hours_per_week,
            'is_lab': self.is_lab,
            'is_elective': self.is_elective,
            'elective_group': self.elective_group
        }
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'
