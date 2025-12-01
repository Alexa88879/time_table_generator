from app import create_app, db
from app.models import Section, Course, Faculty, FacultyCourse, Batch

app = create_app()
app.app_context().push()

def create_mappings():
    print("Creating mappings...")
    
    # Get Section 1 (Sem 1)
    section = Section.query.filter_by(semester=1).first()
    if not section:
        print("Section not found!")
        return

    # Get Courses for Sem 1
    courses = Course.query.filter_by(semester=1).all()
    
    # Get Faculties
    faculties = Faculty.query.all()
    if not faculties:
        print("No faculty found!")
        return

    # Create mappings
    # Assign each course to a faculty
    for i, course in enumerate(courses):
        faculty = faculties[i % len(faculties)]
        
        # Theory mapping
        if not course.is_lab:
            mapping = FacultyCourse(
                faculty_id=faculty.id,
                course_id=course.id,
                section_id=section.id,
                session_type='L'
            )
            db.session.add(mapping)
            print(f"Mapped {course.code} to {faculty.name} (Theory)")
            
        # Lab mapping
        else:
            # For labs, we need batches
            for batch in section.batches:
                mapping = FacultyCourse(
                    faculty_id=faculty.id,
                    course_id=course.id,
                    section_id=section.id,
                    session_type='P',
                    batch_id=batch.id
                )
                db.session.add(mapping)
                print(f"Mapped {course.code} to {faculty.name} (Lab - {batch.name})")

    db.session.commit()
    print("Mappings created successfully!")

if __name__ == "__main__":
    create_mappings()
