from app import db
from datetime import datetime, time


class TimeSlot(db.Model):
    """Time slot model (40 hardcoded slots)"""
    __tablename__ = 'timeslots'
    
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.String(10), unique=True, nullable=False)  # e.g., MON-1
    day = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    day_index = db.Column(db.Integer, nullable=False)  # 0=Monday, 1=Tuesday, etc.
    period = db.Column(db.Integer, nullable=False)  # 1-8
    start_time = db.Column(db.String(10), nullable=False)  # e.g., 09:10
    end_time = db.Column(db.String(10), nullable=False)  # e.g., 10:00
    is_break = db.Column(db.Boolean, default=False)
    is_lunch = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='timeslot', lazy='dynamic')
    
    @property
    def display_time(self):
        return f"{self.start_time} - {self.end_time}"
    
    @property
    def display_name(self):
        return f"{self.day} P{self.period} ({self.display_time})"
    
    @property
    def is_morning(self):
        """Periods 1-4 are morning (before lunch)"""
        return self.period <= 4
    
    @property
    def is_afternoon(self):
        """Periods 5-8 are afternoon (after lunch)"""
        return self.period >= 5
    
    def can_be_lab_start(self):
        """Check if this slot can be the start of a 2-period lab"""
        # Labs can start at periods 1, 2, 3 (morning) or 5, 6, 7 (afternoon)
        # Cannot start at period 4 (would cross lunch)
        return self.period in [1, 2, 3, 5, 6, 7]
    
    def get_next_slot_id(self):
        """Get the next consecutive slot ID for lab scheduling"""
        if self.period < 8 and self.period != 4:  # Can't cross lunch
            return f"{self.day[:3].upper()}-{self.period + 1}"
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'slot_id': self.slot_id,
            'day': self.day,
            'day_index': self.day_index,
            'period': self.period,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'display_time': self.display_time,
            'display_name': self.display_name,
            'is_break': self.is_break,
            'is_lunch': self.is_lunch,
            'is_morning': self.is_morning,
            'is_afternoon': self.is_afternoon,
            'can_be_lab_start': self.can_be_lab_start()
        }
    
    def __repr__(self):
        return f'<TimeSlot {self.slot_id}: {self.display_name}>'
