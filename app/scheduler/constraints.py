"""Constraint Checker - Validates hard and soft constraints for timetable"""
from app.models import (
    Section, Course, Faculty, Room, FacultyCourse,
    Timetable, TimeSlot, Batch
)
from app import db
import json


class ConstraintChecker:
    """Checks all hard and soft constraints for a timetable"""
    
    def __init__(self, section_id):
        self.section_id = section_id
        self.section = Section.query.get(section_id)
        self.entries = Timetable.query.filter_by(section_id=section_id).all()
        # Load timeslots
        self.timeslots = TimeSlot.query.order_by(TimeSlot.day_index, TimeSlot.period).all()
        self.timeslot_ids = [t.id for t in self.timeslots]
        
    def check_all(self):
        """Check all constraints and return violations"""
        hard_violations = []
        soft_violations = []
        
        # Hard constraints
        hard_violations.extend(self.check_faculty_conflicts())
        hard_violations.extend(self.check_room_conflicts())
        hard_violations.extend(self.check_section_conflicts())
        hard_violations.extend(self.check_lab_consecutive())
        hard_violations.extend(self.check_faculty_availability())
        hard_violations.extend(self.check_room_capacity())
        
        # Soft constraints
        soft_violations.extend(self.check_faculty_preferences())
        soft_violations.extend(self.check_faculty_daily_load())
        soft_violations.extend(self.check_course_distribution())
        soft_violations.extend(self.check_lecture_gaps())
        
        # Calculate score (higher is better)
        score = 1000 - (len(hard_violations) * 100) - (len(soft_violations) * 10)
        
        return {
            'hard': hard_violations,
            'soft': soft_violations,
            'score': max(0, score)
        }
    
    def check_faculty_conflicts(self):
        """HC1: Faculty cannot teach two classes at the same time"""
        violations = []
        
        # Group entries by timeslot and faculty
        faculty_slots = {}
        for entry in self.entries:
            if not entry.faculty_course:
                continue
            key = (entry.faculty_course.faculty_id, entry.timeslot_id)
            if key not in faculty_slots:
                faculty_slots[key] = []
            faculty_slots[key].append(entry)
        
        # Check for same faculty at same time across all sections
        all_entries = Timetable.query.all()
        global_faculty_slots = {}
        for entry in all_entries:
            key = (entry.faculty_course.faculty_id, entry.timeslot_id)
            if key not in global_faculty_slots:
                global_faculty_slots[key] = []
            global_faculty_slots[key].append(entry)
        
        for (faculty_id, slot_id), entries in global_faculty_slots.items():
            if len(entries) > 1:
                faculty = Faculty.query.get(faculty_id)
                slot = TimeSlot.query.get(slot_id)
                violations.append({
                    'type': 'faculty_conflict',
                    'message': f"Faculty {faculty.name} has {len(entries)} classes at {slot.day} P{slot.period}",
                    'severity': 'hard'
                })
        
        return violations
    
    def check_room_conflicts(self):
        """HC2: Room cannot have two classes at the same time"""
        violations = []
        
        all_entries = Timetable.query.all()
        room_slots = {}
        for entry in all_entries:
            if entry.room_id:
                key = (entry.room_id, entry.timeslot_id)
                if key not in room_slots:
                    room_slots[key] = []
                room_slots[key].append(entry)
        
        for (room_id, slot_id), entries in room_slots.items():
            if len(entries) > 1:
                room = Room.query.get(room_id)
                slot = TimeSlot.query.get(slot_id)
                violations.append({
                    'type': 'room_conflict',
                    'message': f"Room {room.name} has {len(entries)} bookings at {slot.day} P{slot.period}",
                    'severity': 'hard'
                })
        
        return violations
    
    def check_section_conflicts(self):
        """HC3: Section cannot have two theory classes at the same time"""
        violations = []
        
        # For theory classes (no batch), section can only have one class per slot
        section_slots = {}
        for entry in self.entries:
            if not entry.batch_id:  # Theory class
                if entry.timeslot_id not in section_slots:
                    section_slots[entry.timeslot_id] = []
                section_slots[entry.timeslot_id].append(entry)
        
        for slot_id, entries in section_slots.items():
            if len(entries) > 1:
                slot = TimeSlot.query.get(slot_id)
                violations.append({
                    'type': 'section_conflict',
                    'message': f"Section has {len(entries)} theory classes at {slot.day} P{slot.period}",
                    'severity': 'hard'
                })
        
        return violations
    
    def check_lab_consecutive(self):
        """HC4: Lab sessions must be in consecutive periods"""
        violations = []
        
        # Group lab entries by course and batch
        lab_entries = [e for e in self.entries if e.faculty_course.course.is_lab]
        lab_groups = {}
        
        for entry in lab_entries:
            key = (entry.faculty_course.course_id, entry.batch_id, entry.timeslot.day)
            if key not in lab_groups:
                lab_groups[key] = []
            lab_groups[key].append(entry)
        
        for (course_id, batch_id, day), entries in lab_groups.items():
            if len(entries) >= 2:
                periods = sorted([e.timeslot.period for e in entries])
                # Check if periods are consecutive
                for i in range(len(periods) - 1):
                    if periods[i+1] - periods[i] != 1:
                        course = Course.query.get(course_id)
                        violations.append({
                            'type': 'lab_not_consecutive',
                            'message': f"Lab {course.code} periods not consecutive on {day}: {periods}",
                            'severity': 'hard'
                        })
                        break
        
        return violations
    
    def check_faculty_availability(self):
        """HC5: Faculty cannot be scheduled during unavailable slots"""
        violations = []
        
        for entry in self.entries:
            if entry.faculty_course.faculty.unavailable_slots:
                unavailable = json.loads(entry.faculty_course.faculty.unavailable_slots)
                slot_key = f"{entry.timeslot.day}_{entry.timeslot.period}"
                if slot_key in unavailable:
                    violations.append({
                        'type': 'faculty_unavailable',
                        'message': f"Faculty {entry.faculty_course.faculty.name} is unavailable at {entry.timeslot.day} P{entry.timeslot.period}",
                        'severity': 'hard'
                    })
        
        return violations
    
    def check_room_capacity(self):
        """HC6: Room capacity must accommodate students"""
        violations = []
        
        for entry in self.entries:
            if entry.room:
                if entry.batch:
                    strength = entry.batch.strength
                else:
                    strength = self.section.strength
                
                if entry.room.capacity < strength:
                    violations.append({
                        'type': 'room_capacity',
                        'message': f"Room {entry.room.name} (cap: {entry.room.capacity}) too small for {strength} students",
                        'severity': 'hard'
                    })
        
        return violations
    
    def check_faculty_preferences(self):
        """SC1: Prefer faculty's preferred time slots"""
        violations = []
        
        for entry in self.entries:
            if entry.faculty_course.faculty.preferred_slots:
                preferred = json.loads(entry.faculty_course.faculty.preferred_slots)
                slot_key = f"{entry.timeslot.day}_{entry.timeslot.period}"
                if preferred and slot_key not in preferred:
                    violations.append({
                        'type': 'not_preferred_slot',
                        'message': f"Faculty {entry.faculty_course.faculty.name} not in preferred slot at {entry.timeslot.day} P{entry.timeslot.period}",
                        'severity': 'soft'
                    })
        
        return violations
    
    def check_faculty_daily_load(self):
        """SC2: Limit faculty's daily teaching hours"""
        violations = []
        
        # Count hours per faculty per day
        faculty_daily = {}
        all_entries = Timetable.query.all()
        
        for entry in all_entries:
            key = (entry.faculty_course.faculty_id, entry.timeslot.day)
            if key not in faculty_daily:
                faculty_daily[key] = 0
            faculty_daily[key] += 1
        
        for (faculty_id, day), count in faculty_daily.items():
            faculty = Faculty.query.get(faculty_id)
            if count > faculty.max_hours_per_day:
                violations.append({
                    'type': 'faculty_overload_daily',
                    'message': f"Faculty {faculty.name} has {count} hours on {day} (max: {faculty.max_hours_per_day})",
                    'severity': 'soft'
                })
        
        return violations
    
    def check_course_distribution(self):
        """SC3: Distribute course lectures across the week"""
        violations = []
        
        # Group non-lab courses by course_id
        theory_courses = {}
        for entry in self.entries:
            if not entry.faculty_course.course.is_lab:
                if entry.faculty_course.course_id not in theory_courses:
                    theory_courses[entry.faculty_course.course_id] = []
                theory_courses[entry.faculty_course.course_id].append(entry.timeslot.day)
        
        for course_id, days in theory_courses.items():
            # Check for consecutive days with same course
            day_order = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
            day_indices = sorted([day_order[d] for d in days])
            
            for i in range(len(day_indices) - 1):
                if day_indices[i+1] - day_indices[i] == 1:
                    course = Course.query.get(course_id)
                    violations.append({
                        'type': 'consecutive_days',
                        'message': f"Course {course.code} on consecutive days",
                        'severity': 'soft'
                    })
                    break
        
        return violations
    
    def check_lecture_gaps(self):
        """SC4: Minimize gaps in student's daily schedule"""
        violations = []
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for day in days:
            # Get all periods with classes for this section on this day
            day_entries = [e for e in self.entries if e.timeslot.day == day]
            if len(day_entries) < 2:
                continue
            
            # Get all periods (considering batches)
            all_periods = set()
            for entry in day_entries:
                if not entry.batch_id:  # Theory affects whole section
                    all_periods.add(entry.timeslot.period)
            
            if not all_periods:
                continue
            
            periods = sorted(all_periods)
            
            # Check for gaps (excluding lunch break after P4)
            for i in range(len(periods) - 1):
                gap = periods[i+1] - periods[i]
                # Gap > 1 and not crossing lunch
                if gap > 1 and not (periods[i] <= 4 < periods[i+1]):
                    violations.append({
                        'type': 'schedule_gap',
                        'message': f"Gap of {gap-1} periods on {day} between P{periods[i]} and P{periods[i+1]}",
                        'severity': 'soft'
                    })
        
        return violations


def calculate_fitness(section_id):
    """Calculate fitness score for a timetable"""
    checker = ConstraintChecker(section_id)
    result = checker.check_all()
    return result['score'], result['hard'], result['soft']
