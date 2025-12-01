"""Faculty routes blueprint - CRUD operations for faculty members"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Faculty, FacultyCourse, Course, Section
from app import db
import json

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')


@faculty_bp.route('/')
def list_faculty():
    """List all faculty members"""
    faculty_list = Faculty.query.order_by(Faculty.name).all()
    return render_template('faculty/list.html', faculty=faculty_list)


@faculty_bp.route('/add', methods=['GET', 'POST'])
def add_faculty():
    """Add a new faculty member"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            code = request.form.get('code')
            email = request.form.get('email')
            phone = request.form.get('phone')
            department = request.form.get('department', 'CSE')
            designation = request.form.get('designation')
            max_hours_per_week = int(request.form.get('max_hours_per_week', 18))
            max_hours_per_day = int(request.form.get('max_hours_per_day', 6))
            
            # Parse preferred slots
            preferred_slots = request.form.getlist('preferred_slots')
            unavailable_slots = request.form.getlist('unavailable_slots')
            
            # Check if code already exists
            if Faculty.query.filter_by(code=code).first():
                flash('Faculty code already exists!', 'danger')
                return redirect(url_for('faculty.add_faculty'))
            
            faculty = Faculty(
                name=name,
                code=code,
                email=email,
                phone=phone,
                department=department,
                designation=designation,
                max_hours_per_week=max_hours_per_week,
                max_hours_per_day=max_hours_per_day,
                preferred_slots=json.dumps(preferred_slots) if preferred_slots else None,
                unavailable_slots=json.dumps(unavailable_slots) if unavailable_slots else None
            )
            
            db.session.add(faculty)
            db.session.commit()
            
            flash(f'Faculty "{name}" added successfully!', 'success')
            return redirect(url_for('faculty.list_faculty'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding faculty: {str(e)}', 'danger')
            return redirect(url_for('faculty.add_faculty'))
    
    # GET request - show form
    return render_template('faculty/form.html', faculty=None, action='add')


@faculty_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    """Edit an existing faculty member"""
    faculty = Faculty.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            faculty.name = request.form.get('name')
            faculty.code = request.form.get('code')
            faculty.email = request.form.get('email')
            faculty.phone = request.form.get('phone')
            faculty.department = request.form.get('department', 'CSE')
            faculty.designation = request.form.get('designation')
            faculty.max_hours_per_week = int(request.form.get('max_hours_per_week', 18))
            faculty.max_hours_per_day = int(request.form.get('max_hours_per_day', 6))
            faculty.is_active = request.form.get('is_active') == 'on'
            
            # Parse preferred slots
            preferred_slots = request.form.getlist('preferred_slots')
            unavailable_slots = request.form.getlist('unavailable_slots')
            faculty.preferred_slots = json.dumps(preferred_slots) if preferred_slots else None
            faculty.unavailable_slots = json.dumps(unavailable_slots) if unavailable_slots else None
            
            db.session.commit()
            
            flash(f'Faculty "{faculty.name}" updated successfully!', 'success')
            return redirect(url_for('faculty.list_faculty'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating faculty: {str(e)}', 'danger')
    
    return render_template('faculty/form.html', faculty=faculty, action='edit')


@faculty_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_faculty(id):
    """Delete a faculty member"""
    try:
        faculty = Faculty.query.get_or_404(id)
        
        # Check if faculty has course mappings
        if faculty.course_mappings:
            return jsonify({
                'success': False,
                'message': 'Cannot delete faculty with existing course mappings. Remove mappings first.'
            }), 400
        
        db.session.delete(faculty)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Faculty "{faculty.name}" deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@faculty_bp.route('/view/<int:id>')
def view_faculty(id):
    """View faculty details and their course mappings"""
    faculty = Faculty.query.get_or_404(id)
    mappings = FacultyCourse.query.filter_by(faculty_id=id).all()
    
    return render_template('faculty/view.html', faculty=faculty, mappings=mappings)


@faculty_bp.route('/preferences/<int:id>', methods=['GET', 'POST'])
def faculty_preferences(id):
    """Manage faculty time preferences"""
    faculty = Faculty.query.get_or_404(id)
    
    from app.models import TimeSlot
    timeslots = TimeSlot.query.order_by(TimeSlot.day_code, TimeSlot.period).all()
    
    # Group timeslots by day
    slots_by_day = {}
    for slot in timeslots:
        if slot.day not in slots_by_day:
            slots_by_day[slot.day] = []
        slots_by_day[slot.day].append(slot)
    
    if request.method == 'POST':
        try:
            preferred = request.form.getlist('preferred_slots')
            unavailable = request.form.getlist('unavailable_slots')
            
            faculty.preferred_slots = json.dumps(preferred) if preferred else None
            faculty.unavailable_slots = json.dumps(unavailable) if unavailable else None
            
            db.session.commit()
            flash('Preferences updated successfully!', 'success')
            return redirect(url_for('faculty.view_faculty', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating preferences: {str(e)}', 'danger')
    
    # Get current preferences
    preferred = json.loads(faculty.preferred_slots) if faculty.preferred_slots else []
    unavailable = json.loads(faculty.unavailable_slots) if faculty.unavailable_slots else []
    
    return render_template('faculty/preferences.html', 
                         faculty=faculty, 
                         slots_by_day=slots_by_day,
                         preferred=preferred,
                         unavailable=unavailable)


@faculty_bp.route('/api/list')
def api_list_faculty():
    """API endpoint to get all faculty"""
    faculty_list = Faculty.query.filter_by(is_active=True).order_by(Faculty.name).all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'code': f.code,
        'department': f.department,
        'designation': f.designation
    } for f in faculty_list])


@faculty_bp.route('/api/<int:id>')
def api_get_faculty(id):
    """API endpoint to get single faculty details"""
    faculty = Faculty.query.get_or_404(id)
    return jsonify({
        'id': faculty.id,
        'name': faculty.name,
        'code': faculty.code,
        'email': faculty.email,
        'phone': faculty.phone,
        'department': faculty.department,
        'designation': faculty.designation,
        'max_hours_per_week': faculty.max_hours_per_week,
        'max_hours_per_day': faculty.max_hours_per_day,
        'preferred_slots': json.loads(faculty.preferred_slots) if faculty.preferred_slots else [],
        'unavailable_slots': json.loads(faculty.unavailable_slots) if faculty.unavailable_slots else []
    })
