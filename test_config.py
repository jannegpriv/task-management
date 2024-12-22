import os

# Test database configuration
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_taskmanagement"

# Override the database URL for tests
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
