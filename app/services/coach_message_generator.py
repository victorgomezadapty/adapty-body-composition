"""Generate general, non-diagnostic coaching messages."""

from app.services.progress_analyzer import ProgressSummary


def generate_client_message(summary: ProgressSummary) -> str:
    """Create a simple client-facing progress message."""
    if not summary.trend_available:
        return (
            "A progress trend is not available yet. Add at least two assessments "
            "to compare changes over time."
        )

    if summary.classification == "positive":
        return (
            "Your latest assessment shows encouraging progress. Keep following "
            "the plan and review changes consistently over time."
        )

    if summary.classification == "needs_attention":
        return (
            "Your latest trend suggests the plan may need adjustment. Review "
            "training, nutrition, recovery, and consistency with your coach."
        )

    return (
        "Your progress is mixed or still stabilizing. Keep tracking the key "
        "metrics and use the next assessment to confirm the trend."
    )


def generate_coach_message(summary: ProgressSummary) -> str:
    """Create a coach-facing interpretation of the progress summary."""
    if not summary.trend_available:
        return (
            "Trend analysis is unavailable because the client has fewer than two "
            "assessments. Schedule a follow-up assessment before changing the plan."
        )

    base_message = (
        f"Weight change: {summary.weight_change_kg} kg. "
        f"Body fat change: {summary.body_fat_change_percentage} percentage points. "
        f"Skeletal muscle mass change: {summary.muscle_mass_change_kg} kg."
    )

    if summary.classification == "positive":
        return f"{base_message} The trend looks positive for the stated goal."

    if summary.classification == "needs_attention":
        return (
            f"{base_message} The trend needs attention. Review adherence, recovery, "
            "training load, and nutrition targets."
        )

    return f"{base_message} The trend is mixed. Continue monitoring before major changes."

