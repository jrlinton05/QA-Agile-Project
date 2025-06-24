import pytest
from flask_login import login_user
from Source.flask_app import app as flask_app_instance
from Source.Models.user import User


@pytest.fixture()
def client():
    flask_app_instance.config['TESTING'] = True
    flask_app_instance.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF if used
    with flask_app_instance.test_client() as client:
        yield client


def login_as(client, is_admin=False):
    with flask_app_instance.test_request_context():
        user = User("testuser", is_admin)
        login_user(user)


def test_root_redirects_to_login_if_not_authenticated(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data.lower()


def test_logout_redirects_to_root(client):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith("/")


def test_products_requires_login(client):
    response = client.get("/products", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_review_page_requires_login(client):
    response = client.get("/products/sample_product_id", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_delete_review_requires_login(client):
    response = client.post("/delete-review/sample_review_id", data={"product_id": "sample_product_id"}, follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_edit_review_requires_login(client):
    response = client.get("/edit-review/sample_product_id/sample_review_id", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_admin_page_requires_login(client):
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']


def test_create_product_request_requires_login(client):
    response = client.post("/create-product-request", data={}, follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers['Location']
