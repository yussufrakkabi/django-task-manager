# Django Task Manager

A task management web application and REST API built with **Python, Django, and Django REST Framework**.

The project allows users to register or log in, manage their own tasks, and interact with task data through both a web interface and REST API.

It demonstrates backend development skills including authentication, CRUD operations, database relationships, API development, filtering, pagination, and automated security testing.

## Features

### Web Application
- User authentication
- Create, view, update, and delete tasks
- User-specific task management
- Django Class-Based Views
- Django forms and validation
- Success messages for task operations

### REST API
- RESTful CRUD operations
- Django REST Framework APIViews and ModelViewSet
- Authenticated API access
- Task ownership protection
- Filtering tasks by completion status
- Searching tasks by title and description
- Pagination
- Interactive Swagger API documentation

### Testing
- 11 automated Django tests
- API authentication and ownership checks
- Tests preventing users from accessing, updating, or deleting another user's tasks
- Tests verifying that new tasks belong to the authenticated user

## Technologies

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| REST API | Django REST Framework |
| Database | SQLite |
| API Documentation | drf-spectacular / Swagger |
| Filtering | django-filter |
| Frontend | HTML |
| Version Control | Git and GitHub |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yussufrakkabi/django-task-manager.git
cd django-task-manager
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/tasks/

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks/api/tasks/` | List the authenticated user's tasks |
| POST | `/tasks/api/tasks/` | Create a task |
| GET | `/tasks/api/tasks/<id>/` | Retrieve a task |
| PUT | `/tasks/api/tasks/<id>/` | Update a task |
| PATCH | `/tasks/api/tasks/<id>/` | Partially update a task |
| DELETE | `/tasks/api/tasks/<id>/` | Delete a task |
| GET | `/tasks/api/viewset/tasks/` | List tasks with filtering, search, and pagination |
| POST | `/tasks/api/viewset/tasks/` | Create a task |

The ViewSet also supports retrieve, update, partial update, and delete operations at `/tasks/api/viewset/tasks/<id>/`.

### Filtering

```text
/tasks/api/viewset/tasks/?completed=true
```

### Search

```text
/tasks/api/viewset/tasks/?search=Django
```

### Pagination

```text
/tasks/api/viewset/tasks/?page=2
```

## API Documentation

Interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/tasks/api/docs/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/tasks/api/schema/
```

## Security

- API endpoints require authentication.
- Users can access only tasks they own.
- Task ownership is assigned automatically when creating a task.
- Requests to retrieve, update, or delete another user's task return HTTP 404.

## Running Tests

Run the automated test suite:

```bash
python manage.py test tasks
```

Current test results:

```text
Ran 11 tests

OK
```

## Future Improvements

- PostgreSQL integration
- Docker support
- Deployment to a hosting platform
- Improved frontend design
- Additional automated tests

## Author

GitHub: [yussufrakkabi](https://github.com/yussufrakkabi)

## Project Status

Active development — a learning and portfolio project focused on Python backend development.