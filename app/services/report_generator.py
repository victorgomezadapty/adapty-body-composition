"""Generate simple coach and client reports from progress summaries."""

from dataclasses import asdict

from app.services.coach_message_generator import (
    generate_client_message,
    generate_coach_message,
)
from app.services.progress_analyzer import ProgressSummary


def generate_client_report(summary: ProgressSummary) -> dict[str, object]:
    """Generate a client-facing report payload."""
    return {
        "audience": "client",
        "summary": asdict(summary),
        "message": generate_client_message(summary),
        "disclaimer": (
            "This educational summary does not provide medical diagnosis or "
            "replace professional clinical judgment."
        ),
    }


def generate_coach_report(summary: ProgressSummary) -> dict[str, object]:
    """Generate a coach-facing report payload."""
    return {
        "audience": "coach",
        "summary": asdict(summary),
        "message": generate_coach_message(summary),
        "next_step": "Review consistency, training load, nutrition, and reassessment timing.",
    }

