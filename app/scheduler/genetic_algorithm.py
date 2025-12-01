"""Genetic Algorithm for timetable optimization"""
from app.models import (
    Section, Course, Faculty, Room, FacultyCourse,
    Timetable, TimeSlot, Batch
)
from app import db
from app.scheduler.constraints import calculate_fitness
from app.scheduler.csp_solver import CSPSolver
import random
import copy
from flask import current_app


class Chromosome:
    """Represents a timetable solution as a chromosome"""
    
    def __init__(self, section_id, genes=None):
        self.section_id = section_id
        self.genes = genes or []  # List of (mapping_id, timeslot_id, room_id)
        self.fitness = 0
        self.hard_violations = 0
        self.soft_violations = 0
    
    def calculate_fitness(self):
        """Calculate fitness score for this chromosome"""
        # Temporarily save to database to check constraints
        # This is a simplified approach - in production, use in-memory checking
        
        # Clear existing entries for this section
        Timetable.query.filter_by(section_id=self.section_id).delete()
        
        # Add new entries from genes
        for gene in self.genes:
            mapping_id, slot_id, room_id, batch_id = gene
            mapping = FacultyCourse.query.get(mapping_id)
            
            entry = Timetable(
                generation_id='temp_gen_id',
                section_id=self.section_id,
                faculty_course_id=mapping.id,
                room_id=room_id,
                timeslot_id=slot_id,
                batch_id=batch_id,
                is_lab_slot=mapping.course.is_lab
            )
            db.session.add(entry)
        
        db.session.flush()
        
        # Calculate fitness
        self.fitness, hard, soft = calculate_fitness(self.section_id)
        self.hard_violations = len(hard)
        self.soft_violations = len(soft)
        
        # Rollback the temporary entries
        db.session.rollback()
        
        return self.fitness
    
    def to_entries(self):
        """Convert genes to timetable entries"""
        entries = []
        for gene in self.genes:
            mapping_id, slot_id, room_id, batch_id = gene
            mapping = FacultyCourse.query.get(mapping_id)
            
            entries.append({
                'section_id': self.section_id,
                'faculty_course_id': mapping.id,
                'room_id': room_id,
                'timeslot_id': slot_id,
                'batch_id': batch_id,
                'is_lab_slot': mapping.course.is_lab
            })
        
        return entries


