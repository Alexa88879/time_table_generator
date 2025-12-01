#!/usr/bin/env python3
"""
B.Tech NEP 2020 Timetable Generator
AKTU CSE Curriculum - Hybrid GA+CSP Scheduler

Entry point for the Flask application
"""
import os
import sys
import json
from app import create_app, db
from app.models import Course, TimeSlot, Faculty, Room, Section, Batch


def load_default_data(app):
    """Load default courses and timeslots from JSON files"""
    with app.app_context():
        # Check if data already exists
        if Course.query.count() > 0 and TimeSlot.query.count() > 0:
            print("Default data already loaded.")
            return
        
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        # Load courses
        courses_file = os.path.join(data_dir, 'courses.json')
        if os.path.exists(courses_file):
            with open(courses_file, 'r') as f:
                courses_json = json.load(f)
            
            # Handle both formats: {"courses": [...]} or [...]
            courses_data = courses_json.get('courses', courses_json) if isinstance(courses_json, dict) else courses_json
            
            for course_data in courses_data:
                course = Course(
                    code=course_data['code'],
                    name=course_data['name'],
                    semester=course_data['semester'],
                    credits=course_data.get('credits', 0),
                    lecture_hours=course_data.get('lecture_hours', 0),
                    tutorial_hours=course_data.get('tutorial_hours', 0),
                    practical_hours=course_data.get('practical_hours', 0),
                    category=course_data.get('category', 'Core'),
                    course_type=course_data.get('course_type', 'T'),  # T (Theory) or P (Practical)
                    is_lab=course_data.get('is_lab', False),
                    is_elective=course_data.get('is_elective', False)
                )
                db.session.add(course)
            
            db.session.commit()
            print(f"Loaded {len(courses_data)} courses")
        
        # Load timeslots
        timeslots_file = os.path.join(data_dir, 'timeslots.json')
        if os.path.exists(timeslots_file):
            with open(timeslots_file, 'r') as f:
                timeslots_json = json.load(f)
            
            # Handle both formats: {"timeslots": [...]} or [...]
            timeslots_data = timeslots_json.get('timeslots', timeslots_json) if isinstance(timeslots_json, dict) else timeslots_json
            
            for slot_data in timeslots_data:
                # Generate slot_id from day and period (e.g., "MON-1")
                day_prefix = slot_data['day'][:3].upper()
                slot_id = f"{day_prefix}-{slot_data['period']}"
                
                timeslot = TimeSlot(
                    slot_id=slot_id,
                    day=slot_data['day'],
                    day_index=slot_data.get('day_code', slot_data.get('day_index', 0)),
                    period=slot_data['period'],
                    start_time=slot_data['start_time'],
                    end_time=slot_data['end_time'],
                    is_break=slot_data.get('is_break', False),
                    is_lunch=slot_data.get('is_lunch', False)
                )
                db.session.add(timeslot)
            
            db.session.commit()
            print(f"Loaded {len(timeslots_data)} timeslots")


