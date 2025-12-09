#test_routes.py
from flask import url_for


def test_assignments_list_route_loads(app, client):
    """The assignments list route returns HTTP 200."""
    response = client.get("/assignments")
    assert response.status_code == 200
    assert b"html" in response.data or response.mimetype == "text/html"


def test_materials_list_route_loads(app, client):
    """The materials list route returns HTTP 200."""
    response = client.get("/materials")
    assert response.status_code == 200
    assert response.mimetype == "text/html"


def test_create_assignment_requires_login(app, client):
    """Protected route should redirect anonymous users to login."""
    response = client.get("/assignments/create")
    # login_required should redirect to login view
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_create_assignment_accessible_after_login(app, client, instructor_user):
    """Logged-in instructor can load the assignment creation page."""
    # Log the user in via the real login route
    login_response = client.post(
        "/auth/login",
        data={
            "username": instructor_user.username,
            "password": "testpassword",
            "remember_me": False,
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    # Now access protected route
    response = client.get("/assignments/create")
    assert response.status_code == 200