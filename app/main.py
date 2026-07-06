"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.database import init_db
from app.routers import clients, goals, inbody_records, plans, reports


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize local database tables when the API starts."""
    init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    description=(
        "Educational MVP for tracking synthetic InBody-style body composition "
        "records and generating coaching support summaries."
    ),
)

app.include_router(clients.router)
app.include_router(inbody_records.router)
app.include_router(goals.router)
app.include_router(plans.router)
app.include_router(reports.router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a welcome message for the API."""
    return {
        "message": "Welcome to the ADAPTY InBody Intelligence System API.",
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health check response."""
    return {"status": "ok", "service": settings.app_name}
