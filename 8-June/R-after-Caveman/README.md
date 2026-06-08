# College Registration Management System

A complete Flask and SQLite web application for managing students, courses, and course registrations through a responsive Bootstrap 5 interface and JSON REST APIs.

## Features

- Admin login with session-based authentication
- Dashboard with totals and recent registrations
- Student CRUD with search by name or enrollment number
- Course CRUD with registration counts
- Multi-course student registration with duplicate prevention
- Server-side and client-side validation
- REST APIs with JSON responses
- SQLite schema and seeded sample data
- MVC-like project layout for maintainability

## Project Structure

```text
R-after-Caveman/
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- db.py
|   |-- controllers/
|   |   |-- api_controller.py
|   |   |-- auth_controller.py
|   |   |-- course_controller.py
|   |   |-- dashboard_controller.py
|   |   |-- error_controller.py
|   |   `-- registration_controller.py
|   |-- models/
|   |   |-- auth_model.py
|   |   |-- course_model.py
|   |   |-- dashboard_model.py
|   |   |-- registration_model.py
|   |   `-- student_model.py
|   |-- static/
|   |   |-- css/styles.css
|   |   `-- js/main.js
|   |-- templates/
|   |   |-- auth/login.html
|   |   |-- courses/
|   |   |-- dashboard/
|   |   |-- errors/
|   |   |-- registrations/
|   |   |-- students/
|   |   `-- base.html
|   `-- utils/
|       |-- decorators.py
|       `-- validators.py
|-- data/
|-- requirements.txt
|-- run.py
|-- sample_data.sql
`-- schema.sql
```

## MVC-Like Module Design

- `app/__init__.py`: app factory, blueprint registration, and database bootstrap
- `app/config.py`: central configuration for secret key and SQLite database path
- `app/db.py`: connection lifecycle, query helpers, and first-run schema seeding
- `app/controllers/`: route handlers for HTML pages and REST APIs
- `app/models/`: SQL-backed data access for students, courses, registrations, auth, and dashboard metrics
- `app/utils/validators.py`: form and API validation rules plus friendly constraint errors
- `app/utils/decorators.py`: login protection for HTML and API routes
- `app/templates/`: Bootstrap 5 views for dashboard, forms, tables, and error pages
- `app/static/`: custom styling and JavaScript validation helpers

## Database Schema

### 1. `students`

- `id` primary key
- `full_name`
- `enrollment_number` unique
- `email` unique
- `phone`
- `department`
- `year_level`
- `created_at`
- `updated_at`

### 2. `courses`

- `id` primary key
- `course_code` unique
- `course_name`
- `department`
- `credit_hours`
- `semester`
- `created_at`
- `updated_at`

### 3. `registrations`

- `id` primary key
- `student_id` foreign key to `students.id`
- `course_id` foreign key to `courses.id`
- unique constraint on `(student_id, course_id)` prevents duplicate registrations
- cascade delete ensures clean cleanup when a student or course is removed

### 4. `admins`

- `id` primary key
- `username` unique
- `password_hash`
- `created_at`

## Sample Data

Seed data is loaded automatically on first run:

- 1 admin user
- 5 sample students
- 5 sample courses
- 6 sample registrations

Default admin credentials:

- Username: `admin`
- Password: `admin123`

## Installation

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the application:

   ```powershell
   python run.py
   ```

4. Open the local URL shown by Flask, usually:

   ```text
   http://127.0.0.1:5000
   ```

## Database Initialization

- On first launch, `app/db.py` creates `data/college_registration.db`
- `schema.sql` builds tables, indexes, and update triggers
- `sample_data.sql` loads starter records

## REST API Endpoints

All API endpoints return JSON. Authentication uses the same admin session as the web app.

### Authentication

- `POST /api/login`
- `POST /api/logout`

### Dashboard

- `GET /api/dashboard`

### Students

- `GET /api/students`
- `GET /api/students/<id>`
- `POST /api/students`
- `PUT /api/students/<id>`
- `DELETE /api/students/<id>`

### Courses

- `GET /api/courses`
- `GET /api/courses/<id>`
- `POST /api/courses`
- `PUT /api/courses/<id>`
- `DELETE /api/courses/<id>`

### Registrations

- `GET /api/registrations`
- `GET /api/registrations/<id>`
- `POST /api/registrations`
- `DELETE /api/registrations/<id>`

### Lookup Data

- `GET /api/lookup`

## Example API Payloads

### Create Student

```json
{
  "full_name": "Nina Joseph",
  "enrollment_number": "ENR2026010",
  "email": "nina.joseph@campus.edu",
  "phone": "9876543220",
  "department": "Physics",
  "year_level": 2
}
```

### Create Course

```json
{
  "course_code": "PHY210",
  "course_name": "Thermodynamics",
  "department": "Physics",
  "credit_hours": 4,
  "semester": "Fall"
}
```

### Register Courses

```json
{
  "student_id": 1,
  "course_ids": [2, 4]
}
```

## Validation and Error Handling

- HTML forms use Bootstrap validation classes and browser constraints
- JavaScript validates checkbox-based course selection before submit
- Server-side validation protects all form and API writes
- Integrity errors return friendly duplicate or conflict messages
- Custom 404 and 500 handlers serve HTML pages or JSON based on route type

## Run Notes

- The application uses built-in SQLite and does not require a separate database server
- Deleting a student or course also deletes related registrations
- Duplicate registrations are prevented by validation and a database unique constraint
