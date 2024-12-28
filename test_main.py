import pytest
from main import app
import test_config
from models import Base, engine, SessionLocal, TaskStatus
from sqlalchemy import text
import time
import asyncpg
import urllib.parse
import os

def wait_for_db(max_retries=5, retry_interval=2):
    """Wait for the database to be ready."""
    retries = 0
    while retries < max_retries:
        try:
            # Try to connect directly with asyncpg
            url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/taskmanagement')
            parsed = urllib.parse.urlparse(url)
            user = parsed.username
            password = parsed.password
            host = parsed.hostname
            dbname = parsed.path[1:]  # Remove leading '/'
            conn = asyncpg.connect(
                user=user,
                password=password,
                host=host,
                database='postgres'  # Connect to default db first
            )
            conn.close()
            return True
        except asyncpg.OperationalError:
            retries += 1
            if retries == max_retries:
                raise
            time.sleep(retry_interval)
    return False

async def create_test_db():
    """Create test database if it doesn't exist."""
    url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/taskmanagement')
    parsed = urllib.parse.urlparse(url)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    dbname = parsed.path[1:]  # Remove leading '/'

    conn = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        database='postgres'  # Connect to default db to create test db
    )
    # Check if database exists
    exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = 'test_taskmanagement'")
    if not exists:
        await conn.execute('CREATE DATABASE test_taskmanagement')
    await conn.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Set up test database once for the entire test session."""
    await wait_for_db()
    await create_test_db()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
async def setup_test_tables():
    """Set up fresh tables for each test."""
    # Clear all tables
    db = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(text(f'TRUNCATE TABLE {table.name} CASCADE'))
    db.commit()
    db.close()
    yield

@pytest.fixture
def client():
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
