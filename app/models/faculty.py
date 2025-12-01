from app import db
from datetime import datetime
import json


class Faculty(db.Model):
    """Faculty model with time preferences"""
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    department = db.Column(db.String(50), nullable=False, default='CSE')
    designation = db.Column(db.String(50), nullable=True)
    max_hours_per_day = db.Column(db.Integer, default=6)
    max_hours_per_week = db.Column(db.Integer, default=18)
    
    # Time preferences stored as JSON
    # Format: {"MON-1": "preferred", "MON-2": "unavailable", ...}
    preferred_slots = db.Column(db.Text, default='{}')
    unavailable_slots = db.Column(db.Text, default='{}')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course_mappings = db.relationship('FacultyCourse', backref='faculty', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_preferred_slots(self):
        """Get preferred slots as list"""
        try:
            return json.loads(self.preferred_slots) if self.preferred_slots else {}
        except:
            return {}
    
    def set_preferred_slots(self, slots_dict):
        """Set preferred slots from dictionary"""
        self.preferred_slots = json.dumps(slots_dict)
    
    def get_unavailable_slots(self):
        """Get unavailable slots as list"""
        try:
            return json.loads(self.unavailable_slots) if self.unavailable_slots else {}
        except:
            return {}
    
    def set_unavailable_slots(self, slots_dict):
        """Set unavailable slots from dictionary"""
        self.unavailable_slots = json.dumps(slots_dict)
    
    def is_slot_preferred(self, slot_id):
        """Check if a slot is preferred"""
        prefs = self.get_preferred_slots()
        return prefs.get(slot_id, False)
    
    def is_slot_unavailable(self, slot_id):
        """Check if a slot is unavailable"""
        unavail = self.get_unavailable_slots()
        return unavail.get(slot_id, False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'faculty_id': self.faculty_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'designation': self.designation,
            'max_hours_per_day': self.max_hours_per_day,
            'max_hours_per_week': self.max_hours_per_week,
            'preferred_slots': self.get_preferred_slots(),
            'unavailable_slots': self.get_unavailable_slots(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Faculty {self.faculty_id}: {self.name}>'
