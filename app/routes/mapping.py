"""Mapping routes blueprint - Faculty-Course-Section mappings"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Faculty, Course, Section, FacultyCourse, Batch
from app import db

mapping_bp = Blueprint('mapping', __name__, url_prefix='/mappings')


@mapping_bp.route('/')
def list_mappings():
    """List all faculty-course mappings"""
    mappings = FacultyCourse.query.order_by(
        FacultyCourse.section_id, 
        FacultyCourse.course_id
    ).all()
    
    # Group mappings by section for better display
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    
    return render_template('mapping/list.html', mappings=mappings, sections=sections)


@mapping_bp.route('/add', methods=['GET', 'POST'])
def add_mapping():
    """Add a new faculty-course mapping"""
    if request.method == 'POST':
        try:
            faculty_id = int(request.form.get('faculty_id'))
            course_id = int(request.form.get('course_id'))
            section_id = int(request.form.get('section_id'))
            session_type = request.form.get('session_type', 'theory')
            batch_id = request.form.get('batch_id')
            
            # Validate batch_id
            if batch_id:
                batch_id = int(batch_id)
            else:
                batch_id = None
            
            # Check if mapping already exists
            existing = FacultyCourse.query.filter_by(
                faculty_id=faculty_id,
                course_id=course_id,
                section_id=section_id,
                session_type=session_type,
                batch_id=batch_id
            ).first()
            
            if existing:
                flash('This mapping already exists!', 'warning')
                return redirect(url_for('mapping.add_mapping'))
            
            mapping = FacultyCourse(
                faculty_id=faculty_id,
                course_id=course_id,
                section_id=section_id,
                session_type=session_type,
                batch_id=batch_id
            )
            
            db.session.add(mapping)
            db.session.commit()
            
            flash('Faculty-Course mapping added successfully!', 'success')
            return redirect(url_for('mapping.list_mappings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding mapping: {str(e)}', 'danger')
            return redirect(url_for('mapping.add_mapping'))
    
    # GET request
    faculty = Faculty.query.filter_by(is_active=True).order_by(Faculty.name).all()
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    courses = Course.query.order_by(Course.semester, Course.code).all()
    
    return render_template('mapping/form.html', 
                         faculty=faculty, 
                         sections=sections, 
                         courses=courses,
                         mapping=None,
                         action='add')


@mapping_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_mapping(id):
    """Edit an existing mapping"""
    mapping = FacultyCourse.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            mapping.faculty_id = int(request.form.get('faculty_id'))
            mapping.course_id = int(request.form.get('course_id'))
            mapping.section_id = int(request.form.get('section_id'))
            mapping.session_type = request.form.get('session_type', 'theory')
            
            batch_id = request.form.get('batch_id')
            mapping.batch_id = int(batch_id) if batch_id else None
            
            db.session.commit()
            
            flash('Mapping updated successfully!', 'success')
            return redirect(url_for('mapping.list_mappings'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating mapping: {str(e)}', 'danger')
    
    faculty = Faculty.query.filter_by(is_active=True).order_by(Faculty.name).all()
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    courses = Course.query.order_by(Course.semester, Course.code).all()
    
    return render_template('mapping/form.html',
                         faculty=faculty,
                         sections=sections,
                         courses=courses,
                         mapping=mapping,
                         action='edit')


@mapping_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_mapping(id):
    """Delete a mapping"""
    try:
        mapping = FacultyCourse.query.get_or_404(id)
        db.session.delete(mapping)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mapping deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@mapping_bp.route('/section/<int:section_id>')
def view_section_mappings(section_id):
    """View all mappings for a section"""
    section = Section.query.get_or_404(section_id)
    mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
    
    # Get courses for this semester
    courses = Course.query.filter_by(semester=section.semester).order_by(Course.code).all()
    
    # Check which courses are mapped
    mapped_course_ids = [m.course_id for m in mappings]
    unmapped_courses = [c for c in courses if c.id not in mapped_course_ids]
    
    return render_template('mapping/section_view.html',
                         section=section,
                         mappings=mappings,
                         unmapped_courses=unmapped_courses)


@mapping_bp.route('/quick-add', methods=['GET', 'POST'])
def quick_add_mapping():
    """Quick add multiple mappings for a section"""
    if request.method == 'POST':
        try:
            section_id = int(request.form.get('section_id'))
            section = Section.query.get_or_404(section_id)
            
            # Get form data
            course_ids = request.form.getlist('course_ids')
            
            added_count = 0
            for course_id in course_ids:
                faculty_id = request.form.get(f'faculty_{course_id}')
                if not faculty_id:
                    continue
                    
                course = Course.query.get(int(course_id))
                if not course:
                    continue
                
                # Determine session type
                session_type = 'lab' if course.is_lab else 'theory'
                
                # For labs, create mappings for each batch
                if course.is_lab and section.batches:
                    for batch in section.batches:
                        # Check if mapping exists
                        existing = FacultyCourse.query.filter_by(
                            faculty_id=int(faculty_id),
                            course_id=int(course_id),
                            section_id=section_id,
                            batch_id=batch.id
                        ).first()
                        
                        if not existing:
                            mapping = FacultyCourse(
                                faculty_id=int(faculty_id),
                                course_id=int(course_id),
                                section_id=section_id,
                                session_type=session_type,
                                batch_id=batch.id
                            )
                            db.session.add(mapping)
                            added_count += 1
                else:
                    # Theory course - no batch
                    existing = FacultyCourse.query.filter_by(
                        faculty_id=int(faculty_id),
                        course_id=int(course_id),
                        section_id=section_id,
                        batch_id=None
                    ).first()
                    
                    if not existing:
                        mapping = FacultyCourse(
                            faculty_id=int(faculty_id),
                            course_id=int(course_id),
                            section_id=section_id,
                            session_type=session_type,
                            batch_id=None
                        )
                        db.session.add(mapping)
                        added_count += 1
            
            db.session.commit()
            flash(f'Successfully added {added_count} mappings!', 'success')
            return redirect(url_for('mapping.view_section_mappings', section_id=section_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding mappings: {str(e)}', 'danger')
            return redirect(url_for('mapping.quick_add_mapping'))
    
    # GET request
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    faculty = Faculty.query.filter_by(is_active=True).order_by(Faculty.name).all()
    
    return render_template('mapping/quick_add.html', sections=sections, faculty=faculty)


@mapping_bp.route('/api/section/<int:section_id>')
def api_section_mappings(section_id):
    """API endpoint to get mappings for a section"""
    mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
    return jsonify([{
        'id': m.id,
        'faculty': {'id': m.faculty.id, 'name': m.faculty.name, 'code': m.faculty.code},
        'course': {'id': m.course.id, 'code': m.course.code, 'name': m.course.name, 'is_lab': m.course.is_lab},
        'session_type': m.session_type,
        'batch': {'id': m.batch.id, 'name': m.batch.name} if m.batch else None
    } for m in mappings])


@mapping_bp.route('/api/faculty/<int:faculty_id>')
def api_faculty_mappings(faculty_id):
    """API endpoint to get mappings for a faculty member"""
    mappings = FacultyCourse.query.filter_by(faculty_id=faculty_id).all()
    return jsonify([{
        'id': m.id,
        'course': {'id': m.course.id, 'code': m.course.code, 'name': m.course.name},
        'section': {'id': m.section.id, 'name': m.section.name, 'semester': m.section.semester},
        'session_type': m.session_type,
        'batch': {'id': m.batch.id, 'name': m.batch.name} if m.batch else None
    } for m in mappings])


@mapping_bp.route('/api/check-conflicts')
def api_check_conflicts():
    """API endpoint to check for mapping conflicts"""
    section_id = request.args.get('section_id', type=int)
    
    if not section_id:
        return jsonify({'error': 'section_id is required'}), 400
    
    section = Section.query.get_or_404(section_id)
    courses = Course.query.filter_by(semester=section.semester).all()
    mappings = FacultyCourse.query.filter_by(section_id=section_id).all()
    
    # Check for unmapped courses
    mapped_course_ids = set(m.course_id for m in mappings)
    unmapped = [c for c in courses if c.id not in mapped_course_ids]
    
    # Check for faculty overload
    faculty_loads = {}
    for m in mappings:
        if m.faculty_id not in faculty_loads:
            faculty_loads[m.faculty_id] = {
                'faculty': m.faculty,
                'hours': 0,
                'courses': []
            }
        faculty_loads[m.faculty_id]['hours'] += m.course.weekly_hours
        faculty_loads[m.faculty_id]['courses'].append(m.course)
    
    overloaded = [
        f for f in faculty_loads.values() 
        if f['hours'] > f['faculty'].max_hours_per_week
    ]
    
    return jsonify({
        'unmapped_courses': [{'id': c.id, 'code': c.code, 'name': c.name} for c in unmapped],
        'overloaded_faculty': [{
            'faculty': {'id': f['faculty'].id, 'name': f['faculty'].name},
            'assigned_hours': f['hours'],
            'max_hours': f['faculty'].max_hours_per_week
        } for f in overloaded]
    })
