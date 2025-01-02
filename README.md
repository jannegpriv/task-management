# Task Management Backend

A Flask-based REST API for managing tasks. This service provides the backend functionality for the Task Management application.

## Architecture

- **Framework**: Flask
- **Database**: PostgreSQL
- **Container Registry**: GitHub Container Registry (ghcr.io)
- **CI/CD**: GitHub Actions
- **Deployment**: Kubernetes via [task-management-k8s](https://github.com/jannegpriv/task-management-k8s)

## Local Development

### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker (optional)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jannegpriv/task-management.git
cd task-management
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanagement
```

5. Run the application:
```bash
flask run
```

The API will be available at `http://localhost:5000`

### Using Docker

Build and run the application using Docker:
```bash
docker build -t task-management .
docker run -p 5000:5000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/taskmanagement task-management
```

## API Endpoints

- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

## Deployment

This service is deployed using GitHub Actions and Kubernetes:

1. Changes pushed to main trigger the CI/CD pipeline
2. The pipeline:
   - Runs tests
   - Builds a Docker image
   - Pushes to GitHub Container Registry
   - Tags with both `latest` and git version tag (if present)

### Release Process

To create a new release:

1. Tag the commit:
```bash
git tag -a v1.1.0 -m "Description of changes"
git push origin v1.1.0
```

2. GitHub Actions will automatically:
   - Build the Docker image
   - Tag it as `ghcr.io/jannegpriv/task-management:v1.1.0`
   - Push to the registry

3. Update the Kubernetes manifests in [task-management-k8s](https://github.com/jannegpriv/task-management-k8s) to use the new version.

## Related Repositories

- [task-management-ui](https://github.com/jannegpriv/task-management-ui) - Frontend React application
- [task-management-k8s](https://github.com/jannegpriv/task-management-k8s) - Kubernetes manifests
