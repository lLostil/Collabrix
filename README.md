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