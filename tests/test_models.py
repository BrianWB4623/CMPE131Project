# tests/test_models.py
from app import db
from app.models import User, Assignment, CourseMaterial


def test_user_creation_and_retrieval(app):
    """User saved and retrieved from database."""
    with app.app_context():
        user = User(
            username="rachel",
            email="rachel@example.com",
            password_hash="password123",
            role="student",
        )
        db.session.add(user)
        db.session.commit()

        fetched = User.query.filter_by(username="rachel").first()
        assert fetched is not None
        assert fetched.email == "rachel@example.com"
        assert fetched.role == "student"


def test_assignment_save_and_relationship(app):
    with app.app_context():
        instructor = User(
            username="jahan",
            email="jahan@example.com",
            password_hash="password123",
            role="instructor",
        )
        db.session.add(instructor)
        db.session.commit()

        assignment = Assignment(
            title="HW 1",
            description="Intro assignment",
            instructor_id=instructor.id,
        )
        db.session.add(assignment)
        db.session.commit()

        fetched = Assignment.query.first()
        assert fetched is not None
        assert fetched.title == "HW 1"
        assert fetched.instructor_id == instructor.id
        # relationship backref
        assert fetched.instructor.username == "jahan"


def test_course_material_save_and_relationship(app):
    """coursematerial link + query."""
    with app.app_context():
        instructor = User(
            username="brian",
            email="brian@example.com",
            password_hash="password123",
            role="instructor",
        )
        db.session.add(instructor)
        db.session.commit()

        material = CourseMaterial(
            title="Syllabus",
            description="Course overview",
            instructor_id=instructor.id,
        )
        db.session.add(material)
        db.session.commit()

        fetched = CourseMaterial.query.first()
        assert fetched is not None
        assert fetched.title == "Syllabus"
        assert fetched.instructor_id == instructor.id
        assert fetched.instructor.username == "brian"
