"""CSP Solver - Constraint Satisfaction Problem solver for initial timetable generation"""
from app.models import (
    Section, Course, Faculty, Room, FacultyCourse,
    Timetable, TimeSlot, Batch
)
from app import db
import json
import random
from collections import defaultdict


class CSPSolver:
    """
    Constraint Satisfaction Problem solver for timetable generation.
    Uses backtracking with forward checking and MRV heuristic.
    """
    
    def __init__(self, section_id):
        self.section_id = section_id
        self.section = Section.query.get(section_id)
        self.mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
        # Load timeslots
        self.timeslots = TimeSlot.query.order_by(TimeSlot.day_index, TimeSlot.period).all()
        self.timeslot_ids = [t.id for t in self.timeslots]
        self.rooms = Room.query.filter_by(is_available=True).all()
        self.classrooms = [r for r in self.rooms if not r.is_lab]
        self.labs = [r for r in self.rooms if r.is_lab]
        
        # Domain: possible (timeslot, room) assignments for each mapping
        self.domains = {}
        self.assignment = {}
        
        # Track used resources
        self.faculty_schedule = defaultdict(set)  # faculty_id -> set of timeslot_ids
        self.room_schedule = defaultdict(set)     # room_id -> set of timeslot_ids
        self.section_schedule = defaultdict(set)  # batch_id/None -> set of timeslot_ids
        
        self._initialize_domains()
    
    def _initialize_domains(self):
        """Initialize domains for each mapping"""
        for mapping in self.mappings:
            self.domains[mapping.id] = self._get_valid_slots(mapping)
    
    def _get_valid_slots(self, mapping):
        """Get valid (timeslot_id, room_id) pairs for a mapping"""
        valid = []
        
        is_lab = mapping.course.is_lab
        rooms = self.labs if is_lab else self.classrooms
        
        if not rooms:
            return valid
        
        # Get faculty unavailable slots
        unavailable = []
        if mapping.faculty.unavailable_slots:
            unavailable = json.loads(mapping.faculty.unavailable_slots)
        
        for slot in self.timeslots:
            # Skip if faculty unavailable
            slot_key = f"{slot.day}_{slot.period}"
            if slot_key in unavailable:
                continue
            
            # For labs, must start at periods 1, 3, 5, 7
            if is_lab and slot.period not in [1, 3, 5, 7]:
                continue
            
            for room in rooms:
                # Check capacity
                if mapping.batch:
                    needed_capacity = mapping.batch.strength
                if not mapping.batch_id:
                    needed_capacity = self.section.strength
                
                if room.capacity >= needed_capacity:
                    valid.append((slot.id, room.id))
        
        return valid
    
    def _get_required_hours(self, mapping):
        """Get number of periods needed for a mapping"""
        course = mapping.course
        if course.is_lab:
            return course.practical_hours  # Usually 2 for labs
        else:
            return course.lecture_hours + course.tutorial_hours
    
    def _is_consistent(self, mapping_id, slot_id, room_id):
        """Check if assignment is consistent with constraints"""
        mapping = FacultyCourse.query.get(mapping_id)
        slot = TimeSlot.query.get(slot_id)
        
        # Check faculty conflict
        if slot_id in self.faculty_schedule[mapping.faculty_id]:
            return False
        
        # Check room conflict
        if slot_id in self.room_schedule[room_id]:
            return False
        
        # Check section/batch conflict
        batch_key = mapping.batch_id if mapping.batch_id else 'section'
        if batch_key != 'section' and slot_id in self.section_schedule['section']:
            # Batch cannot have class when whole section has theory
            return False
        if batch_key == 'section' and any(slot_id in self.section_schedule[b.id] for b in self.section.batches):
            # Theory cannot overlap with any batch lab
            return False
        if slot_id in self.section_schedule[batch_key]:
            return False
        
        # For labs, check consecutive slot availability
        if mapping.course.is_lab:
            next_slot = TimeSlot.query.filter_by(
                day=slot.day, 
                period=slot.period + 1
            ).first()
            
            if not next_slot:
                return False
            
            # Check next slot is also free
            if next_slot.id in self.faculty_schedule[mapping.faculty_id]:
                return False
            if next_slot.id in self.room_schedule[room_id]:
                return False
            if next_slot.id in self.section_schedule[batch_key]:
                return False
        
        return True
    
    def _assign(self, mapping_id, slot_id, room_id):
        """Make an assignment"""
        mapping = FacultyCourse.query.get(mapping_id)
        batch_key = mapping.batch_id if mapping.batch_id else 'section'
        
        self.assignment[mapping_id] = (slot_id, room_id)
        self.faculty_schedule[mapping.faculty_id].add(slot_id)
        self.room_schedule[room_id].add(slot_id)
        self.section_schedule[batch_key].add(slot_id)
        
        # For labs, also mark the next slot
        if mapping.course.is_lab:
            slot = TimeSlot.query.get(slot_id)
            next_slot = TimeSlot.query.filter_by(day=slot.day, period=slot.period + 1).first()
            if next_slot:
                self.faculty_schedule[mapping.faculty_id].add(next_slot.id)
                self.room_schedule[room_id].add(next_slot.id)
                self.section_schedule[batch_key].add(next_slot.id)
    
    def _unassign(self, mapping_id):
        """Remove an assignment"""
        if mapping_id not in self.assignment:
            return
        
        mapping = FacultyCourse.query.get(mapping_id)
        slot_id, room_id = self.assignment[mapping_id]
        batch_key = mapping.batch_id if mapping.batch_id else 'section'
        
        self.faculty_schedule[mapping.faculty_id].discard(slot_id)
        self.room_schedule[room_id].discard(slot_id)
        self.section_schedule[batch_key].discard(slot_id)
        
        # For labs, also remove next slot
        if mapping.course.is_lab:
            slot = TimeSlot.query.get(slot_id)
            next_slot = TimeSlot.query.filter_by(day=slot.day, period=slot.period + 1).first()
            if next_slot:
                self.faculty_schedule[mapping.faculty_id].discard(next_slot.id)
                self.room_schedule[room_id].discard(next_slot.id)
                self.section_schedule[batch_key].discard(next_slot.id)
        
        del self.assignment[mapping_id]
    
    def _select_unassigned_variable(self, unassigned):
        """MRV heuristic: select variable with minimum remaining values"""
        min_domain_size = float('inf')
        selected = None
        
        for mapping_id in unassigned:
            valid_count = sum(1 for slot_id, room_id in self.domains[mapping_id] 
                            if self._is_consistent(mapping_id, slot_id, room_id))
            if valid_count < min_domain_size:
                min_domain_size = valid_count
                selected = mapping_id
        
        return selected
    
    def _order_domain_values(self, mapping_id):
        """Order domain values using least constraining value heuristic"""
        values = []
        for slot_id, room_id in self.domains[mapping_id]:
            if self._is_consistent(mapping_id, slot_id, room_id):
                # Score based on how many options it leaves for others
                values.append((slot_id, room_id))
        
        # Shuffle to add randomness
        random.shuffle(values)
        return values
    
    def solve(self):
        """Main solving method using backtracking"""
        # Create list of assignments needed per mapping based on hours
        assignments_needed = []
        for mapping in self.mappings:
            hours = self._get_required_hours(mapping)
            for _ in range(hours):
                assignments_needed.append(mapping.id)
        
        return self._backtrack(assignments_needed)
    
    def _backtrack(self, unassigned):
        """Backtracking search"""
        if not unassigned:
            return True  # All assigned successfully
        
        # Select next variable (mapping) to assign
        mapping_id = unassigned[0]
        remaining = unassigned[1:]
        
        # Try each value in domain
        for slot_id, room_id in self._order_domain_values(mapping_id):
            if self._is_consistent(mapping_id, slot_id, room_id):
                self._assign(mapping_id, slot_id, room_id)
                
                if self._backtrack(remaining):
                    return True
                
                self._unassign(mapping_id)
        
        return False
    
    def get_solution(self):
        """Get the current assignment as timetable entries"""
        entries = []
        
        for mapping_id, (slot_id, room_id) in self.assignment.items():
            mapping = FacultyCourse.query.get(mapping_id)
            
            entry = {
                'section_id': self.section_id,
                'course_id': mapping.course_id,
                'faculty_id': mapping.faculty_id,
                'room_id': room_id,
                'timeslot_id': slot_id,
                'batch_id': mapping.batch_id,
                'session_type': mapping.session_type
            }
            entries.append(entry)
            
            # For labs, add the consecutive period
            if mapping.course.is_lab:
                slot = TimeSlot.query.get(slot_id)
                next_slot = TimeSlot.query.filter_by(
                    day=slot.day, 
                    period=slot.period + 1
                ).first()
                
                if next_slot:
                    entry2 = entry.copy()
                    entry2['timeslot_id'] = next_slot.id
                    entries.append(entry2)
        
        return entries


def generate_initial_solution(section_id):
    """Generate an initial valid timetable using CSP"""
    solver = CSPSolver(section_id)
    
    if solver.solve():
        return {
            'success': True,
            'entries': solver.get_solution()
        }
    else:
        return {
            'success': False,
            'message': 'Could not find a valid initial solution'
        }
