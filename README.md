# ADAPTY InBody Intelligence System

FastAPI backend and Streamlit dashboard for managing synthetic clients, InBody-style body composition assessments, goals, plans, and progress reports.

## Problem

Coaches and physiotherapists often collect body composition data but do not have a clean system to track progress, explain results, and generate consistent reports.

## Solution

This MVP provides a local API and dashboard to register clients, store assessments, calculate progress, and generate simple coach/client reports. It is built as an educational health-tech portfolio project and uses synthetic data only.

## Features

- Client CRUD
- InBody-style assessment CRUD
- Goals and plans
- Progress summaries
- Coach and client reports
- Synthetic seed data
- Streamlit dashboard
- Pytest and Coverage
- GitHub Actions test workflow

## Tech Stack

Python, FastAPI, SQLModel, SQLite, Pydantic validation, Pytest, Coverage, Streamlit, Pandas.

## Project Structure

```text
app/
  core/          Application settings
  db/            SQLite session and synthetic seed data
  models/        SQLModel table models
  routers/       FastAPI endpoints
  schemas/       Request and response schemas
  services/      Pure Python progress and report logic
dashboard/       Streamlit dashboard
docs/            Architecture, API examples, roadmap
tests/           Unit and API integration tests
```

## How to Run

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Seed synthetic demo data:

```bash
python -m app.db.seed
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Run the dashboard from the project root:

```bash
streamlit run dashboard/streamlit_app.py
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
coverage run -m pytest
coverage report
```

## API Highlights

- `POST /clients`
- `GET /clients`
- `GET /clients/{client_id}`
- `PATCH /clients/{client_id}`
- `DELETE /clients/{client_id}`
- `POST /clients/{client_id}/inbody-records`
- `GET /clients/{client_id}/inbody-records`
- `GET /inbody-records`
- `GET /inbody-records/{record_id}`
- `PATCH /inbody-records/{record_id}`
- `DELETE /inbody-records/{record_id}`
- `POST /clients/{client_id}/goals`
- `GET /clients/{client_id}/goals`
- `PATCH /goals/{goal_id}`
- `DELETE /goals/{goal_id}`
- `POST /clients/{client_id}/plans`
- `GET /clients/{client_id}/plans`
- `PATCH /plans/{plan_id}`
- `DELETE /plans/{plan_id}`
- `GET /clients/{client_id}/summary`
- `GET /clients/{client_id}/coach-report`
- `GET /clients/{client_id}/client-report`

## Progress Logic

The MVP compares the first and latest assessment for:

- Weight change
- Body fat percentage-point change
- Skeletal muscle mass change
- Simple goal-specific classification

If a client has fewer than two records, the API returns a clear `not_enough_data` trend.

## Disclaimer

This project is for educational and portfolio purposes. It does not provide medical diagnosis and does not replace professional clinical judgment. Use synthetic data only.

## Roadmap

- Benchmark engine by age group, gender, and goal
- AI coach assistant
- Nutrition guidance engine
- Prediction models with synthetic longitudinal data
- InBody data import tooling
- Authentication and role-based access
- Cloud deployment
