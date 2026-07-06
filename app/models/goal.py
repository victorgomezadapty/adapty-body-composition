"""Goal database model."""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Goal(SQLModel, table=True):
    """Client goal for body composition or performance support."""

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", index=True)
    goal_type: str = Field(index=True, max_length=80)
    target_weight_kg: Optional[float] = Field(default=None, gt=0)
    target_body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=80)
    target_muscle_mass_kg: Optional[float] = Field(default=None, gt=0)
    deadline: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=1000)

