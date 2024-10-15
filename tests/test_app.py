import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_init_database(client):
    response = client.post('/init_database')
    assert response.status_code == 200
    assert b'Database initialized successfully' in response.data

def test_accidents_by_area(client):
    response = client.get('/accidents_by_area/1234')
    assert response.status_code == 200
    data = response.get_json()
    assert 'beat' in data
    assert 'total_accidents' in data

def test_accidents_by_area_time(client):
    response = client.get('/accidents_by_area_time/1234/month?start_date=01/01/2023 12:00:00 AM&end_date=01/31/2023 11:59:59 PM')
    assert response.status_code == 200
    data = response.get_json()
    assert 'beat' in data
    assert 'period' in data
    assert 'total_accidents' in data

def test_accidents_by_cause(client):
    response = client.get('/accidents_by_cause/1234')
    assert response.status_code == 200
    data = response.get_json()
    assert 'beat' in data
    assert 'causes' in data
    assert isinstance(data['causes'], list)

def test_injury_stats(client):
    response = client.get('/injury_stats/1234')
    assert response.status_code == 200
    data = response.get_json()
    assert 'beat' in data
    assert 'total_injuries' in data
    assert 'fatal_injuries' in data
    assert 'incapacitating_injuries' in data
    assert 'non_incapacitating_injuries' in data
    assert 'fatal_accidents' in data