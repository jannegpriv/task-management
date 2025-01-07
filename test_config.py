import os

# Test database URL - handle both local and CI environments
DB_HOST = "postgres" if os.getenv("CI") else "localhost"
DB_NAME = "test_taskmanagement"
TEST_DATABASE_URL = os.getenv('DATABASE_URL', f'postgresql://postgres:postgres@{DB_HOST}:5432/{DB_NAME}')

# Override the database URL for tests
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
