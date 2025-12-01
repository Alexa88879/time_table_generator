from app import db
from datetime import datetime


class Room(db.Model):
    """Room/Lab model"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(50), nullable=True)
    floor = db.Column(db.Integer, nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=60)
    room_type = db.Column(db.String(20), nullable=False, default='Classroom')  # Classroom, Lab
    lab_type = db.Column(db.String(50), nullable=True)  # Computer, Physics, Chemistry, etc.
    has_projector = db.Column(db.Boolean, default=True)
    has_ac = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='room', lazy='dynamic')
    
    @property
    def is_lab(self):
        return self.room_type == 'Lab'
    
    @property
    def display_name(self):
        if self.name:
            return f"{self.room_id} - {self.name}"
        return self.room_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'name': self.name,
            'building': self.building,
            'floor': self.floor,
            'capacity': self.capacity,
            'room_type': self.room_type,
            'lab_type': self.lab_type,
            'is_lab': self.is_lab,
            'has_projector': self.has_projector,
            'has_ac': self.has_ac,
            'is_available': self.is_available,
            'display_name': self.display_name
        }
    
    def __repr__(self):
        return f'<Room {self.room_id}: {self.name}>'
