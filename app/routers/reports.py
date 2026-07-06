"""Progress summary and report endpoints."""

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.inbody_record import InBodyRecord
from app.routers.helpers import get_client_or_404
from app.schemas.report_schema import ClientProgressSummaryRead, ReportRead
from app.services.coach_message_generator import (
    generate_client_message,
    generate_coach_message,
)
from app.services.progress_analyzer import ProgressSummary, build_progress_summary
from app.services.report_generator import generate_client_report, generate_coach_report

router = APIRouter(tags=["reports"])


def _get_client_records(session: Session, client_id: int) -> list[InBodyRecord]:
    """Return chronological records for a client."""
    return list(
        session.exec(
            select(InBodyRecord)
            .where(InBodyRecord.client_id == client_id)
            .order_by(InBodyRecord.measurement_date)
        ).all()
    )


def _summary_payload(summary: ProgressSummary) -> dict[str, Any]:
    """Convert a progress summary dataclass to an API-friendly dictionary."""
    return asdict(summary)


@router.get("/clients/{client_id}/summary", response_model=ClientProgressSummaryRead)
def get_client_summary(
    client_id: int,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    """Generate a progress summary for one client."""
    client = get_client_or_404(session, client_id)
    records = _get_client_records(session, client_id)
    summary = build_progress_summary(records=records, goal_type=client.main_goal)
    latest_date = records[-1].measurement_date.isoformat() if records else None

    return {
        "client_id": client.id,
        "client_name": f"{client.first_name} {client.last_name}",
        "main_goal": client.main_goal,
        "records_count": len(records),
        "latest_measurement_date": latest_date,
        "summary": _summary_payload(summary),
        "message": generate_client_message(summary),
    }


@router.get("/clients/{client_id}/coach-report", response_model=ReportRead)
def get_coach_report(
    client_id: int,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    """Generate a coach-facing report for one client."""
    client = get_client_or_404(session, client_id)
    records = _get_client_records(session, client_id)
    summary = build_progress_summary(records=records, goal_type=client.main_goal)
    report = generate_coach_report(summary)

    return {
        "audience": report["audience"],
        "client_id": client.id,
        "client_name": f"{client.first_name} {client.last_name}",
        "main_goal": client.main_goal,
        "records_count": len(records),
        "message": generate_coach_message(summary),
        "summary": report["summary"],
        "next_step": report["next_step"],
    }


@router.get("/clients/{client_id}/client-report", response_model=ReportRead)
def get_client_report(
    client_id: int,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    """Generate a client-facing report for one client."""
    client = get_client_or_404(session, client_id)
    records = _get_client_records(session, client_id)
    summary = build_progress_summary(records=records, goal_type=client.main_goal)
    report = generate_client_report(summary)

    return {
        "audience": report["audience"],
        "client_id": client.id,
        "client_name": f"{client.first_name} {client.last_name}",
        "main_goal": client.main_goal,
        "records_count": len(records),
        "message": generate_client_message(summary),
        "summary": report["summary"],
        "disclaimer": report["disclaimer"],
    }
