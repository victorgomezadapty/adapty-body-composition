"""Tests for Phase 1 pure Python services."""

import pytest

from app.exceptions.custom_exceptions import InvalidAssessmentValueError
from app.services.coach_message_generator import (
    generate_client_message,
    generate_coach_message,
)
from app.services.progress_analyzer import (
    build_progress_summary,
    calculate_body_fat_change,
    calculate_muscle_mass_change,
    calculate_weight_change,
    classify_progress,
    ProgressSummary,
)
from app.services.nutrition_engine import get_nutrition_engine_status
from app.services.report_generator import generate_client_report, generate_coach_report


FIRST_RECORD = {
    "weight_kg": 88.0,
    "body_fat_percentage": 28.0,
    "skeletal_muscle_mass_kg": 34.0,
}

LATEST_RECORD = {
    "weight_kg": 84.5,
    "body_fat_percentage": 24.5,
    "skeletal_muscle_mass_kg": 34.4,
}


def test_metric_change_calculations() -> None:
    """Progress metric helpers should calculate changes from first to latest."""
    assert calculate_weight_change(FIRST_RECORD, LATEST_RECORD) == -3.5
    assert calculate_body_fat_change(FIRST_RECORD, LATEST_RECORD) == -3.5
    assert calculate_muscle_mass_change(FIRST_RECORD, LATEST_RECORD) == 0.4


def test_classify_positive_fat_loss_progress() -> None:
    """Fat loss is positive when body fat decreases and muscle is maintained."""
    classification = classify_progress(
        goal_type="fat_loss",
        weight_change_kg=-3.5,
        body_fat_change_percentage=-3.5,
        muscle_mass_change_kg=0.4,
    )

    assert classification == "positive"


def test_classify_needs_attention_fat_loss_progress() -> None:
    """Fat loss needs attention when body fat increases."""
    classification = classify_progress(
        goal_type="fat_loss",
        weight_change_kg=1.0,
        body_fat_change_percentage=1.0,
        muscle_mass_change_kg=0.1,
    )

    assert classification == "needs_attention"


def test_classify_muscle_gain_and_recomposition_progress() -> None:
    """Goal-specific rules should support muscle gain and recomposition."""
    assert (
        classify_progress(
            goal_type="muscle_gain",
            weight_change_kg=2.0,
            body_fat_change_percentage=0.5,
            muscle_mass_change_kg=1.2,
        )
        == "positive"
    )
    assert (
        classify_progress(
            goal_type="muscle_gain",
            weight_change_kg=-1.0,
            body_fat_change_percentage=-0.5,
            muscle_mass_change_kg=-0.2,
        )
        == "needs_attention"
    )
    assert (
        classify_progress(
            goal_type="recomposition",
            weight_change_kg=-0.5,
            body_fat_change_percentage=-2.0,
            muscle_mass_change_kg=0.7,
        )
        == "positive"
    )
    assert (
        classify_progress(
            goal_type="recomposition",
            weight_change_kg=1.0,
            body_fat_change_percentage=1.0,
            muscle_mass_change_kg=-0.3,
        )
        == "needs_attention"
    )


def test_classify_stable_and_monitor_progress() -> None:
    """Unknown goals should produce stable or monitor classifications."""
    assert (
        classify_progress(
            goal_type="health",
            weight_change_kg=0.0,
            body_fat_change_percentage=0.0,
            muscle_mass_change_kg=0.0,
        )
        == "stable"
    )
    assert (
        classify_progress(
            goal_type="performance",
            weight_change_kg=1.0,
            body_fat_change_percentage=-0.3,
            muscle_mass_change_kg=0.2,
        )
        == "monitor"
    )


def test_build_progress_summary_with_two_records() -> None:
    """Two chronological records should produce an available trend."""
    summary = build_progress_summary(
        records=[FIRST_RECORD, LATEST_RECORD],
        goal_type="fat_loss",
    )

    assert summary.trend_available is True
    assert summary.classification == "positive"
    assert summary.weight_change_kg == -3.5


def test_progress_summary_without_enough_records() -> None:
    """A single record should return a clear no-trend summary."""
    summary = build_progress_summary(records=[FIRST_RECORD], goal_type="fat_loss")

    assert summary.trend_available is False
    assert summary.classification == "not_enough_data"
    assert "not available yet" in generate_client_message(summary)
    assert "fewer than two" in generate_coach_message(summary)


def test_invalid_metric_value_raises_custom_error() -> None:
    """Invalid assessment metrics should raise an application-specific error."""
    invalid_record = {
        "weight_kg": "not-a-number",
        "body_fat_percentage": 28.0,
        "skeletal_muscle_mass_kg": 34.0,
    }

    with pytest.raises(InvalidAssessmentValueError):
        calculate_weight_change(invalid_record, LATEST_RECORD)


def test_missing_metric_raises_custom_error() -> None:
    """Missing required metrics should be reported clearly."""
    with pytest.raises(InvalidAssessmentValueError):
        calculate_body_fat_change({"weight_kg": 88.0}, LATEST_RECORD)


def test_metric_helpers_accept_objects() -> None:
    """Progress helpers should support simple objects as well as dictionaries."""

    class Assessment:
        def __init__(self, weight_kg: float) -> None:
            self.weight_kg = weight_kg

    assert calculate_weight_change(Assessment(90.0), Assessment(87.5)) == -2.5


def test_message_generation_for_positive_and_attention_trends() -> None:
    """Message services should adapt tone to the progress classification."""
    positive_summary = ProgressSummary(
        weight_change_kg=-3.5,
        body_fat_change_percentage=-3.5,
        muscle_mass_change_kg=0.4,
        classification="positive",
    )
    attention_summary = ProgressSummary(
        weight_change_kg=1.0,
        body_fat_change_percentage=1.0,
        muscle_mass_change_kg=-0.4,
        classification="needs_attention",
    )

    assert "encouraging progress" in generate_client_message(positive_summary)
    assert "may need adjustment" in generate_client_message(attention_summary)
    assert "needs attention" in generate_coach_message(attention_summary)


def test_nutrition_engine_status() -> None:
    """The nutrition engine placeholder should make future scope explicit."""
    status = get_nutrition_engine_status()

    assert status["status"] == "planned"


def test_report_generation() -> None:
    """Report services should wrap summaries with audience-specific messages."""
    summary = build_progress_summary(
        records=[FIRST_RECORD, LATEST_RECORD],
        goal_type="fat_loss",
    )

    client_report = generate_client_report(summary)
    coach_report = generate_coach_report(summary)

    assert client_report["audience"] == "client"
    assert coach_report["audience"] == "coach"
    assert "medical diagnosis" in client_report["disclaimer"]
    assert "Weight change" in coach_report["message"]
