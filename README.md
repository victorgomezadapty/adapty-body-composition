# ADAPTY Body Composition Intelligence

![Tests](https://github.com/victorgomezadapty/adapty-body-composition/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**FastAPI backend + Streamlit dashboard for body composition tracking, coaching progress classification, and clinician-grade reporting.**

A portfolio-grade MVP for coaches, physiotherapists, and sports scientists working with bioelectrical impedance analysis (BIA) data.

---

## Why this exists (from a physiotherapist's perspective)

Most body composition tools stop at raw numbers. As a physiotherapist tracking clients across gym floors and clinical settings — and as someone building AI tools for clinical decision support — I found the same gap everywhere: coaches capture assessments but have no clean way to answer the two questions that actually matter:

> **"Compared to what?"** (baseline) and **"Toward what?"** (goal)

Off-the-shelf tools give you a PDF. What clinicians and coaches need is a system that: stores longitudinal assessments, computes deltas, classifies progress against a *specific goal* (fat loss vs. muscle gain vs. recomposition each have different success criteria), and generates coach-facing and client-facing reports in seconds.

That's what this project is. The classification logic reflects how I actually assess progress in practice — not generic CRUD.

---

## Features

- **Client management** — CRUD lifecycle
- **BIA assessment tracking** — 8 body composition metrics per record
- **Goals + plans** — attach goal type (fat_loss / muscle_gain / recomposition) per client
- **Progress classification** — first-vs-latest analysis with goal-aware rules
- **Dual reporting** — coach-facing (technical) and client-facing (plain language)
- **Synthetic seed data** — realistic demo dataset for exploration
- **Streamlit dashboard** — visual companion to the API
- **Test coverage** — pytest + coverage with CI/CD on every push

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI (async, lifespan context) |
| ORM | SQLModel + SQLite (portable, zero-config) |
| Validation | Pydantic v2 |
| Testing | Pytest + Coverage (branch coverage enabled) |
| Dashboard | Streamlit + Pandas |
| CI/CD | GitHub Actions (Python 3.11 matrix) |

---

## Project structure

```
app/
  core/          Application settings
  db/            SQLite session and synthetic seed data
  exceptions/    Domain-specific error types
  models/        SQLModel table models
  routers/       FastAPI endpoints
  schemas/       Request and response DTOs
  services/      Progress logic, report generation, nutrition heuristics
dashboard/       Streamlit dashboard
docs/            Architecture, API examples, roadmap
tests/           Unit and integration tests
```

---

## Getting started

Requires **Python 3.11+**.

```bash
# 1. Clone
git clone https://github.com/victorgomezadapty/adapty-body-composition.git
cd adapty-body-composition

# 2. Virtual environment
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed synthetic demo data
python -m app.db.seed

# 5. Run the API
uvicorn app.main:app --reload
```

Then open:

- **Swagger docs:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Run the dashboard:

```bash
streamlit run dashboard/streamlit_app.py
```

Run tests:

```bash
pytest
coverage run -m pytest && coverage report
```

---

## API surface

Client lifecycle:

- `POST /clients` · `GET /clients` · `GET /clients/{id}` · `PATCH /clients/{id}` · `DELETE /clients/{id}`

Body composition records:

- `POST /clients/{client_id}/body-records`
- `GET /clients/{client_id}/body-records`
- `GET /body-records` · `GET /body-records/{id}` · `PATCH /body-records/{id}` · `DELETE /body-records/{id}`

Goals + plans:

- `POST /clients/{client_id}/goals` · `PATCH /goals/{id}` · `DELETE /goals/{id}`
- `POST /clients/{client_id}/plans` · `PATCH /plans/{id}` · `DELETE /plans/{id}`

Reports:

- `GET /clients/{client_id}/summary` — computed progress snapshot
- `GET /clients/{client_id}/coach-report` — technical detail for the coach
- `GET /clients/{client_id}/client-report` — plain-language version for the client

---

## Progress classification

The MVP compares the first and latest assessment for:

- Weight change (kg)
- Body fat percentage-point change
- Skeletal muscle mass change (kg)
- Goal-specific classification (`positive` / `mixed` / `needs_attention` / `stable`)

If a client has fewer than two records, the API returns a clear `not_enough_data` trend so the UI can prompt for a follow-up assessment.

The classification thresholds are *educational coaching rules* informed by ACSM position stands on concurrent training and body recomposition. They are not diagnostic and should be adapted to individual context.

---

## Roadmap

- [ ] **Benchmarks** — percentiles and z-scores by age group, sex, and goal
- [ ] **Predictive models** — recomposition trajectory with confidence intervals
- [ ] **Nutrition guidance engine** — heuristic macro/calorie recommendations from goal + measurements
- [ ] **AI coach assistant** — natural-language explanations of progress deltas
- [ ] **BIA data import** — CSV/JSON parsers for common BIA formats
- [ ] **Auth + roles** — coach / physio / admin permissions
- [ ] **Cloud deployment** — Streamlit Cloud demo + Railway/Fly API

---

## Disclaimer

This project is for **educational and portfolio purposes** and operates exclusively on **synthetic data**. It does not provide medical diagnosis and does not replace professional clinical judgment. Do not use with real patient data without adding proper authentication, audit logging, and applicable healthcare compliance (HIPAA / GDPR / local regulations).

*"InBody"* and other BIA brand names, where they appear in documentation, refer to the general category of bioelectrical impedance analysis. This project is **not affiliated with or endorsed by InBody Co., Ltd. or any BIA device manufacturer**.

---

## Author

Built by **Víctor Andrés Gómez López** — physiotherapist, doctoral researcher in physical activity and sport, founder of [ADAPTY](https://adapty.global). Currently Head Physiotherapist at Optimo Gym (Riyadh) and building clinical AI tools full time.

- LinkedIn: [linkedin.com/in/victorgomezadapty](https://linkedin.com/in/victorgomezadapty)
- Other projects: [physioflow](https://github.com/victorgomezadapty/physioflow) · [ADAPTY](https://adapty.global)

---

## License

MIT — see [LICENSE](./LICENSE).
