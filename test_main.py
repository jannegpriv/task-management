import pytest
from main import app
import test_config
from models import Base, engine, SessionLocal, TaskStatus
from sqlalchemy import text
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from urllib.parse import urlparse

def parse_db_url(url):
    """Parse DATABASE_URL into connection parameters."""
    parsed = urlparse(url)
    return {
        'dbname': 'postgres',  # Initially connect to default db
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port or 5432
    }

def wait_for_db(max_retries=5, retry_interval=2):
    """Wait for database to be ready."""
    retries = 0
    while retries < max_retries:
        try:
            url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/taskmanagement')
            conn_params = parse_db_url(url)
            conn = psycopg2.connect(**conn_params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            conn.close()
            return True
        except psycopg2.OperationalError:
            retries += 1
            if retries == max_retries:
                raise
            time.sleep(retry_interval)
    return False

def create_test_db():
    """Create test database if it doesn't exist."""
    url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/taskmanagement')
    conn_params = parse_db_url(url)
    
    conn = psycopg2.connect(**conn_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'test_taskmanagement'")
    if not cur.fetchone():
        cur.execute('CREATE DATABASE test_taskmanagement')
    
    cur.close()
    conn.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up test database once for the entire test session."""
    wait_for_db()
    create_test_db()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_test_tables():
    """Set up fresh tables for each test."""
    # Clear all tables
    db = SessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f'TRUNCATE TABLE {table.name} CASCADE'))
        db.commit()
    finally:
        db.close()
    yield

@pytest.fixture
def client():
    """Test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_task(client):
    """Test creating a new task."""
    response = client.post('/api/tasks', json={'title': 'Test Task'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test Task'
    assert response.json['status'] == TaskStatus.TODO.value

def test_get_tasks(client):
    """Test getting all tasks."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_task(client):
    """Test updating a task."""
    # First create a task
    create_response = client.post('/api/tasks', json={'title': 'Test Task'})
    task_id = create_response.json['id']
    
    # Then update it
    update_response = client.put(f'/api/tasks/{task_id}', 
                               json={'title': 'Updated Task', 'status': TaskStatus.DONE.value})
    assert update_response.status_code == 200
    assert update_response.json['title'] == 'Updated Task'
    assert update_response.json['status'] == TaskStatus.DONE.value
