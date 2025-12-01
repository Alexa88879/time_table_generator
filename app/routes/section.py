"""Section routes blueprint - CRUD operations for sections and batches"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Section, Batch, Course, FacultyCourse, Timetable
from app import db

section_bp = Blueprint('section', __name__, url_prefix='/sections')


@section_bp.route('/')
def list_sections():
    """List all sections"""
    sections = Section.query.order_by(Section.semester, Section.name).all()
    return render_template('section/list.html', sections=sections)


@section_bp.route('/add', methods=['GET', 'POST'])
def add_section():
    """Add a new section with batches"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            semester = int(request.form.get('semester'))
            department = request.form.get('department', 'CSE')
            total_students = int(request.form.get('total_students', 60))
            
            # Check if section already exists
            if Section.query.filter_by(name=name, semester=semester).first():
                flash('Section with this name already exists for this semester!', 'danger')
                return redirect(url_for('section.add_section'))
            
            section = Section(
                name=name,
                semester=semester,
                department=department,
                total_students=total_students
            )
            
            db.session.add(section)
            db.session.flush()  # Get section ID
            
            # Create batches (G1 and G2 for lab groups)
            create_batches = request.form.get('create_batches') == 'on'
            if create_batches:
                batch_count = int(request.form.get('batch_count', 2))
                students_per_batch = total_students // batch_count
                
                for i in range(1, batch_count + 1):
                    batch = Batch(
                        name=f"G{i}",
                        section_id=section.id,
                        student_count=students_per_batch
                    )
                    db.session.add(batch)
            
            db.session.commit()
            
            flash(f'Section "{name}" added successfully!', 'success')
            return redirect(url_for('section.list_sections'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding section: {str(e)}', 'danger')
            return redirect(url_for('section.add_section'))
    
    return render_template('section/form.html', section=None, action='add')


@section_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_section(id):
    """Edit an existing section"""
    section = Section.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            section.name = request.form.get('name')
            section.semester = int(request.form.get('semester'))
            section.department = request.form.get('department', 'CSE')
            section.total_students = int(request.form.get('total_students', 60))
            section.is_active = request.form.get('is_active') == 'on'
            
            db.session.commit()
            
            flash(f'Section "{section.name}" updated successfully!', 'success')
            return redirect(url_for('section.list_sections'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating section: {str(e)}', 'danger')
    
    return render_template('section/form.html', section=section, action='edit')


@section_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_section(id):
    """Delete a section and its batches"""
    try:
        section = Section.query.get_or_404(id)
        
        # Check if section has timetable entries
        if Timetable.query.filter_by(section_id=id).first():
            return jsonify({
                'success': False,
                'message': 'Cannot delete section with existing timetable entries.'
            }), 400
        
        # Check if section has faculty mappings
        if FacultyCourse.query.filter_by(section_id=id).first():
            return jsonify({
                'success': False,
                'message': 'Cannot delete section with existing faculty mappings.'
            }), 400
        
        # Delete batches first
        Batch.query.filter_by(section_id=id).delete()
        
        db.session.delete(section)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Section "{section.name}" deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@section_bp.route('/view/<int:id>')
def view_section(id):
    """View section details, batches and course mappings"""
    section = Section.query.get_or_404(id)
    
    # Get courses for this semester
    courses = Course.query.filter_by(semester=section.semester).order_by(Course.code).all()
    
    # Get faculty mappings for this section
    mappings = FacultyCourse.query.filter_by(section_id=id).all()
    
    return render_template('section/view.html', 
                         section=section, 
                         courses=courses,
                         mappings=mappings)


@section_bp.route('/batches/<int:section_id>', methods=['GET', 'POST'])
def manage_batches(section_id):
    """Manage batches for a section"""
    section = Section.query.get_or_404(section_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            try:
                name = request.form.get('batch_name')
                student_count = int(request.form.get('student_count', 30))
                
                batch = Batch(
                    name=name,
                    section_id=section_id,
                    student_count=student_count
                )
                db.session.add(batch)
                db.session.commit()
                
                flash(f'Batch "{name}" added successfully!', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding batch: {str(e)}', 'danger')
                
        elif action == 'delete':
            batch_id = request.form.get('batch_id')
            try:
                batch = Batch.query.get_or_404(batch_id)
                db.session.delete(batch)
                db.session.commit()
                flash('Batch deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting batch: {str(e)}', 'danger')
        
        return redirect(url_for('section.manage_batches', section_id=section_id))
    
    return render_template('section/batches.html', section=section)


@section_bp.route('/api/list')
def api_list_sections():
    """API endpoint to get all active sections"""
    sections = Section.query.filter_by(is_active=True).order_by(Section.semester, Section.name).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'semester': s.semester,
        'department': s.department,
        'total_students': s.total_students,
        'display_name': f"Sem {s.semester} - {s.name}"
    } for s in sections])


@section_bp.route('/api/semester/<int:semester>')
def api_sections_by_semester(semester):
    """API endpoint to get sections by semester"""
    sections = Section.query.filter_by(semester=semester, is_active=True).order_by(Section.name).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'total_students': s.total_students,
        'batches': [{'id': b.id, 'name': b.name} for b in s.batches]
    } for s in sections])


@section_bp.route('/api/<int:id>/batches')
def api_section_batches(id):
    """API endpoint to get batches for a section"""
    section = Section.query.get_or_404(id)
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'student_count': b.student_count
    } for b in section.batches])


@section_bp.route('/api/<int:id>/courses')
def api_section_courses(id):
    """API endpoint to get courses for a section's semester"""
    section = Section.query.get_or_404(id)
    courses = Course.query.filter_by(semester=section.semester).order_by(Course.code).all()
    return jsonify([{
        'id': c.id,
        'code': c.code,
        'name': c.name,
        'is_lab': c.is_lab,
        'weekly_hours': c.weekly_hours
    } for c in courses])


@section_bp.route('/bulk-create', methods=['GET', 'POST'])
def bulk_create_sections():
    """Bulk create sections for all semesters"""
    if request.method == 'POST':
        try:
            department = request.form.get('department', 'CSE')
            sections_per_semester = int(request.form.get('sections_per_semester', 2))
            students_per_section = int(request.form.get('students_per_section', 60))
            create_batches = request.form.get('create_batches') == 'on'
            
            section_names = ['A', 'B', 'C', 'D', 'E', 'F']
            created_count = 0
            
            for semester in range(1, 9):
                for i in range(sections_per_semester):
                    section_name = section_names[i] if i < len(section_names) else f"S{i+1}"
                    
                    # Check if section exists
                    if Section.query.filter_by(name=section_name, semester=semester, department=department).first():
                        continue
                    
                    section = Section(
                        name=section_name,
                        semester=semester,
                        department=department,
                        total_students=students_per_section
                    )
                    db.session.add(section)
                    db.session.flush()
                    
                    if create_batches:
                        for j in range(1, 3):  # G1 and G2
                            batch = Batch(
                                name=f"G{j}",
                                section_id=section.id,
                                student_count=students_per_section // 2
                            )
                            db.session.add(batch)
                    
                    created_count += 1
            
            db.session.commit()
            flash(f'Successfully created {created_count} sections!', 'success')
            return redirect(url_for('section.list_sections'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating sections: {str(e)}', 'danger')
    
    return render_template('section/bulk_create.html')
