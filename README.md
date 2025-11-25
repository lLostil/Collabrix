Collabrix is a lightweight knowledge management API built with FastAPI, SQLAlchemy, and Alembic. The current setup exposes basic workspace ("space") management endpoints and is ready to expand with additional content types like pages and comments.

## Getting started

1. **Create a virtual environment** (Python 3.11+ recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -e .
   ```

3. **Configure the database**: set `DATABASE_URL` in your environment or `.env` file. The default expects PostgreSQL at `postgresql+psycopg2://collabrix:collabrix@localhost:5432/collabrix`.

4. **Run migrations**:

   ```bash
   alembic upgrade head
   ```

5. **Start the API**:

   ```bash
   uvicorn app.main:app --reload
   ```

Visit `http://localhost:8000/docs` to explore the interactive OpenAPI docs.

## Available endpoints

- `GET /health` — health check
- `GET /api/v1/spaces` — list spaces
- `POST /api/v1/spaces` — create a space
- `GET /api/v1/spaces/{space_id}` — fetch a specific space
- `PUT /api/v1/spaces/{space_id}` — update a space
- `DELETE /api/v1/spaces/{space_id}` — delete a space

## Project structure

- `app/core` — configuration
- `app/db` — database setup and session management
- `app/models` — SQLAlchemy models
- `app/schemas` — Pydantic schemas for request/response validation
- `app/repositories` — data access layer
- `app/services` — business logic
- `app/api` — FastAPI routers
- `alembic` — migrations
Collabrix is a FastAPI-based knowledge management backend inspired by Confluence. It ships with user authentication (JWT),
space/page hierarchies, versioned content, comments (including inline), file attachment metadata, and RBAC primitives.

## Backend layout

```
app/
  main.py                  # FastAPI application factory
  api/
    main.py                # Router aggregator
    deps.py                # Shared dependencies (DB, auth)
    routes/
      auth.py              # Registration & login
      health.py            # Health check
      pages.py             # Page CRUD endpoints
      spaces.py            # Space CRUD endpoints
  core/
    config.py              # Settings via environment variables
    security.py            # Password hashing & JWT helpers
  db/
    base.py                # Declarative base
    session.py             # Engine and session factory
  models/                  # SQLAlchemy models (users, spaces, pages, comments, attachments)
  repositories/            # Data access layer
  schemas/                 # Pydantic schemas
  services/                # Business logic services
alembic/
  env.py                   # Migration runner configuration
  versions/                # Generated migration files
pyproject.toml             # Dependencies and metadata
```

## Configuration

Set these environment variables (or place them in a `.env` file) before running the API or migrations:

- `DATABASE_URL` — PostgreSQL URL (e.g., `postgresql+psycopg2://user:pass@localhost:5432/collabrix`)
- `SECRET_KEY` — secret used to sign JWTs
- `JWT_ALGORITHM` — defaults to `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — defaults to 1440 (24 hours)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Database setup

Run migrations after configuring your environment:

```bash
alembic upgrade head
```

## Running the API

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API docs.

## Initial endpoints

- `GET /health` — health check
- `POST /auth/register` — register a user and receive a JWT
- `POST /auth/login` — authenticate and receive a JWT
- `GET /api/v1/spaces` — list spaces
- `POST /api/v1/spaces` — create a space (requires auth)
- `GET /api/v1/spaces/{space_id}` — retrieve a space
- `PUT /api/v1/spaces/{space_id}` — update a space (requires role)
- `DELETE /api/v1/spaces/{space_id}` — delete a space (requires admin role)
- `GET /api/v1/pages/spaces/{space_id}` — list pages in a space
- `POST /api/v1/pages` — create a page (requires auth)
- `GET /api/v1/pages/{page_id}` — retrieve a page
- `PUT /api/v1/pages/{page_id}` — update a page (requires edit permission)
- `DELETE /api/v1/pages/{page_id}` — delete a page (requires edit permission)

## Notes

- Passwords are hashed with bcrypt.
- JWT access tokens default to 24-hour expiration; adjust via environment variables.
- Alembic is preconfigured to read `DATABASE_URL` directly from the app settings so migrations and the API share configuration.s