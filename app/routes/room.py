"""Room routes blueprint - CRUD operations for rooms and labs"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Room, Timetable
from app import db

room_bp = Blueprint('room', __name__, url_prefix='/rooms')


@room_bp.route('/')
def list_rooms():
    """List all rooms and labs"""
    rooms = Room.query.order_by(Room.room_type.desc(), Room.name).all()
    return render_template('room/list.html', rooms=rooms)


@room_bp.route('/add', methods=['GET', 'POST'])
def add_room():
    """Add a new room or lab"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            room_id = request.form.get('code')
            capacity = int(request.form.get('capacity', 60))
            is_lab = request.form.get('is_lab') == 'on'
            room_type = 'Lab' if is_lab else 'Classroom'
            lab_type = request.form.get('lab_type') if is_lab else None
            building = request.form.get('building')
            floor = request.form.get('floor')
            
            # Check if code already exists
            if Room.query.filter_by(room_id=room_id).first():
                flash('Room code already exists!', 'danger')
                return redirect(url_for('room.add_room'))
            
            room = Room(
                name=name,
                room_id=room_id,
                capacity=capacity,
                room_type=room_type,
                lab_type=lab_type,
                building=building,
                floor=floor
            )
            
            db.session.add(room)
            db.session.commit()
            
            flash(f'{"Lab" if is_lab else "Room"} "{name}" added successfully!', 'success')
            return redirect(url_for('room.list_rooms'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding room: {str(e)}', 'danger')
            return redirect(url_for('room.add_room'))
    
    return render_template('room/form.html', room=None, action='add')


@room_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    """Edit an existing room"""
    room = Room.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            room.name = request.form.get('name')
            room.room_id = request.form.get('code')
            room.capacity = int(request.form.get('capacity', 60))
            is_lab = request.form.get('is_lab') == 'on'
            room.room_type = 'Lab' if is_lab else 'Classroom'
            room.lab_type = request.form.get('lab_type') if is_lab else None
            room.building = request.form.get('building')
            room.floor = request.form.get('floor')
            room.is_available = request.form.get('is_active') == 'on'
            
            db.session.commit()
            
            flash(f'{"Lab" if room.is_lab else "Room"} "{room.name}" updated successfully!', 'success')
            return redirect(url_for('room.list_rooms'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating room: {str(e)}', 'danger')
    
    return render_template('room/form.html', room=room, action='edit')


@room_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_room(id):
    """Delete a room"""
    try:
        room = Room.query.get_or_404(id)
        
        # Check if room is used in timetables
        if Timetable.query.filter_by(room_id=id).first():
            return jsonify({
                'success': False,
                'message': 'Cannot delete room with existing timetable entries.'
            }), 400
        
        db.session.delete(room)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{"Lab" if room.is_lab else "Room"} "{room.name}" deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@room_bp.route('/view/<int:id>')
def view_room(id):
    """View room details and schedule"""
    room = Room.query.get_or_404(id)
    
    # Get timetable entries for this room
    entries = Timetable.query.filter_by(room_id=id).all()
    
    return render_template('room/view.html', room=room, entries=entries)


@room_bp.route('/api/list')
def api_list_rooms():
    """API endpoint to get all active rooms"""
    rooms = Room.query.filter_by(is_available=True).order_by(Room.room_type.desc(), Room.name).all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'code': r.code,
        'capacity': r.capacity,
        'is_lab': r.is_lab,
        'lab_type': r.lab_type,
        'building': r.building,
        'floor': r.floor
    } for r in rooms])


@room_bp.route('/api/labs')
def api_list_labs():
    """API endpoint to get all labs"""
    labs = Room.query.filter_by(is_lab=True, is_active=True).order_by(Room.name).all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'code': r.code,
        'capacity': r.capacity,
        'lab_type': r.lab_type
    } for r in labs])


@room_bp.route('/api/classrooms')
def api_list_classrooms():
    """API endpoint to get all classrooms (non-labs)"""
    classrooms = Room.query.filter_by(is_lab=False, is_active=True).order_by(Room.name).all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'code': r.code,
        'capacity': r.capacity
    } for r in classrooms])


@room_bp.route('/api/available')
def api_available_rooms():
    """API endpoint to get available rooms for a specific timeslot"""
    day = request.args.get('day')
    period = request.args.get('period', type=int)
    section_id = request.args.get('section_id', type=int)
    is_lab = request.args.get('is_lab', 'false').lower() == 'true'
    
    from app.models import TimeSlot
    
    # Get timeslot
    timeslot = TimeSlot.query.filter_by(day=day, period=period).first()
    if not timeslot:
        return jsonify([])
    
    # Get all rooms of required type
    query = Room.query.filter_by(is_active=True, is_lab=is_lab)
    all_rooms = query.all()
    
    # Get rooms already booked at this timeslot
    booked_rooms = db.session.query(Timetable.room_id).filter(
        Timetable.timeslot_id == timeslot.id
    ).all()
    booked_ids = [r[0] for r in booked_rooms]
    
    # Filter available rooms
    available = [r for r in all_rooms if r.id not in booked_ids]
    
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'code': r.code,
        'capacity': r.capacity
    } for r in available])
