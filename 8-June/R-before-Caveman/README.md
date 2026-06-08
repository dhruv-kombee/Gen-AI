# College Registration Management System

A complete Flask and SQLite web application for managing students, courses, and registrations in a college environment. The project includes an admin login, a responsive Bootstrap 5 interface, server-side and client-side validation, and REST API endpoints for CRUD operations.

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Python, Flask
- Database: SQLite
- Architecture: MVC-like structure with controllers, repositories, services, templates, and static assets

## Features

- Admin authentication with session-based access control
- Dashboard with student, course, and registration totals
- Student CRUD with search by name or enrollment number
- Course CRUD with registration counts
- Multi-course student registration with duplicate prevention
- REST-style JSON APIs for students, courses, and registrations
- Responsive college-themed interface
- Built-in SQLite schema and sample data seeding
- Error handling for HTML pages and API routes

## Project Structure

```text
R-before-Caveman/
|-- app/
|   |-- __init__.py
|   |-- db.py
|   |-- controllers/
|   |   |-- api_controller.py
|   |   |-- auth_controller.py
|   |   |-- course_controller.py
|   |   |-- dashboard_controller.py
|   |   |-- registration_controller.py
|   |   `-- student_controller.py
|   |-- repositories/
|   |   |-- course_repository.py
|   |   |-- registration_repository.py
|   |   `-- student_repository.py
|   |-- services/
|   |   `-- auth_service.py
|   |-- static/
|   |   |-- css/styles.css
|   |   `-- js/app.js
|   |-- templates/
|   |   |-- courses/
|   |   |-- errors/
|   |   |-- registrations/
|   |   |-- students/
|   |   |-- dashboard.html
|   |   |-- layout.html
|   |   `-- login.html
|   `-- utils/
|       |-- constants.py
|       |-- decorators.py
|       `-- validators.py
|-- database/
|   |-- schema.sql
|   `-- sample_data.sql
|-- .gitignore
|-- config.py
|-- README.md
|-- requirements.txt
`-- run.py
```

## MVC-Like Module Breakdown

### `run.py`

Entry point that creates the Flask application and starts the development server.

### `config.py`

Stores application configuration such as database location, admin credentials, and session settings.

### `app/__init__.py`

Builds the Flask app, initializes the database, registers blueprints, and sets up error handlers.

### `app/db.py`

Provides SQLite connection management and startup database initialization with automatic sample-data seeding when the database is empty.

### `app/controllers/`

Contains route handlers for:

- `auth_controller.py`: admin login and logout
- `dashboard_controller.py`: dashboard metrics and recent registrations
- `student_controller.py`: student HTML CRUD flows and search
- `course_controller.py`: course HTML CRUD flows
- `registration_controller.py`: student-course registration flows and delete actions
- `api_controller.py`: JSON REST endpoints for CRUD actions

### `app/repositories/`

Encapsulates database queries and keeps SQL access separated from routing logic.

- `student_repository.py`: student CRUD, counts, and uniqueness checks
- `course_repository.py`: course CRUD, counts, and lookup helpers
- `registration_repository.py`: registration CRUD, duplicate-safe inserts, and summaries

### `app/services/`

- `auth_service.py`: validates admin credentials using the configured username and password

### `app/utils/`

- `constants.py`: shared departments and year options
- `decorators.py`: `login_required` session guard
- `validators.py`: shared server-side validation for forms and API payloads

### `app/templates/`

Bootstrap 5 Jinja templates for the admin UI, CRUD pages, registration views, and error pages.

### `app/static/`

- `css/styles.css`: college-themed design system and responsive styles
- `js/app.js`: Bootstrap validation behavior, checkbox-group validation, and delete confirmations

## Database Schema

### 1. `students`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key |
| `full_name` | TEXT | Required |
| `enrollment_number` | TEXT | Required, unique |
| `email` | TEXT | Required, unique |
| `phone` | TEXT | Optional |
| `department` | TEXT | Required |
| `year` | INTEGER | Required, range 1-6 |
| `created_at` | DATETIME | Default current timestamp |
| `updated_at` | DATETIME | Default current timestamp |

### 2. `courses`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key |
| `course_code` | TEXT | Required, unique |
| `title` | TEXT | Required |
| `department` | TEXT | Required |
| `credits` | INTEGER | Required, range 1-6 |
| `capacity` | INTEGER | Required, range 1-500 |
| `created_at` | DATETIME | Default current timestamp |
| `updated_at` | DATETIME | Default current timestamp |

### 3. `registrations`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key |
| `student_id` | INTEGER | Foreign key to `students.id` |
| `course_id` | INTEGER | Foreign key to `courses.id` |
| `registered_at` | DATETIME | Default current timestamp |

Constraints:

- `UNIQUE(student_id, course_id)` prevents duplicate registrations
- Cascade delete removes related registrations when a student or course is deleted

## Authentication

- Default username: `admin`
- Default password: `admin123`

You can override these with environment variables before running:

```powershell
$env:ADMIN_USERNAME="superadmin"
$env:ADMIN_PASSWORD="change-me"
```

## Installation

### 1. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
python run.py
```

### 4. Open in your browser

Visit `http://127.0.0.1:5000`

## Database Initialization and Sample Data

- The app automatically creates `database/college_registration.db` on first run.
- `database/schema.sql` creates the tables and indexes.
- `database/sample_data.sql` seeds demo students, courses, and registrations only when the database is empty.

## Run Instructions

```powershell
python run.py
```

To stop the server, press `Ctrl + C` in the terminal.

## REST API Endpoints

All API routes require an authenticated session.

### Students

- `GET /api/students`
- `GET /api/students/<student_id>`
- `POST /api/students`
- `PUT /api/students/<student_id>`
- `DELETE /api/students/<student_id>`

### Courses

- `GET /api/courses`
- `GET /api/courses/<course_id>`
- `POST /api/courses`
- `PUT /api/courses/<course_id>`
- `DELETE /api/courses/<course_id>`

### Registrations

- `GET /api/registrations`
- `GET /api/registrations/<registration_id>`
- `POST /api/registrations`
- `PUT /api/students/<student_id>/registrations`
- `DELETE /api/registrations/<registration_id>`

### Example JSON Payloads

Create a student:

```json
{
  "full_name": "Sana Kapoor",
  "enrollment_number": "CSE2024050",
  "email": "sana.kapoor@college.edu",
  "phone": "+91 9876543200",
  "department": "Computer Science",
  "year": 1
}
```

Create a course:

```json
{
  "course_code": "CSE305",
  "title": "Machine Learning Basics",
  "department": "Computer Science",
  "credits": 4,
  "capacity": 40
}
```

Register a student in multiple courses:

```json
{
  "student_id": 1,
  "course_ids": [2, 4, 6]
}
```

## Validation Rules

- Student name must be at least 3 characters
- Enrollment number must be 4 to 20 valid characters
- Email must be valid and unique
- Phone number is optional but validated if present
- Course credits must be between 1 and 6
- Course capacity must be between 1 and 500
- At least one course must be selected when registering
- Duplicate student-course registrations are skipped and blocked by both code and database constraint

## Notes

- This project uses session authentication for the admin UI and APIs.
- The SQLite database file is ignored through `.gitignore`, while schema and sample data stay versioned.
- The design is responsive across desktop, tablet, and mobile layouts.
