import os

# Test database configuration
TEST_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'postgres')}@{os.getenv('POSTGRES_HOST', 'localhost')}:5432/{os.getenv('POSTGRES_DB', 'test_taskmanagement')}"

# Override the database URL for tests
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