def create_sample_data(app):
    """Create sample data for testing"""
    with app.app_context():
        # Check if sample data exists
        if Faculty.query.count() > 0:
            print("Sample data already exists.")
            return
        
        # Create sample faculty
        faculty_data = [
            {'faculty_id': 'FAC001', 'name': 'Dr. Amit Kumar', 'department': 'CSE', 'designation': 'Professor', 'max_hours_per_week': 16},
            {'faculty_id': 'FAC002', 'name': 'Dr. Priya Sharma', 'department': 'CSE', 'designation': 'Associate Professor', 'max_hours_per_week': 18},
            {'faculty_id': 'FAC003', 'name': 'Mr. Rahul Singh', 'department': 'CSE', 'designation': 'Assistant Professor', 'max_hours_per_week': 20},
            {'faculty_id': 'FAC004', 'name': 'Ms. Neha Gupta', 'department': 'CSE', 'designation': 'Assistant Professor', 'max_hours_per_week': 20},
            {'faculty_id': 'FAC005', 'name': 'Dr. Suresh Verma', 'department': 'MATH', 'designation': 'Professor', 'max_hours_per_week': 16},
            {'faculty_id': 'FAC006', 'name': 'Dr. Meena Rani', 'department': 'PHY', 'designation': 'Associate Professor', 'max_hours_per_week': 18},
            {'faculty_id': 'FAC007', 'name': 'Mr. Vijay Kumar', 'department': 'CSE', 'designation': 'Lab Instructor', 'max_hours_per_week': 24},
            {'faculty_id': 'FAC008', 'name': 'Ms. Anita Devi', 'department': 'CSE', 'designation': 'Lab Instructor', 'max_hours_per_week': 24},
        ]
        
        for f_data in faculty_data:
            faculty = Faculty(**f_data)
            db.session.add(faculty)
        
        db.session.commit()
        print(f"Created {len(faculty_data)} sample faculty members")
        
        # Create sample rooms
        room_data = [
            {'room_id': 'CR101', 'name': 'Classroom 101', 'capacity': 60, 'building': 'Main Block', 'floor': 1, 'room_type': 'Classroom'},
            {'room_id': 'CR102', 'name': 'Classroom 102', 'capacity': 60, 'building': 'Main Block', 'floor': 1, 'room_type': 'Classroom'},
            {'room_id': 'CR201', 'name': 'Classroom 201', 'capacity': 60, 'building': 'Main Block', 'floor': 2, 'room_type': 'Classroom'},
            {'room_id': 'CR202', 'name': 'Classroom 202', 'capacity': 60, 'building': 'Main Block', 'floor': 2, 'room_type': 'Classroom'},
            {'room_id': 'LAB-A', 'name': 'Computer Lab A', 'capacity': 30, 'building': 'Lab Complex', 'floor': 0, 'room_type': 'Lab', 'lab_type': 'Computer Lab'},
            {'room_id': 'LAB-B', 'name': 'Computer Lab B', 'capacity': 30, 'building': 'Lab Complex', 'floor': 0, 'room_type': 'Lab', 'lab_type': 'Programming Lab'},
            {'room_id': 'LAB-C', 'name': 'Network Lab', 'capacity': 25, 'building': 'Lab Complex', 'floor': 1, 'room_type': 'Lab', 'lab_type': 'Network Lab'},
            {'room_id': 'LAB-D', 'name': 'Hardware Lab', 'capacity': 25, 'building': 'Lab Complex', 'floor': 1, 'room_type': 'Lab', 'lab_type': 'Hardware Lab'},
        ]
        
        for r_data in room_data:
            room = Room(**r_data)
            db.session.add(room)
        
        db.session.commit()
        print(f"Created {len(room_data)} sample rooms")
        
        # Create sample sections with batches
        for sem in [1, 3]:  # Create for semesters 1 and 3
            for sec in ['A', 'B']:
                section_id = f"CSE-{sem}-{sec}"  # e.g., CSE-1-A
                section = Section(
                    section_id=section_id,
                    name=sec,
                    branch='CSE',
                    semester=sem,
                    strength=60,
                    batch_year=2024,
                    academic_year='2024-25',
                    is_active=True
                )
                db.session.add(section)
                db.session.flush()
                
                # Create batches with proper batch_id (e.g., CSE-1-A-G1)
                batch_g1 = Batch(batch_id=f"{section_id}-G1", name='G1', section_id=section.id, strength=30)
                batch_g2 = Batch(batch_id=f"{section_id}-G2", name='G2', section_id=section.id, strength=30)
                db.session.add(batch_g1)
                db.session.add(batch_g2)
        
        db.session.commit()
        print("Created sample sections with batches")


# Create the application
app = create_app()

if __name__ == '__main__':
    # Command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            # Initialize database with default data
            with app.app_context():
                db.create_all()
                print("Database tables created.")
            load_default_data(app)
            create_sample_data(app)
            print("Initialization complete!")
            
        elif command == 'load-courses':
            load_default_data(app)
            
        elif command == 'sample-data':
            create_sample_data(app)
            
        elif command == 'reset':
            # Reset database
            with app.app_context():
                db.drop_all()
                db.create_all()
                print("Database reset complete.")
            load_default_data(app)
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: init, load-courses, sample-data, reset")
    else:
        # Run the development server
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   B.Tech NEP 2020 Timetable Generator                        ║
║   AKTU CSE Curriculum - Hybrid GA+CSP Scheduler              ║
║                                                               ║
║   Starting development server...                              ║
║   Open http://127.0.0.1:5000 in your browser                 ║
║                                                               ║
║   First time? Run: python run.py init                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        # Ensure database is created
        with app.app_context():
            db.create_all()
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
