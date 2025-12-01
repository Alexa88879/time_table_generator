"""Timetable routes blueprint - Generation and viewing"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import (
    Section, Course, Faculty, Room, FacultyCourse, 
    Timetable, TimeSlot, GenerationLog, Batch
)
from app import db
from datetime import datetime
import json

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')


from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response, stream_with_context

# ... imports ...

@timetable_bp.route('/generate-stream')
def generate_stream():
    """Stream generation progress via SSE"""
    section_id = request.args.get('section_id', type=int)
    config_str = request.args.get('config', '{}')
    try:
        config = json.loads(config_str)
    except:
        config = {}
    
    if not section_id:
        return jsonify({'error': 'Section ID required'}), 400

    def generate():
        from app.scheduler.hybrid_scheduler import HybridScheduler
        scheduler = HybridScheduler(section_id, config)
        
        for progress in scheduler.generate():
            yield f"data: {json.dumps(progress)}\n\n"
            
    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@timetable_bp.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate timetable page"""
    if request.method == 'POST':
        try:
            # Handle JSON or Form data
            if request.is_json:
                data = request.json
                section_id = int(data.get('section_id'))
                algorithm = data.get('algorithm', 'hybrid')
                config = data
            else:
                section_id = int(request.form.get('section_id'))
                algorithm = request.form.get('algorithm', 'hybrid')
                config = {}
            
            # Start generation log
            log = GenerationLog(
                section_id=section_id,
                algorithm=algorithm,
                status='running'
            )
            db.session.add(log)
            db.session.commit()
            
            # Import and run scheduler
            from app.scheduler.hybrid_scheduler import HybridScheduler
            
            scheduler = HybridScheduler(section_id, config)
            
            # Consume generator to get final result
            final_result = None
            for progress in scheduler.generate():
                final_result = progress
            
            if final_result and final_result.get('success'):
                log.status = 'completed'
                log.fitness_score = final_result.get('fitness_score', 0)
                log.generations_run = final_result.get('generations', 0)
                log.hard_constraint_violations = final_result.get('hard_violations', 0)
                log.soft_constraint_violations = final_result.get('soft_violations', 0)
                log.completed_at = datetime.utcnow()
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Timetable generated successfully!',
                    'log_id': log.id,
                    'fitness': final_result.get('fitness_score', 0),
                    'redirect': url_for('timetable.view', section_id=section_id),
                    'section_id': section_id
                })
            else:
                log.status = 'failed'
                log.error_message = final_result.get('message', 'Unknown error') if final_result else 'Unknown error'
                db.session.commit()
                
                return jsonify({
                    'success': False,
                    'message': final_result.get('message', 'Failed to generate timetable') if final_result else 'Failed to generate timetable'
                }), 400
                
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    # GET request
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    return render_template('timetable/generate.html', sections=sections)


@timetable_bp.route('/view/<int:section_id>')
def view(section_id):
    """View timetable for a section"""
    section = Section.query.get_or_404(section_id)
    
    # Get timeslots
    timeslots = TimeSlot.query.order_by(TimeSlot.day_index, TimeSlot.period).all()
    
    # Group by day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    slots_by_day = {day: [] for day in days}
    for slot in timeslots:
        if slot.day in slots_by_day:
            slots_by_day[slot.day].append(slot)
    
    # Get timetable entries for this section
    entries = Timetable.query.filter_by(section_id=section_id).all()
    
    # Get batches for lab view
    batches = Batch.query.filter_by(section_id=section_id).all()
    
    return render_template(
        'timetable/view.html',
        section=section,
        days=days,
        slots_by_day=slots_by_day,
        entries=entries,
        batches=batches
    )


@timetable_bp.route('/view-all')
def view_all():
    """View all generated timetables"""
    # Get sections with timetables
    sections_with_tt = db.session.query(Section).join(
        Timetable, Section.id == Timetable.section_id
    ).distinct().order_by(Section.semester, Section.name).all()
    
    # Get recent logs
    logs = GenerationLog.query.order_by(GenerationLog.created_at.desc()).limit(20).all()
    
    return render_template('timetable/list.html', sections=sections_with_tt, logs=logs)


@timetable_bp.route('/edit/<int:section_id>')
def edit(section_id):
    """Edit timetable for a section"""
    section = Section.query.get_or_404(section_id)
    
    # Get all required data
    timeslots = TimeSlot.query.order_by(TimeSlot.day_index, TimeSlot.period).all()
    rooms = Room.query.filter_by(is_active=True).order_by(Room.name).all()
    mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
    entries = Timetable.query.filter_by(section_id=section_id).all()
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    return render_template('timetable/edit.html',
                         section=section,
                         timeslots=timeslots,
                         rooms=rooms,
                         mappings=mappings,
                         entries=entries,
                         days=days)


