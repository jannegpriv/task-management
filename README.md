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

## Related Repositories

- [task-management-ui](https://github.com/jannegpriv/task-management-ui) - Frontend React application
- [task-management-k8s](https://github.com/jannegpriv/task-management-k8s) - Kubernetes manifests

## Architecture Diagrams

### Application Data Flow
```mermaid
graph TD
    A[Client] -->|HTTP Requests| B[Flask API]
    B -->|SQLAlchemy ORM| C[PostgreSQL Database]
    
    subgraph Flask Application
        B -->|Create| D[Task Routes]
        B -->|Read| D
        B -->|Update| D
        B -->|Delete| D
        B -->|Settings| E[Settings Routes]
        D -->|Models| F[Task Model]
        E -->|Models| G[Settings Model]
    end
    
    subgraph Database
        F -->|Store| C
        G -->|Store| C
    end
```

## Deployment

This service is deployed using GitHub Actions and Kubernetes:

### CI/CD Pipeline

```mermaid
flowchart TD
    subgraph Triggers
        A[Push to main branch] --> D[Pipeline Start]
        B[Push tag v*.*.*] --> D
        C[Pull Request to main] --> D
    end

    subgraph test[Test Job]
        D --> E[Setup PostgreSQL Service]
        E --> F[Setup Python 3.9]
        F --> G[Install Dependencies]
        G --> H[Wait for PostgreSQL]
        H --> I[Run Tests]
    end

    subgraph build[Build and Push Job]
        I -->|Success| J{Check Conditions}
        J -->|Tag or Main Branch| K[Login to Registry]
        K --> L[Get Version]
        L --> M[Build & Push Image]
    end

    subgraph tags[Image Tags]
        M --> N[Latest Tag]
        M --> O[Version Tag]
        M --> P[SHA Tag]
    end

    style test fill:#f0f7ff,stroke:#4788c7
    style build fill:#f1fff0,stroke:#47c747
    style Triggers fill:#fff0f0,stroke:#c74747
    style tags fill:#f7f0ff,stroke:#8347c7
```

The pipeline is triggered by:
- Push to main branch
- Push of version tags (v*.*.*)
- Pull requests to main branch

The pipeline consists of two main jobs:
1. **Test Job**: Sets up PostgreSQL, runs the test suite
2. **Build and Push Job**: Builds and pushes Docker image if tests pass and trigger is either main branch or version tag

Images are tagged with:
- Latest: Always updated for main branch and version tags
- Version: Applied when pushing version tags (e.g., v1.0.0)
- SHA: Short commit hash for main branch pushes

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
