#!/usr/bin/env python3
"""
Utility script to seed data for 5th semester (sections + mappings)
without touching hardcoded JSON course/timeslot data.

Usage:
    python seed_sem5.py
"""

from app import create_app, db
from app.models import Section, Batch, Course, Faculty, FacultyCourse


app = create_app()
app.app_context().push()


def ensure_sem5_section():
    """Ensure at least one active 5th-semester section with G1/G2 batches."""
    section = Section.query.filter_by(semester=5, branch="CSE", name="A").first()

    if not section:
        section = Section(
            section_id="CSE-5-A",
            name="A",
            branch="CSE",
            semester=5,
            strength=60,
            batch_year=2024,
            academic_year="2024-25",
            is_active=True,
        )
        db.session.add(section)
        db.session.flush()

    # Ensure two lab batches (G1/G2)
    if section.batches.count() == 0:
        batch_g1 = Batch(
            batch_id=f"{section.section_id}-G1",
            name="G1",
            section_id=section.id,
            strength=section.batch_g1_strength,
        )
        batch_g2 = Batch(
            batch_id=f"{section.section_id}-G2",
            name="G2",
            section_id=section.id,
            strength=section.batch_g2_strength,
        )
        db.session.add(batch_g1)
        db.session.add(batch_g2)

    db.session.commit()
    return section


def seed_sem5_mappings(section: Section):
    """
    Create FacultyCourse mappings for all non‑elective 5th‑sem courses
    for the given section. Labs are mapped per batch, theory without batch.
    """
    # Get all non‑elective 5th‑sem courses (already hardcoded in courses.json)
    courses = Course.query.filter_by(semester=5).all()
    required_courses = [c for c in courses if not c.is_elective]

    if not required_courses:
        print("No 5th semester courses found in database. Run `python run.py init` first.")
        return

    # Use all active faculty in a round‑robin fashion
    faculty_list = Faculty.query.filter_by(is_active=True).order_by(Faculty.id).all()
    if not faculty_list:
        print("No faculty found. Run `python run.py sample-data` or create faculty first.")
        return

    batches = list(section.batches.all())

    created = 0
    for idx, course in enumerate(required_courses):
        faculty = faculty_list[idx % len(faculty_list)]

        if course.is_lab:
            # Practical: create mapping per batch
            for batch in batches:
                existing = FacultyCourse.query.filter_by(
                    faculty_id=faculty.id,
                    course_id=course.id,
                    section_id=section.id,
                    session_type="P",
                    batch_id=batch.id,
                    academic_year="2024-25",
                ).first()
                if existing:
                    continue

                mapping = FacultyCourse(
                    faculty_id=faculty.id,
                    course_id=course.id,
                    section_id=section.id,
                    session_type="P",
                    batch_id=batch.id,
                    academic_year="2024-25",
                )
                db.session.add(mapping)
                created += 1
                print(f"Mapped LAB {course.code} to {faculty.name} for {section.section_id} ({batch.name})")
        else:
            # Theory: single mapping for whole section
            existing = FacultyCourse.query.filter_by(
                faculty_id=faculty.id,
                course_id=course.id,
                section_id=section.id,
                session_type="L",
                batch_id=None,
                academic_year="2024-25",
            ).first()
            if existing:
                continue

            mapping = FacultyCourse(
                faculty_id=faculty.id,
                course_id=course.id,
                section_id=section.id,
                session_type="L",
                batch_id=None,
                academic_year="2024-25",
            )
            db.session.add(mapping)
            created += 1
            print(f"Mapped THEORY {course.code} to {faculty.name} for {section.section_id}")

    db.session.commit()
    print(f"Created {created} new mappings for section {section.section_id} (Sem {section.semester}).")


if __name__ == "__main__":
    sec = ensure_sem5_section()
    print(f"Using section {sec.section_id} (id={sec.id}, semester={sec.semester})")
    seed_sem5_mappings(sec)


