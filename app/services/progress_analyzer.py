"""Pure Python progress analysis helpers."""

from dataclasses import dataclass
from typing import Any

from app.exceptions.custom_exceptions import InvalidAssessmentValueError


@dataclass(frozen=True)
class ProgressSummary:
    """Computed progress between the first and latest InBody-style records."""

    weight_change_kg: float
    body_fat_change_percentage: float
    muscle_mass_change_kg: float
    classification: str
    trend_available: bool = True


def _read_metric(record: Any, metric_name: str) -> float:
    """Read a numeric metric from an object or dictionary."""
    if isinstance(record, dict):
        value = record.get(metric_name)
    else:
        value = getattr(record, metric_name, None)

    if value is None:
        raise InvalidAssessmentValueError(f"Missing required metric: {metric_name}")

    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise InvalidAssessmentValueError(
            f"Metric {metric_name} must be numeric."
        ) from exc

    return numeric_value


def calculate_weight_change(first_record: Any, latest_record: Any) -> float:
    """Calculate weight change in kilograms from first to latest record."""
    return round(
        _read_metric(latest_record, "weight_kg") - _read_metric(first_record, "weight_kg"),
        2,
    )


def calculate_body_fat_change(first_record: Any, latest_record: Any) -> float:
    """Calculate body fat percentage-point change from first to latest record."""
    return round(
        _read_metric(latest_record, "body_fat_percentage")
        - _read_metric(first_record, "body_fat_percentage"),
        2,
    )


def calculate_muscle_mass_change(first_record: Any, latest_record: Any) -> float:
    """Calculate skeletal muscle mass change in kilograms."""
    return round(
        _read_metric(latest_record, "skeletal_muscle_mass_kg")
        - _read_metric(first_record, "skeletal_muscle_mass_kg"),
        2,
    )


def classify_progress(
    goal_type: str,
    weight_change_kg: float,
    body_fat_change_percentage: float,
    muscle_mass_change_kg: float,
) -> str:
    """Classify progress using simple educational coaching rules."""
    normalized_goal = goal_type.strip().lower()

    if normalized_goal == "fat_loss":
        if body_fat_change_percentage < 0 and muscle_mass_change_kg >= -0.5:
            return "positive"
        if body_fat_change_percentage > 0.5:
            return "needs_attention"
        return "mixed"

    if normalized_goal == "muscle_gain":
        if muscle_mass_change_kg > 0 and body_fat_change_percentage <= 1.5:
            return "positive"
        if muscle_mass_change_kg <= 0:
            return "needs_attention"
        return "mixed"

    if normalized_goal == "recomposition":
        if body_fat_change_percentage < 0 and muscle_mass_change_kg > 0:
            return "positive"
        if body_fat_change_percentage > 0 and muscle_mass_change_kg < 0:
            return "needs_attention"
        return "mixed"

    if weight_change_kg == 0 and body_fat_change_percentage == 0 and muscle_mass_change_kg == 0:
        return "stable"

    return "monitor"


def build_progress_summary(records: list[Any], goal_type: str) -> ProgressSummary:
    """Build a progress summary from chronological assessment records."""
    if len(records) < 2:
        return ProgressSummary(
            weight_change_kg=0.0,
            body_fat_change_percentage=0.0,
            muscle_mass_change_kg=0.0,
            classification="not_enough_data",
            trend_available=False,
        )

    first_record = records[0]
    latest_record = records[-1]
    weight_change_kg = calculate_weight_change(first_record, latest_record)
    body_fat_change_percentage = calculate_body_fat_change(first_record, latest_record)
    muscle_mass_change_kg = calculate_muscle_mass_change(first_record, latest_record)

    return ProgressSummary(
        weight_change_kg=weight_change_kg,
        body_fat_change_percentage=body_fat_change_percentage,
        muscle_mass_change_kg=muscle_mass_change_kg,
        classification=classify_progress(
            goal_type=goal_type,
            weight_change_kg=weight_change_kg,
            body_fat_change_percentage=body_fat_change_percentage,
            muscle_mass_change_kg=muscle_mass_change_kg,
        ),
    )

