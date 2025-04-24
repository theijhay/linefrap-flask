import io
import pytest
from app import create_app

def test_upload_no_file(client):
    response = client.post('/', data={})
    assert b"No file selected" in response.data

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client