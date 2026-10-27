
# Django Task Manager

A task management web application and REST API built with Django and Django REST Framework.

## Features

- User authentication
- Create, read, update, and delete tasks
- User-specific task management
- REST API endpoints
- Search, filtering, and pagination
- Swagger/OpenAPI documentation
- PostgreSQL database support
- Docker containerization
- Automated Django tests

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (Neon)
- Docker and Docker Compose
- Gunicorn
- WhiteNoise
- Git and GitHub

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks/api/viewset/tasks/ | List tasks |
| POST | /tasks/api/viewset/tasks/ | Create task |
| GET | /tasks/api/viewset/tasks/{id}/ | Retrieve task |
| PUT | /tasks/api/viewset/tasks/{id}/ | Update task |
| DELETE | /tasks/api/viewset/tasks/{id}/ | Delete task |
| GET | /tasks/api/docs/ | Swagger documentation |

## Run Locally with Docker

1. Clone the repository.
2. Create a `.env` file containing the required environment variables.
3. Start the application:

```bash
docker compose up -d --build
```

4. Apply database migrations:

```bash
docker compose exec web python manage.py migrate
```

5. Open http://127.0.0.1:8000/tasks/

## Run Tests

```bash
docker compose exec web python manage.py test tasks
```

## Security

- Environment variables for secrets
- Authentication and task ownership permissions
- Non-root Docker user
- Production security configuration

## Project Status

Backend development completed.
Public deployment is planned.
