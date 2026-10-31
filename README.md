# Django Task Manager

A full-stack task management application built with **Python, Django, Django REST Framework, and PostgreSQL**.

The project demonstrates backend development skills through secure REST APIs, user authentication, database integration, automated testing, and containerization. It also includes a responsive frontend built with Django templates and Bootstrap 5.

## Features

- User authentication and protected pages
- Create, read, update, and delete tasks
- Complete and reopen tasks
- Task search and status filtering
- Dashboard statistics and pagination
- User-specific task ownership and access control
- REST API with Swagger/OpenAPI documentation
- PostgreSQL database integration
- Docker containerization
- GitHub Actions continuous integration
- 20 automated Django tests

## Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Frontend | HTML, CSS, Bootstrap 5 |
| Database | PostgreSQL (Neon) |
| API Documentation | drf-spectacular, Swagger UI |
| Infrastructure | Docker, Docker Compose, Gunicorn, WhiteNoise |
| Testing | Django TestCase, DRF APITestCase |
| CI/CD | GitHub Actions |
| Version Control | Git and GitHub |

## Project Architecture

The application uses Django and Django REST Framework to provide both a web interface and a REST API.

- **Django:** authentication, web views, and business logic
- **Django REST Framework:** API endpoints, serializers, and permissions
- **PostgreSQL:** stores users and tasks
- **Docker:** containerizes the application
- **Gunicorn:** runs the Django WSGI application
- **WhiteNoise:** serves static files
- **Swagger/OpenAPI:** documents API endpoints
- **GitHub Actions:** runs automated tests on pushes and pull requests

```mermaid
flowchart TD
    A[Browser / API Client] --> B[Gunicorn + Django]
    B --> C[Django Web Views]
    B --> D[DRF REST API]
    C --> E[Django ORM]
    D --> E
    E --> F[(Neon PostgreSQL)]
    G[GitHub Actions CI] --> H[Automated Django Tests]
```

## Security

- Authentication is required for protected pages and all task API endpoints
- Users can access only their own tasks; ownership is enforced at the database-query level
- Accessing another user's task returns `404`
- Task ownership is assigned by the backend, never by the client
- CSRF protection for Django forms
- Secrets and database credentials are stored in environment variables
- Docker runs the application as a non-root user
- Automated tests cover unauthorized access

## API

Base URL (local): `http://127.0.0.1:8000`

### Authentication

The API uses Django session authentication. For local development, log in at
`http://127.0.0.1:8000/users/login/`.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks/api/tasks/` | List your tasks |
| POST | `/tasks/api/tasks/` | Create a task |
| GET | `/tasks/api/tasks/<id>/` | Retrieve a task |
| GET | `/tasks/api/viewset/tasks/` | List tasks (filtering and pagination) |
| POST | `/tasks/api/viewset/tasks/` | Create a task |
| GET | `/tasks/api/viewset/tasks/<id>/` | Retrieve a task |
| PUT / PATCH | `/tasks/api/viewset/tasks/<id>/` | Update a task |
| DELETE | `/tasks/api/viewset/tasks/<id>/` | Delete a task |
| GET | `/tasks/api/docs/` | Swagger UI documentation |

### Examples

**List tasks** — `GET /tasks/api/tasks/`

```json
[
  {
    "id": 1,
    "title": "Learn Django REST Framework",
    "description": "Practice API development",
    "completed": false,
    "owner": 1
  }
]
```

**Create a task** — `POST /tasks/api/tasks/` (returns `201 Created`)

```json
{
  "title": "Build REST API",
  "description": "Create Django API endpoints",
  "completed": false
}
```

The authenticated user is automatically assigned as the owner.

**Update a task** — `PATCH /tasks/api/viewset/tasks/1/` (returns `200 OK`)

```json
{
  "completed": true
}
```

**Delete a task** — `DELETE /tasks/api/viewset/tasks/1/` (returns `204 No Content`)

Interactive documentation: http://127.0.0.1:8000/tasks/api/docs/

## Run Locally with Docker

1. Clone the repository.
2. Create a `.env` file in the project root with the required environment variables, for example:

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

   Adjust the names to match your `settings.py`.

3. Build and start the application:

   ```bash
   docker compose up -d --build
   ```

4. Apply database migrations:

   ```bash
   docker compose exec web python manage.py migrate
   ```

5. Open http://127.0.0.1:8000/tasks/

## Automated Testing

Run the test suite:

```bash
python manage.py test tasks
```

Or inside Docker:

```bash
docker compose exec web python manage.py test tasks
```

The 20 tests cover API security, task ownership, dashboard search, status filtering, pagination, and task completion. GitHub Actions runs them automatically on pushes and pull requests.

## Application Screenshots

### Task Dashboard

![Task Dashboard](docs/screenshots/dashboard.png)

### Login Page

![Login Page](docs/screenshots/login.png)

### Create Task

![Create Task](docs/screenshots/create-task.png)

## Project Status

Backend and frontend development are complete. Public deployment is planned.