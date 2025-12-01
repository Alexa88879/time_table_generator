"""Upload routes blueprint - Excel file upload and processing"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models import Faculty, Room, Section, Batch, Course, FacultyCourse
from app import db
import pandas as pd
import os
import json

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/')
def index():
    """Upload page with dropzone"""
    return render_template('upload/index.html')


@upload_bp.route('/faculty', methods=['POST'])
def upload_faculty():
    """Upload faculty data from Excel"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file type. Use .xlsx, .xls, or .csv'}), 400
    
    try:
        # Read the file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Expected columns: Name, Code, Email, Phone, Department, Designation, Max Hours/Week, Max Hours/Day
        required_columns = ['Name', 'Code']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'success': False, 'message': f'Missing required column: {col}'}), 400
        
        added_count = 0
        updated_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                name = str(row['Name']).strip()
                code = str(row['Code']).strip().upper()
                
                if not name or not code or name == 'nan' or code == 'nan':
                    continue
                
                # Check if faculty exists
                faculty = Faculty.query.filter_by(code=code).first()
                
                if faculty:
                    # Update existing
                    faculty.name = name
                    faculty.email = str(row.get('Email', '')).strip() if pd.notna(row.get('Email')) else None
                    faculty.phone = str(row.get('Phone', '')).strip() if pd.notna(row.get('Phone')) else None
                    faculty.department = str(row.get('Department', 'CSE')).strip()
                    faculty.designation = str(row.get('Designation', '')).strip() if pd.notna(row.get('Designation')) else None
                    faculty.max_hours_per_week = int(row.get('Max Hours/Week', 18)) if pd.notna(row.get('Max Hours/Week')) else 18
                    faculty.max_hours_per_day = int(row.get('Max Hours/Day', 6)) if pd.notna(row.get('Max Hours/Day')) else 6
                    updated_count += 1
                else:
                    # Add new
                    faculty = Faculty(
                        name=name,
                        code=code,
                        email=str(row.get('Email', '')).strip() if pd.notna(row.get('Email')) else None,
                        phone=str(row.get('Phone', '')).strip() if pd.notna(row.get('Phone')) else None,
                        department=str(row.get('Department', 'CSE')).strip(),
                        designation=str(row.get('Designation', '')).strip() if pd.notna(row.get('Designation')) else None,
                        max_hours_per_week=int(row.get('Max Hours/Week', 18)) if pd.notna(row.get('Max Hours/Week')) else 18,
                        max_hours_per_day=int(row.get('Max Hours/Day', 6)) if pd.notna(row.get('Max Hours/Day')) else 6
                    )
                    db.session.add(faculty)
                    added_count += 1
                    
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        db.session.commit()
        
        message = f'Added {added_count}, Updated {updated_count} faculty members.'
        if errors:
            message += f' {len(errors)} errors occurred.'
        
        return jsonify({
            'success': True,
            'message': message,
            'added': added_count,
            'updated': updated_count,
            'errors': errors[:10]  # Return first 10 errors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@upload_bp.route('/rooms', methods=['POST'])
def upload_rooms():
    """Upload rooms/labs data from Excel"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file'}), 400
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Expected columns: Name, Code, Capacity, Is Lab, Lab Type, Building, Floor
        required_columns = ['Name', 'Code']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'success': False, 'message': f'Missing required column: {col}'}), 400
        
        added_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            try:
                name = str(row['Name']).strip()
                room_id = str(row['Code']).strip().upper()
                
                if not name or not room_id or name == 'nan' or room_id == 'nan':
                    continue
                
                is_lab_val = row.get('Is Lab', False)
                is_lab = is_lab_val in [True, 'Yes', 'yes', 'YES', 1, '1', 'True', 'true']
                room_type = 'Lab' if is_lab else 'Classroom'
                
                room = Room.query.filter_by(room_id=room_id).first()
                
                if room:
                    room.name = name
                    room.capacity = int(row.get('Capacity', 60)) if pd.notna(row.get('Capacity')) else 60
                    room.room_type = room_type
                    room.lab_type = str(row.get('Lab Type', '')).strip() if is_lab and pd.notna(row.get('Lab Type')) else None
                    room.building = str(row.get('Building', '')).strip() if pd.notna(row.get('Building')) else None
                    room.floor = str(row.get('Floor', '')).strip() if pd.notna(row.get('Floor')) else None
                    updated_count += 1
                else:
                    room = Room(
                        name=name,
                        room_id=room_id,
                        capacity=int(row.get('Capacity', 60)) if pd.notna(row.get('Capacity')) else 60,
                        room_type=room_type,
                        lab_type=str(row.get('Lab Type', '')).strip() if is_lab and pd.notna(row.get('Lab Type')) else None,
                        building=str(row.get('Building', '')).strip() if pd.notna(row.get('Building')) else None,
                        floor=str(row.get('Floor', '')).strip() if pd.notna(row.get('Floor')) else None
                    )
                    db.session.add(room)
                    added_count += 1
                    
            except Exception as e:
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Added {added_count}, Updated {updated_count} rooms/labs.',
            'added': added_count,
            'updated': updated_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@upload_bp.route('/sections', methods=['POST'])
def upload_sections():
    """Upload sections data from Excel"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file'}), 400
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Expected columns: Name, Semester, Department, Total Students, Create Batches
        required_columns = ['Name', 'Semester']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'success': False, 'message': f'Missing required column: {col}'}), 400
        
        added_count = 0
        
        for index, row in df.iterrows():
            try:
                name = str(row['Name']).strip()
                semester = int(row['Semester'])
                
                if not name or name == 'nan' or semester < 1 or semester > 8:
                    continue
                
                # Check if section exists
                if Section.query.filter_by(name=name, semester=semester).first():
                    continue
                
                department = str(row.get('Department', 'CSE')).strip()
                total_students = int(row.get('Total Students', 60)) if pd.notna(row.get('Total Students')) else 60
                
                section = Section(
                    name=name,
                    semester=semester,
                    department=department,
                    total_students=total_students
                )
                db.session.add(section)
                db.session.flush()
                
                # Create batches if specified
                create_batches = row.get('Create Batches', True)
                if create_batches in [True, 'Yes', 'yes', 'YES', 1, '1', 'True', 'true']:
                    for i in range(1, 3):
                        batch = Batch(
                            name=f"G{i}",
                            section_id=section.id,
                            student_count=total_students // 2
                        )
                        db.session.add(batch)
                
                added_count += 1
                
            except Exception as e:
                continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Added {added_count} sections with batches.',
            'added': added_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@upload_bp.route('/mappings', methods=['POST'])
