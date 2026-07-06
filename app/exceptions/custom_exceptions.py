"""Custom exceptions used across the application."""


class AdaptyInBodyError(Exception):
    """Base exception for expected application errors."""


class NotEnoughRecordsError(AdaptyInBodyError):
    """Raised when a progress trend requires at least two records."""


class InvalidAssessmentValueError(AdaptyInBodyError):
    """Raised when an assessment metric is missing or invalid."""

