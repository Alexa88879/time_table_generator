from app import db
from datetime import datetime


class Section(db.Model):
    """Section model for student groups"""
    __tablename__ = 'sections'
    
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CSE-3-A
    name = db.Column(db.String(10), nullable=False)  # A, B, C
    branch = db.Column(db.String(50), nullable=False, default='CSE')
    semester = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False, default=60)
    batch_year = db.Column(db.Integer, nullable=False)  # e.g., 2024
    academic_year = db.Column(db.String(10), nullable=False)  # e.g., 2024-25
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    batches = db.relationship('Batch', backref='section', lazy='dynamic', cascade='all, delete-orphan')
    faculty_mappings = db.relationship('FacultyCourse', backref='section', lazy='dynamic', cascade='all, delete-orphan')
    timetable_entries = db.relationship('Timetable', backref='section', lazy='dynamic')
    
    @property
    def display_name(self):
        return f"{self.branch} Sem-{self.semester} Sec-{self.name}"
    
    @property
    def batch_g1_strength(self):
        return self.strength // 2
    
    @property
    def batch_g2_strength(self):
        return self.strength - self.batch_g1_strength
    
    def get_batches(self):
        """Get G1 and G2 batches"""
        return self.batches.all()
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'name': self.name,
            'branch': self.branch,
            'semester': self.semester,
            'strength': self.strength,
            'batch_year': self.batch_year,
            'academic_year': self.academic_year,
            'is_active': self.is_active,
            'display_name': self.display_name,
            'batch_g1_strength': self.batch_g1_strength,
            'batch_g2_strength': self.batch_g2_strength
        }
    
    def __repr__(self):
        return f'<Section {self.section_id}>'


class Batch(db.Model):
    """Batch model for lab groups (G1, G2)"""
    __tablename__ = 'batches'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(30), unique=True, nullable=False)  # e.g., CSE-3-A-G1
    name = db.Column(db.String(5), nullable=False)  # G1, G2
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='batch', lazy='dynamic')
    
    @property
    def display_name(self):
        return f"{self.section.display_name} - {self.name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'name': self.name,
            'section_id': self.section_id,
            'strength': self.strength,
            'display_name': self.display_name
        }
    
    def __repr__(self):
        return f'<Batch {self.batch_id}>'
