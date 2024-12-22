# Task Management API

A cloud-native task management API built with Python Flask, containerized with Docker, and deployed on Kubernetes. This project demonstrates the implementation of a RESTful CRUD API with CI/CD pipeline using GitHub Actions.

## Features

- RESTful API endpoints for task management (Create, Read, Update, Delete)
- Containerized application using Docker
- CI/CD pipeline with GitHub Actions
- Kubernetes deployment ready
- Comprehensive test suite

## Technical Stack

- **Backend**: Python Flask
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Container Registry**: GitHub Container Registry (ghcr.io)
- **Orchestration**: Kubernetes
- **Testing**: pytest

## API Endpoints

- `POST /tasks`: Create a new task
- `GET /tasks`: List all tasks
- `GET /tasks/<id>`: Get a specific task
- `PUT /tasks/<id>`: Update a task
- `DELETE /tasks/<id>`: Delete a task

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Running Tests

```bash
pytest
```

## Docker Build

```bash
docker build -t taskmanagement .
docker run -p 5000:5000 taskmanagement
```

## Deployment

The application is automatically built and deployed using GitHub Actions when changes are pushed to the main branch. The pipeline:
1. Runs tests
2. Builds Docker image
3. Pushes to GitHub Container Registry
4. Can be configured to deploy to Kubernetes cluster
