"""Report response schemas."""

from typing import Optional

from sqlmodel import SQLModel


class ProgressSummaryRead(SQLModel):
    """Serializable progress summary response."""

    trend_available: bool
    classification: str
    weight_change_kg: float
    body_fat_change_percentage: float
    muscle_mass_change_kg: float


class ClientProgressSummaryRead(SQLModel):
    """Client progress endpoint response."""

    client_id: int
    client_name: str
    main_goal: str
    records_count: int
    latest_measurement_date: Optional[str]
    summary: ProgressSummaryRead
    message: str


class ReportRead(SQLModel):
    """Coach or client report response."""

    audience: str
    client_id: int
    client_name: str
    main_goal: str
    records_count: int
    message: str
    summary: ProgressSummaryRead
    disclaimer: Optional[str] = None
    next_step: Optional[str] = None
