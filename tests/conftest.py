import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Every test gets a new app instance created and configured"""
    app = create_app()

    # Test-specific config
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # disable CSRF for easier form testing
    )

    with app.app_context():
        # Start from a clean DB for each test session
        db.drop_all()
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def instructor_user(app):
    """Sample Instructor for database"""
    with app.app_context():
        user = User(
            username="Professor Rojas",
            email="crojas@example.com",
            password_hash="testpassword",  # app compares plain text
            role="instructor",
        )
        db.session.add(user)
        db.session.commit()
        return user