class GeneticAlgorithm:
    """Genetic Algorithm for optimizing timetables"""
    
    def __init__(self, section_id, config=None):
        self.section_id = section_id
        self.section = Section.query.get(section_id)
        
        # Configuration
        self.config = config or {}
        self.population_size = self.config.get('population_size', 50)
        self.max_generations = self.config.get('max_generations', 500)
        self.crossover_rate = self.config.get('crossover_rate', 0.85)
        self.mutation_rate = self.config.get('mutation_rate', 0.15)
        self.elitism_count = self.config.get('elitism_count', 2)
        self.tournament_size = self.config.get('tournament_size', 3)
        
        # Data
        self.mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
        self.timeslots = TimeSlot.query.order_by(TimeSlot.day_index, TimeSlot.period).all()
        self.rooms = Room.query.filter_by(is_available=True).all()
        self.classrooms = [r for r in self.rooms if not r.is_lab]
        self.labs = [r for r in self.rooms if r.is_lab]
        
        self.population = []
        self.best_chromosome = None
        self.generation = 0
    
    def initialize_population(self, initial_solution=None):
        """Initialize population with CSP-generated solutions"""
        self.population = []
        
        # If we have an initial solution from CSP, use it as seed
        if initial_solution:
            chromosome = self._solution_to_chromosome(initial_solution)
            self.population.append(chromosome)
        
        # Generate rest of population
        while len(self.population) < self.population_size:
            chromosome = self._generate_random_chromosome()
            if chromosome:
                self.population.append(chromosome)
        
        # Calculate fitness for all
        for chromosome in self.population:
            chromosome.calculate_fitness()
        
        # Sort by fitness
        self.population.sort(key=lambda c: c.fitness, reverse=True)
        self.best_chromosome = self.population[0]
    
    def _solution_to_chromosome(self, solution):
        """Convert CSP solution to chromosome"""
        genes = []
        for entry in solution:
            mapping = FacultyCourse.query.filter_by(
                course_id=entry['course_id'],
                faculty_id=entry['faculty_id'],
                section_id=entry['section_id'],
                batch_id=entry.get('batch_id')
            ).first()
            
            if mapping:
                genes.append((
                    mapping.id,
                    entry['timeslot_id'],
                    entry['room_id'],
                    entry.get('batch_id')
                ))
        
        return Chromosome(self.section_id, genes)
    
    def _generate_random_chromosome(self):
        """Generate a random chromosome"""
        genes = []
        used_slots = {
            'faculty': {},    # faculty_id -> set of slot_ids
            'room': {},       # room_id -> set of slot_ids
            'section': set(), # slot_ids for whole section
            'batch': {}       # batch_id -> set of slot_ids
        }
        
        for mapping in self.mappings:
            hours = self._get_hours(mapping)
            is_lab = mapping.course.is_lab
            rooms = self.labs if is_lab else self.classrooms
            
            if not rooms:
                continue
            
            for _ in range(hours):
                # Find valid slot
                valid_found = False
                attempts = 0
                max_attempts = 100
                
                while not valid_found and attempts < max_attempts:
                    attempts += 1
                    
                    # Pick random slot and room
                    slot = random.choice(self.timeslots)
                    room = random.choice(rooms)
                    
                    # Skip invalid lab start periods
                    if is_lab and slot.period not in [1, 3, 5, 7]:
                        continue
                    
                    # Check constraints
                    faculty_id = mapping.faculty_id
                    batch_id = mapping.batch_id
                    
                    if faculty_id not in used_slots['faculty']:
                        used_slots['faculty'][faculty_id] = set()
                    if room.id not in used_slots['room']:
                        used_slots['room'][room.id] = set()
                    if batch_id and batch_id not in used_slots['batch']:
                        used_slots['batch'][batch_id] = set()
                    
                    # Check if slot is free
                    if slot.id in used_slots['faculty'][faculty_id]:
                        continue
                    if slot.id in used_slots['room'][room.id]:
                        continue
                    
                    if batch_id:
                        if slot.id in used_slots['batch'].get(batch_id, set()):
                            continue
                        if slot.id in used_slots['section']:
                            continue
                    else:
                        if slot.id in used_slots['section']:
                            continue
                        # Check all batches
                        batch_conflict = any(
                            slot.id in used_slots['batch'].get(b.id, set())
                            for b in self.section.batches
                        )
                        if batch_conflict:
                            continue
                    
                    # For labs, check consecutive slot
                    if is_lab:
                        next_slot = TimeSlot.query.filter_by(
                            day=slot.day,
                            period=slot.period + 1
                        ).first()
                        
                        if not next_slot:
                            continue
                        if next_slot.id in used_slots['faculty'][faculty_id]:
                            continue
                        if next_slot.id in used_slots['room'][room.id]:
                            continue
                    
                    # Valid slot found
                    valid_found = True
                    
                    # Mark as used
                    used_slots['faculty'][faculty_id].add(slot.id)
                    used_slots['room'][room.id].add(slot.id)
                    
                    if batch_id:
                        used_slots['batch'][batch_id].add(slot.id)
                    else:
                        used_slots['section'].add(slot.id)
                    
                    if is_lab and next_slot:
                        used_slots['faculty'][faculty_id].add(next_slot.id)
                        used_slots['room'][room.id].add(next_slot.id)
                        if batch_id:
                            used_slots['batch'][batch_id].add(next_slot.id)
                        else:
                            used_slots['section'].add(next_slot.id)
                    
                    genes.append((mapping.id, slot.id, room.id, batch_id))
                    
                    if is_lab and next_slot:
                        genes.append((mapping.id, next_slot.id, room.id, batch_id))
        
        return Chromosome(self.section_id, genes)
    
    def _get_hours(self, mapping):
        """Get required hours for a mapping"""
        course = mapping.course
        if course.is_lab:
            return 1  # Labs counted as single 2-hour block
        return course.lecture_hours + course.tutorial_hours
    
    def select_parent(self):
        """Tournament selection"""
        tournament = random.sample(self.population, min(self.tournament_size, len(self.population)))
        return max(tournament, key=lambda c: c.fitness)
    
    def crossover(self, parent1, parent2):
        """Single-point crossover"""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Simple crossover: swap some genes
        genes1 = copy.deepcopy(parent1.genes)
        genes2 = copy.deepcopy(parent2.genes)
        
        if len(genes1) > 1 and len(genes2) > 1:
            point = random.randint(1, min(len(genes1), len(genes2)) - 1)
            genes1[point:], genes2[point:] = genes2[point:], genes1[point:]
        
        child1 = Chromosome(self.section_id, genes1)
        child2 = Chromosome(self.section_id, genes2)
        
        return child1, child2
    
    def mutate(self, chromosome):
        """Mutation: randomly change some gene values"""
        if random.random() > self.mutation_rate:
            return chromosome
        
        genes = copy.deepcopy(chromosome.genes)
        
        if genes:
            # Pick random gene to mutate
            idx = random.randint(0, len(genes) - 1)
            mapping_id, old_slot, old_room, batch_id = genes[idx]
            
            mapping = FacultyCourse.query.get(mapping_id)
            is_lab = mapping.course.is_lab
            
            # Pick new random slot and room
            rooms = self.labs if is_lab else self.classrooms
            if rooms:
                new_room = random.choice(rooms)
                new_slot = random.choice(self.timeslots)
                
                if is_lab and new_slot.period not in [1, 3, 5, 7]:
                    # Keep original if invalid
                    pass
                else:
                    genes[idx] = (mapping_id, new_slot.id, new_room.id, batch_id)
        
        return Chromosome(self.section_id, genes)
    
    def evolve(self):
        """Evolve population for one generation"""
        new_population = []
        
        # Elitism: keep best chromosomes
        new_population.extend(self.population[:self.elitism_count])
        
        # Generate rest through selection, crossover, mutation
        while len(new_population) < self.population_size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            new_population.extend([child1, child2])
        
        # Trim to population size
        self.population = new_population[:self.population_size]
        
        # Calculate fitness
        for chromosome in self.population:
            chromosome.calculate_fitness()
        
        # Sort by fitness
        self.population.sort(key=lambda c: c.fitness, reverse=True)
        
        # Update best
        if self.population[0].fitness > self.best_chromosome.fitness:
            self.best_chromosome = copy.deepcopy(self.population[0])
        
        self.generation += 1
    
    def run(self, initial_solution=None):
        """Run the genetic algorithm"""
        self.initialize_population(initial_solution)
        
        no_improvement_count = 0
        previous_best = self.best_chromosome.fitness
        
        for gen in range(self.max_generations):
            self.evolve()
            
            # Check for improvement
            if self.best_chromosome.fitness > previous_best:
                no_improvement_count = 0
                previous_best = self.best_chromosome.fitness
            else:
                no_improvement_count += 1
            
            # Yield progress
            yield {
                'generation': self.generation,
                'fitness': self.best_chromosome.fitness,
                'hard_violations': self.best_chromosome.hard_violations,
                'soft_violations': self.best_chromosome.soft_violations,
                'best_chromosome': self.best_chromosome
            }
            
            # Early stopping if perfect solution found
            if self.best_chromosome.hard_violations == 0 and self.best_chromosome.fitness >= 900:
                break
            
            # Early stopping if no improvement for many generations
            if no_improvement_count > 100:
                break
        
        yield {
            'best_chromosome': self.best_chromosome,
            'generations': self.generation,
            'fitness': self.best_chromosome.fitness,
            'hard_violations': self.best_chromosome.hard_violations,
            'soft_violations': self.best_chromosome.soft_violations
        }
