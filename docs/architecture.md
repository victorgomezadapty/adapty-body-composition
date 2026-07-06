# Architecture

The MVP separates web/API concerns from pure business logic.

## Layers

- `app/main.py`: FastAPI application setup, router registration, database initialization.
- `app/db/`: SQLite engine, SQLModel sessions, and synthetic seed data.
- `app/models/`: SQLModel table models for clients, assessments, goals, and plans.
- `app/schemas/`: request and response contracts used by FastAPI.
- `app/routers/`: HTTP endpoints for CRUD and reports.
- `app/services/`: pure Python progress and report functions.
- `dashboard/`: Streamlit interface for overview metrics, profiles, charts, reports, and tables.
- `tests/`: service tests and API integration tests with in-memory SQLite.

## Data Flow

1. FastAPI receives and validates a request through a schema.
2. A router uses a SQLModel session dependency.
3. Models are created, read, updated, or deleted in SQLite.
4. Report endpoints retrieve chronological records and call pure service functions.
5. The dashboard reads from the API or falls back to synthetic demo data.

## Safety Boundaries

- No real client, patient, or member data.
- No medical diagnosis.
- No authentication or production deployment in version 0.1.
- No OpenAI, machine learning, wearables, or InBody USB integration in version 0.1.
