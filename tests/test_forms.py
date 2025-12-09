#test_forms.py
from app.forms import LoginForm


def test_login_form_valid_data(app):
    """LoginForm validates when all required fields are provided."""
    with app.test_request_context("/auth/login", method="POST"):
        form = LoginForm(
            meta={"csrf": False},  # disable CSRF at form level
            data={
                "username": "testuser",
                "password": "secret123",
                "remember_me": False,
            },
        )
        assert form.validate() is True


def test_login_form_missing_username_is_invalid(app):
    """LoginForm fails validation when username is missing."""
    with app.test_request_context("/auth/login", method="POST"):
        form = LoginForm(
            meta={"csrf": False},
            data={
                "username": "",
                "password": "secret123",
                "remember_me": False,
            },
        )
        assert form.validate() is False
        assert "username" in form.errors