@timetable_bp.route('/delete/<int:section_id>', methods=['DELETE'])
def delete(section_id):
    """Delete timetable for a section"""
    try:
        Timetable.query.filter_by(section_id=section_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Timetable deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@timetable_bp.route('/api/entry', methods=['POST'])
def add_entry():
    """Add or update a timetable entry"""
    try:
        data = request.json
        
        section_id = data.get('section_id')
        timeslot_id = data.get('timeslot_id')
        mapping_id = data.get('mapping_id')
        room_id = data.get('room_id')
        batch_id = data.get('batch_id')
        
        # Get mapping details
        mapping = FacultyCourse.query.get(mapping_id)
        if not mapping:
            return jsonify({'success': False, 'message': 'Invalid mapping'}), 400
        
        # Check for conflicts
        conflicts = check_conflicts(section_id, timeslot_id, mapping, room_id, batch_id)
        if conflicts:
            return jsonify({'success': False, 'message': conflicts}), 400
        
        # Create entry
        entry = Timetable(
            section_id=section_id,
            faculty_course_id=mapping.id,
            room_id=room_id,
            timeslot_id=timeslot_id,
            batch_id=batch_id,
            is_lab_slot=mapping.course.is_lab,
            generation_id=GenerationLog.generate_id()
        )
        
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entry added successfully!',
            'entry_id': entry.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@timetable_bp.route('/api/entry/<int:id>', methods=['DELETE'])
def delete_entry(id):
    """Delete a timetable entry"""
    try:
        entry = Timetable.query.get_or_404(id)
        db.session.delete(entry)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Entry deleted!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@timetable_bp.route('/api/section/<int:section_id>')
def api_get_timetable(section_id):
    """API endpoint to get timetable data"""
    entries = Timetable.query.filter_by(section_id=section_id).all()
    
    return jsonify([{
        'id': e.id,
        'day': e.timeslot.day,
        'period': e.timeslot.period,
        'start_time': e.timeslot.start_time,
        'end_time': e.timeslot.end_time,
        'course': {'code': e.course.code, 'name': e.course.name, 'is_lab': e.course.is_lab},
        'faculty': {'name': e.faculty.name, 'code': e.faculty.code},
        'room': {'name': e.room.name, 'code': e.room.code} if e.room else None,
        'batch': {'name': e.batch.name} if e.batch else None,
        'session_type': e.session_type
    } for e in entries])


@timetable_bp.route('/api/faculty/<int:faculty_id>')
def api_faculty_timetable(faculty_id):
    """Get timetable for a faculty member"""
    entries = Timetable.query.filter_by(faculty_id=faculty_id).all()
    
    return jsonify([{
        'id': e.id,
        'day': e.timeslot.day,
        'period': e.timeslot.period,
        'start_time': e.timeslot.start_time,
        'end_time': e.timeslot.end_time,
        'course': {'code': e.course.code, 'name': e.course.name},
        'section': {'name': e.section.name, 'semester': e.section.semester},
        'room': {'name': e.room.name} if e.room else None,
        'batch': {'name': e.batch.name} if e.batch else None
    } for e in entries])


@timetable_bp.route('/api/room/<int:room_id>')
def api_room_timetable(room_id):
    """Get timetable for a room"""
    entries = Timetable.query.filter_by(room_id=room_id).all()
    
    return jsonify([{
        'id': e.id,
        'day': e.timeslot.day,
        'period': e.timeslot.period,
        'start_time': e.timeslot.start_time,
        'end_time': e.timeslot.end_time,
        'course': {'code': e.course.code, 'name': e.course.name},
        'section': {'name': e.section.name, 'semester': e.section.semester},
        'faculty': {'name': e.faculty.name}
    } for e in entries])


@timetable_bp.route('/api/validate/<int:section_id>')
def api_validate_timetable(section_id):
    """Validate timetable and return conflicts"""
    from app.scheduler.constraints import ConstraintChecker
    
    checker = ConstraintChecker(section_id)
    violations = checker.check_all()
    
    return jsonify({
        'valid': len(violations['hard']) == 0,
        'hard_violations': violations['hard'],
        'soft_violations': violations['soft'],
        'score': violations['score']
    })


@timetable_bp.route('/regenerate/<int:section_id>', methods=['POST'])
def regenerate(section_id):
    """Regenerate timetable for a section"""
    try:
        # Delete existing timetable
        Timetable.query.filter_by(section_id=section_id).delete()
        db.session.commit()
        
        # Trigger generation (same as POST to /generate)
        return redirect(url_for('timetable.generate'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('timetable.view', section_id=section_id))


def check_conflicts(section_id, timeslot_id, mapping, room_id, batch_id=None):
    """Check for scheduling conflicts"""
    timeslot = TimeSlot.query.get(timeslot_id)
    
    # 1. Faculty conflict - faculty already teaching at this time
    # 1. Faculty conflict - faculty already teaching at this time
    faculty_conflict = Timetable.query.join(FacultyCourse).filter(
        FacultyCourse.faculty_id == mapping.faculty_id,
        Timetable.timeslot_id == timeslot_id
    ).first()
    
    if faculty_conflict:
        return f"Faculty {mapping.faculty.name} is already scheduled at this time"
    
    # 2. Room conflict - room already in use
    room_conflict = Timetable.query.filter_by(
        room_id=room_id,
        timeslot_id=timeslot_id
    ).first()
    
    if room_conflict:
        return f"Room is already booked at this time"
    
    # 3. Section conflict (for theory classes) - section already has a class
    if not batch_id:
        section_conflict = Timetable.query.filter_by(
            section_id=section_id,
            timeslot_id=timeslot_id,
            batch_id=None
        ).first()
        
        if section_conflict:
            return "Section already has a theory class at this time"
    
    # 4. Batch conflict - batch already has a class
    if batch_id:
        batch_conflict = Timetable.query.filter_by(
            section_id=section_id,
            timeslot_id=timeslot_id,
            batch_id=batch_id
        ).first()
        
        if batch_conflict:
            return "Batch already has a class at this time"
    
    # 5. Lab period validation - labs must start at odd periods and have 2 consecutive slots
    if mapping.course.is_lab:
        if timeslot.period not in [1, 3, 5, 7]:
            return "Labs must start at period 1, 3, 5, or 7"
    
    return None
