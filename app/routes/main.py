"""Main routes blueprint - Dashboard and home"""
from flask import Blueprint, render_template, jsonify
from app.models import Course, Faculty, Room, Section, FacultyCourse, Timetable, GenerationLog
from app import db
import json
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page with statistics and overview"""
    # Get statistics
    stats = {
        'faculty_count': Faculty.query.count(),
        'room_count': Room.query.count(),
        'section_count': Section.query.count(),
        'course_count': Course.query.count(),
        'mapping_count': FacultyCourse.query.count(),
        'timetable_count': db.session.query(db.func.count(db.distinct(Timetable.section_id))).scalar() or 0
    }
    
    # Get recent generation logs
    recent_logs = GenerationLog.query.order_by(GenerationLog.created_at.desc()).limit(5).all()
    
    # Get all courses for modal
    courses = Course.query.order_by(Course.semester, Course.code).all()
    
    # Calculate semester-wise course distribution
    semester_theory = [0] * 8
    semester_labs = [0] * 8
    
    for course in courses:
        if 1 <= course.semester <= 8:
            idx = course.semester - 1
            if course.is_lab:
                semester_labs[idx] += 1
            else:
                semester_theory[idx] += 1
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_logs=recent_logs,
                         courses=courses,
                         semester_theory=semester_theory,
                         semester_labs=semester_labs)


@main_bp.route('/api/stats')
def get_stats():
    """API endpoint for dashboard statistics"""
    stats = {
        'faculty_count': Faculty.query.count(),
        'room_count': Room.query.count(),
        'section_count': Section.query.count(),
        'course_count': Course.query.count(),
        'mapping_count': FacultyCourse.query.count(),
        'timetable_count': db.session.query(db.func.count(db.distinct(Timetable.section_id))).scalar() or 0
    }
    return jsonify(stats)


@main_bp.route('/api/courses')
def get_courses():
    """API endpoint to get all courses"""
    courses = Course.query.order_by(Course.semester, Course.code).all()
    return jsonify([{
        'id': c.id,
        'code': c.code,
        'name': c.name,
        'semester': c.semester,
        'credits': c.credits,
        'category': c.category,
        'is_lab': c.is_lab,
        'lecture_hours': c.lecture_hours,
        'tutorial_hours': c.tutorial_hours,
        'practical_hours': c.practical_hours
    } for c in courses])


@main_bp.route('/api/courses/semester/<int:semester>')
def get_courses_by_semester(semester):
    """API endpoint to get courses by semester"""
    courses = Course.query.filter_by(semester=semester).order_by(Course.code).all()
    return jsonify([{
        'id': c.id,
        'code': c.code,
        'name': c.name,
        'credits': c.credits,
        'category': c.category,
        'is_lab': c.is_lab,
        'weekly_hours': c.weekly_hours
    } for c in courses])


@main_bp.route('/init-db')
def init_database():
    """Initialize database with courses and timeslots from JSON files"""
    try:
        # Load courses from JSON
        courses_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'courses.json')
        if os.path.exists(courses_file):
            with open(courses_file, 'r') as f:
                data = json.load(f)
                
            # Clear existing courses
            Course.query.delete()
            
            # Add courses
            for course_data in data.get('courses', []):
                course = Course(
                    code=course_data['code'],
                    name=course_data['name'],
                    semester=course_data['semester'],
                    credits=course_data['credits'],
                    category=course_data['category'],
                    course_type=course_data.get('course_type', 'T'),
                    lecture_hours=course_data.get('lecture_hours', 0),
                    tutorial_hours=course_data.get('tutorial_hours', 0),
                    practical_hours=course_data.get('practical_hours', 0),
                    is_lab=course_data.get('is_lab', False),
                    is_elective=course_data.get('is_elective', False),
                    elective_group=course_data.get('elective_group')
                )
                db.session.add(course)
        
        # Load timeslots from JSON
        from app.models import TimeSlot
        timeslots_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'timeslots.json')
        if os.path.exists(timeslots_file):
            with open(timeslots_file, 'r') as f:
                data = json.load(f)
            
            # Clear existing timeslots
            TimeSlot.query.delete()
            
            # Add timeslots
            for slot_data in data.get('timeslots', []):
                slot = TimeSlot(
                    day=slot_data['day'],
                    day_code=slot_data['day_code'],
                    period=slot_data['period'],
                    start_time=slot_data['start_time'],
                    end_time=slot_data['end_time'],
                    is_break=slot_data.get('is_break', False)
                )
                db.session.add(slot)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Database initialized with {Course.query.count()} courses and {TimeSlot.query.count()} timeslots'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected'
    })


@main_bp.route('/courses')
def courses_list():
    """Courses catalog page"""
    courses = Course.query.order_by(Course.semester, Course.code).all()
    return render_template('courses/list.html', courses=courses)
