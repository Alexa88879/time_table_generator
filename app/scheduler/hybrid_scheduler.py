"""Hybrid Scheduler - Combines CSP and Genetic Algorithm for optimal timetable generation"""
from app.models import (
    Section, Course, Faculty, Room, FacultyCourse,
    Section, Course, Faculty, Room, FacultyCourse,
    Timetable, TimeSlot, Batch, GenerationLog
)
from app import db
from app.scheduler.csp_solver import CSPSolver, generate_initial_solution
from app.scheduler.genetic_algorithm import GeneticAlgorithm
from app.scheduler.constraints import ConstraintChecker
import json
from collections import defaultdict


class HybridScheduler:
    """
    Hybrid scheduling approach:
    1. Use CSP to generate a valid initial solution
    2. Use Genetic Algorithm to optimize the solution
    3. Apply local search for fine-tuning
    """
    
    def __init__(self, section_id, config=None):
        self.section_id = section_id
        self.section = Section.query.get(section_id)
        self.config = config or {}
        
        # Validate section
        if not self.section:
            raise ValueError(f"Section {section_id} not found")
        
        # Load data
        self.mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
        self.timeslots = TimeSlot.query.filter_by(is_break=False).order_by(TimeSlot.day_index, TimeSlot.period).all()
        self.timeslot_ids = [t.id for t in self.timeslots]
        self.rooms = Room.query.filter_by(is_available=True).all()
        
        # Separate rooms by type
        self.classrooms = [r for r in self.rooms if not r.is_lab]
        self.labs = [r for r in self.rooms if r.is_lab]
        
        # Results
        self.result = None
    
    def validate_prerequisites(self):
        """Check if all prerequisites for scheduling are met"""
        errors = []
        
        if not self.mappings:
            errors.append(f"No faculty-course mappings found for section {self.section.name}")
        
        if not self.timeslots:
            errors.append("No timeslots defined")
        
        if not self.classrooms:
            errors.append("No classrooms available")
        
        # Check if labs are needed but not available
        lab_courses = [m for m in self.mappings if m.course.is_lab]
        if lab_courses and not self.labs:
            errors.append("Lab courses exist but no labs are available")
        
        # Check for unmapped courses
        semester_courses = Course.query.filter_by(semester=self.section.semester).all()
        mapped_course_ids = set(m.course_id for m in self.mappings)
        unmapped = [c for c in semester_courses if c.id not in mapped_course_ids and not c.is_elective]
        
        if unmapped:
            unmapped_codes = [c.code for c in unmapped]
            errors.append(f"Unmapped required courses: {', '.join(unmapped_codes)}")
        
        return errors
    
    def generate(self):
        """Main generation method - yields progress updates"""
        # Validate prerequisites
        errors = self.validate_prerequisites()
        if errors:
            yield {
                'type': 'error',
                'message': 'Prerequisites not met: ' + '; '.join(errors),
                'errors': errors
            }
            return
        
        # Clear existing timetable for this section
        Timetable.query.filter_by(section_id=self.section_id).delete()
        db.session.commit()
        
        try:
            # Step 1: Generate initial solution using CSP
            yield {
                'type': 'progress',
                'progress': 10,
                'status': 'Initializing',
                'substatus': 'CSP Solver',
                'message': f"Generating initial solution for section {self.section.name}..."
            }
            
            csp_result = generate_initial_solution(self.section_id)
            
            if csp_result['success']:
                initial_entries = csp_result['entries']
                yield {
                    'type': 'progress',
                    'progress': 20,
                    'status': 'Optimization',
                    'substatus': 'Genetic Algorithm',
                    'message': f"CSP generated {len(initial_entries)} entries. Starting optimization..."
                }
                
                # Step 2: Optimize using Genetic Algorithm
                use_ga = self.config.get('use_ga', True)
                
                if use_ga and len(initial_entries) > 5:
                    ga = GeneticAlgorithm(
                        self.section_id,
                        config={
                            'population_size': self.config.get('population_size', 30),
                            'max_generations': self.config.get('max_generations', 200),
                            'crossover_rate': self.config.get('crossover_rate', 0.85),
                            'mutation_rate': self.config.get('mutation_rate', 0.15)
                        }
                    )
                    
                    # Run GA and consume progress updates
                    ga_result = None
                    for progress in ga.run(initial_entries):
                        if 'best_chromosome' in progress and 'generation' not in progress:
                             # This is the final result
                             ga_result = progress
                        else:
                            # This is a progress update
                            percent = 20 + int((progress['generation'] / ga.max_generations) * 70)
                            yield {
                                'type': 'progress',
                                'progress': percent,
                                'status': 'Optimizing',
                                'substatus': f"Generation {progress['generation']}",
                                'generation': progress['generation'],
                                'fitness': progress['fitness'],
                                'message': f"Gen {progress['generation']}: Fitness {progress['fitness']}"
                            }
                            # Keep track of last result in case loop finishes
                            ga_result = progress
                    
                    # Use GA result if better
                    if ga_result and ga_result['best_chromosome'].fitness > 0:
                        entries = ga_result['best_chromosome'].to_entries()
                        fitness = ga_result['fitness']
                        generations = ga_result['generations']
                    else:
                        entries = initial_entries
                        fitness = 800  # Default for CSP solution
                        generations = 0
                else:
                    entries = initial_entries
                    fitness = 800
                    generations = 0
                    yield {
                        'type': 'progress',
                        'progress': 90,
                        'status': 'Finalizing',
                        'substatus': 'Saving results',
                        'message': "Skipping GA optimization..."
                    }
                
                # Step 3: Save to database
                self._save_entries(entries)
                
                # Step 4: Validate and get final stats
                checker = ConstraintChecker(self.section_id)
                validation = checker.check_all()
                
                self.result = {
                    'type': 'complete',
                    'success': True,
                    'message': 'Timetable generated successfully',
                    'fitness_score': validation['score'],
                    'generations': generations,
                    'hard_violations': len(validation['hard']),
                    'soft_violations': len(validation['soft']),
                    'entries_count': len(entries),
                    'section_id': self.section_id
                }
                
                yield self.result
                
            else:
                # CSP couldn't find solution, try greedy approach
                yield {
                    'type': 'progress',
                    'progress': 50,
                    'status': 'Fallback',
                    'substatus': 'Greedy Algorithm',
                    'message': "CSP failed, trying greedy approach..."
                }
                
                greedy_result = self._greedy_schedule()
                
                if greedy_result['success']:
                    self._save_entries(greedy_result['entries'])
                    
                    checker = ConstraintChecker(self.section_id)
                    validation = checker.check_all()
                    
                    yield {
                        'type': 'complete',
                        'success': True,
                        'message': 'Timetable generated (greedy approach)',
                        'fitness_score': validation['score'],
                        'generations': 0,
                        'hard_violations': len(validation['hard']),
                        'soft_violations': len(validation['soft']),
                        'entries_count': len(greedy_result['entries']),
                        'section_id': self.section_id
                    }
                else:
                    yield {
                        'type': 'error',
                        'success': False,
                        'message': 'Could not generate a valid timetable. Please check constraints and try again.'
                    }
                
        except Exception as e:
            db.session.rollback()
            yield {
                'type': 'error',
                'success': False,
                'message': f'Error during generation: {str(e)}'
            }
    
    def _greedy_schedule(self):
        """Fallback greedy scheduling approach"""
        entries = []
        used_slots = {
            'faculty': defaultdict(set),
            'room': defaultdict(set),
            'section': set(),
            'batch': defaultdict(set)
        }
        
        # Sort mappings: labs first (harder to schedule), then by weekly hours
        sorted_mappings = sorted(
            self.mappings,
            key=lambda m: (not m.course.is_lab, -m.course.weekly_hours)
        )
        
        for mapping in sorted_mappings:
            hours = self._get_required_hours(mapping)
            is_lab = mapping.course.is_lab
            available_rooms = self.labs if is_lab else self.classrooms
            
            if not available_rooms:
                continue
            
            scheduled_hours = 0
            
            for slot in self.timeslots:
                if scheduled_hours >= hours:
                    break
                
                # For labs, only start at odd periods
                if is_lab and slot.period not in [1, 3, 5, 7]:
                    continue
                
                for room in available_rooms:
                    if scheduled_hours >= hours:
                        break
                    
                    # Check constraints
                    if not self._is_slot_free(mapping, slot, room, used_slots):
                        continue
                    
                    # For labs, check consecutive slot
                    if is_lab:
                        next_slot = TimeSlot.query.filter_by(
                            day=slot.day,
                            period=slot.period + 1
                        ).first()
                        
                        if not next_slot or not self._is_slot_free(mapping, next_slot, room, used_slots):
                            continue
                    
                    # Schedule this slot
                    entry = {
                        'section_id': self.section_id,
                        'faculty_course_id': mapping.id,
                        'room_id': room.id,
                        'timeslot_id': slot.id,
                        'batch_id': mapping.batch_id,
                        'is_lab_slot': mapping.course.is_lab
                    }
                    entries.append(entry)
                    self._mark_used(mapping, slot, room, used_slots)
                    
                    # For labs, also schedule next period
                    if is_lab and next_slot:
                        entry2 = entry.copy()
                        entry2['timeslot_id'] = next_slot.id
                        entries.append(entry2)
                        self._mark_used(mapping, next_slot, room, used_slots)
                    
                    scheduled_hours += 2 if is_lab else 1
                    break
        
        return {
            'success': len(entries) > 0,
            'entries': entries
        }
    
    def _get_required_hours(self, mapping):
        """Get number of periods needed"""
        course = mapping.course
        if course.is_lab:
            return course.practical_hours or 2
        return (course.lecture_hours or 0) + (course.tutorial_hours or 0)
    
    def _is_slot_free(self, mapping, slot, room, used_slots):
        """Check if slot is available for this mapping"""
        # Faculty check
        if slot.id in used_slots['faculty'][mapping.faculty_id]:
            return False
        
        # Room check
        if slot.id in used_slots['room'][room.id]:
            return False
        
        # Section/batch check
        if mapping.batch_id:
            if slot.id in used_slots['batch'][mapping.batch_id]:
                return False
            if slot.id in used_slots['section']:
                return False
        else:
            if slot.id in used_slots['section']:
                return False
            # Check all batches
            for batch in self.section.batches:
                if slot.id in used_slots['batch'][batch.id]:
                    return False
        
        return True
    
    def _mark_used(self, mapping, slot, room, used_slots):
        """Mark slot as used"""
        used_slots['faculty'][mapping.faculty_id].add(slot.id)
        used_slots['room'][room.id].add(slot.id)
        
        if mapping.batch_id:
            used_slots['batch'][mapping.batch_id].add(slot.id)
        else:
            used_slots['section'].add(slot.id)
    
    def _save_entries(self, entries):
        """Save entries to database"""
        generation_id = GenerationLog.generate_id()
        for entry_data in entries:
            entry_data['generation_id'] = generation_id
            entry = Timetable(**entry_data)
            db.session.add(entry)
        
        db.session.commit()


def schedule_all_sections(sections=None):
    """Schedule multiple sections"""
    if sections is None:
        sections = Section.query.filter_by(is_active=True).all()
    
    results = []
    for section in sections:
        scheduler = HybridScheduler(section.id)
        # Consume generator to get final result
        result = None
        for progress in scheduler.generate():
            result = progress
            
        if result:
            result['section'] = {'id': section.id, 'name': section.name, 'semester': section.semester}
            results.append(result)
    
    return results
