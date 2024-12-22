import pytest
from main import app
import test_config
from models import Base, engine

@pytest.fixture(autouse=True)
def setup_test_database():
    # Create all tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Test Task'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'
    assert response.json['completed'] == False

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_task(client):
    # First create a task
    create_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = create_response.json['id']
    
    # Then update it
    update_response = client.put(f'/tasks/{task_id}', 
                               json={'title': 'Updated Task', 'completed': True})
    assert update_response.status_code == 200
    assert update_response.json['title'] == 'Updated Task'
    assert update_response.json['completed'] == True
