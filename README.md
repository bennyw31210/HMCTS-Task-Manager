# HMCTS Task Manager

## Overview

**HMCTS Task Manager** is a simple task management web  application designed to assist caseworkers in
keeping track of their tasks and effectively managing their workloads. The site utilises **FastAI (Python)** for the backend and a **HTML/CSS/JavaScript** frontend. It allows users to create, view, update and delete tasks via a simple interface through a RESTful API.

---

## Features

- REST API for task management (CRUD operations)
- Interactive frontend web app
- PostgreSQL database integration
- Logging system
- Docker deployment support

---

## Functionality

- Create a task with the following properties:
  - Title
  - Description (optional)
  - Status
  - Due date/time
- Retrieve tasks
- Update the status of a task
- Delete a task

---

## Project Structure

### Backend (Located inside `src/`)

- **`main.py`** - The entry point of the FastAPI application. It sets up the API routes and middleware, and houses the application's core settings and configurations including database session initialisation and clean-up functions.

- **`routers/`** - Contains FastAPI routes defining the API endpoints for the task management operations.

- **`db/`** - Manages database models and database connection sessions using SQLAlchemy. Contains the Create, Read, Update, Delete (CRUD) operations code.

- **`models/`** - Contains pydantic models for data validation and serialisation/deserialisation between the API and database.

- **`tests/`** - Contains unit tests to test the functionality of the application's API endpoints in isolation (an in-memory mock SQLite database was used in place of the PostgreSQL database used in production).

- **`utils/`** - Contains code that is shared across multiple components of the backend.

- **`logger.py`** - Configures the application's logging for consistent and structured log output, aiding debugging and monitoring.

#### API Endpoints

| Name           | Method   | Description                                                    |
|:--------------:|:--------:|:---------------------------------------------------------------|
| `/tasks/`      | `POST`   | Create a new task.                                             |
| `/tasks/`      | `GET`    | Retrieve all tasks.                                            |
| `/tasks/{ID}/` | `GET`    | Retrieve a single task by its ID.                              |
| `/tasks/{ID}/` | `PATCH`  | Update a task's status.                                        |
| `/tasks/{ID}/` | `DELETE` | Delete a task.                                                 |
| `/`            | `GET`    | Root endpoint. Retrieve the app's frontend.                    |
| `/docs/`       | `GET`    | Retrieve the **OpenAPI (Swagger)** documentation for this API. |

### Frontend (Located inside `src/static/`)

Contains JavaScript, CSS and HTML to provide an intuitive UI for interactions with the API.

---

## Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (if using containerisation)
- Pipenv (recommended for managing Python packages)

---

### Clone the Repository

```bash
git clone https://github.com/bennyw31210/HMCTS-Task-Manager.git
cd HMCTS-Task-Manager
```

### Run Locally without Docker

```bash
pip install pipenv
pipenv install
```

Setup a **PostgreSQL** database and run the SQL below to create a table named **Tasks**. 

```SQL
-- Create statusType enum if it doesn't exist
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statustypes') THEN
        CREATE TYPE statustypes AS ENUM ('PENDING', 'IN_PROGRESS', 'DONE');
    END IF;
END $$;

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS "Tasks" (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status statustypes NOT NULL DEFAULT 'PENDING',
    due_date TIMESTAMPTZ NOT NULL
);
```

Update the environment variables in the ***`.env`*** file if and where appropriate, then run the following command in the **`src/`** directory to start the app.

```bash
uvicorn main:app --reload
```

By default, the app will be available at [http://localhost:8000/](http://localhost:8000/).

### Run Using Docker (Recommended)

Run the following command in the root directory:

```bash
docker compose up --build
```

This will:
- Build the docker images
- Start the FastAPI app
- Expose the application on [http://localhost:8001/](http://localhost:8001/)