def upload_mappings():
    """Upload faculty-course mappings from Excel"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file'}), 400
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Expected columns: Faculty Code, Course Code, Section Name, Semester, Session Type, Batch (optional)
        required_columns = ['Faculty Code', 'Course Code', 'Section Name', 'Semester']
        for col in required_columns:
            if col not in df.columns:
                return jsonify({'success': False, 'message': f'Missing required column: {col}'}), 400
        
        added_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                faculty_code = str(row['Faculty Code']).strip().upper()
                course_code = str(row['Course Code']).strip().upper()
                section_name = str(row['Section Name']).strip()
                semester = int(row['Semester'])
                
                # Find faculty
                faculty = Faculty.query.filter_by(code=faculty_code).first()
                if not faculty:
                    errors.append(f"Row {index + 2}: Faculty '{faculty_code}' not found")
                    continue
                
                # Find course
                course = Course.query.filter_by(code=course_code).first()
                if not course:
                    errors.append(f"Row {index + 2}: Course '{course_code}' not found")
                    continue
                
                # Find section
                section = Section.query.filter_by(name=section_name, semester=semester).first()
                if not section:
                    errors.append(f"Row {index + 2}: Section '{section_name}' Sem {semester} not found")
                    continue
                
                # Determine session type
                session_type = str(row.get('Session Type', '')).strip().lower()
                if not session_type or session_type == 'nan':
                    session_type = 'lab' if course.is_lab else 'theory'
                
                # Handle batch
                batch_id = None
                batch_name = str(row.get('Batch', '')).strip() if pd.notna(row.get('Batch')) else None
                if batch_name and batch_name != 'nan':
                    batch = Batch.query.filter_by(section_id=section.id, name=batch_name).first()
                    if batch:
                        batch_id = batch.id
                
                # Check if mapping exists
                existing = FacultyCourse.query.filter_by(
                    faculty_id=faculty.id,
                    course_id=course.id,
                    section_id=section.id,
                    batch_id=batch_id
                ).first()
                
                if not existing:
                    mapping = FacultyCourse(
                        faculty_id=faculty.id,
                        course_id=course.id,
                        section_id=section.id,
                        session_type=session_type,
                        batch_id=batch_id
                    )
                    db.session.add(mapping)
                    added_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        db.session.commit()
        
        message = f'Added {added_count} mappings.'
        if errors:
            message += f' {len(errors)} errors occurred.'
        
        return jsonify({
            'success': True,
            'message': message,
            'added': added_count,
            'errors': errors[:10]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@upload_bp.route('/template/<data_type>')
def download_template(data_type):
    """Download Excel template for data upload"""
    from io import BytesIO
    from flask import send_file
    
    templates = {
        'faculty': {
            'columns': ['Name', 'Code', 'Email', 'Phone', 'Department', 'Designation', 'Max Hours/Week', 'Max Hours/Day'],
            'sample': [['Dr. John Smith', 'JS001', 'john@college.edu', '9876543210', 'CSE', 'Professor', 18, 6]]
        },
        'rooms': {
            'columns': ['Name', 'Code', 'Capacity', 'Is Lab', 'Lab Type', 'Building', 'Floor'],
            'sample': [['Computer Lab 1', 'CL01', 60, 'Yes', 'Computer', 'Block A', '2nd']]
        },
        'sections': {
            'columns': ['Name', 'Semester', 'Department', 'Total Students', 'Create Batches'],
            'sample': [['A', 1, 'CSE', 60, 'Yes']]
        },
        'mappings': {
            'columns': ['Faculty Code', 'Course Code', 'Section Name', 'Semester', 'Session Type', 'Batch'],
            'sample': [['JS001', 'BCS301', 'A', 3, 'theory', '']]
        }
    }
    
    if data_type not in templates:
        return jsonify({'error': 'Invalid template type'}), 400
    
    template = templates[data_type]
    df = pd.DataFrame(template['sample'], columns=template['columns'])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'{data_type}_template.xlsx'
    )


@upload_bp.route('/load-defaults', methods=['POST'])
def load_defaults():
    """Load default AKTU CSE NEP 2020 courses and timeslots from JSON files"""
    import json
    import os
    from flask import current_app
    from app.models import Course
    
    try:
        # Load courses from JSON
        courses_file = os.path.join(current_app.root_path, '..', 'data', 'courses.json')
        if os.path.exists(courses_file):
            with open(courses_file, 'r') as f:
                courses_data = json.load(f)
            
            added_count = 0
            for course_data in courses_data:
                # Check if course already exists
                existing = Course.query.filter_by(code=course_data['code']).first()
                if not existing:
                    course = Course(
                        code=course_data['code'],
                        name=course_data['name'],
                        semester=course_data['semester'],
                        credits=course_data.get('credits', 3),
                        course_type=course_data.get('course_type', 'Theory'),
                        lecture_hours=course_data.get('lecture_hours', 3),
                        tutorial_hours=course_data.get('tutorial_hours', 0),
                        practical_hours=course_data.get('practical_hours', 0)
                    )
                    db.session.add(course)
                    added_count += 1
            
            db.session.commit()
            flash(f'Successfully loaded {added_count} courses from default data!', 'success')
        else:
            flash('Default courses file not found!', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error loading defaults: {str(e)}', 'danger')
    
    return redirect(url_for('upload.index'))
