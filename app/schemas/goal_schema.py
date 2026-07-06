"""Goal request and response schemas."""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class GoalBase(SQLModel):
    """Shared goal fields."""

    goal_type: str = Field(min_length=1, max_length=80)
    target_weight_kg: Optional[float] = Field(default=None, gt=0)
    target_body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=80)
    target_muscle_mass_kg: Optional[float] = Field(default=None, gt=0)
    deadline: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=1000)


class GoalCreate(GoalBase):
    """Payload used to create a goal."""


class GoalUpdate(SQLModel):
    """Payload used to update a goal."""

    goal_type: Optional[str] = Field(default=None, min_length=1, max_length=80)
    target_weight_kg: Optional[float] = Field(default=None, gt=0)
    target_body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=80)
    target_muscle_mass_kg: Optional[float] = Field(default=None, gt=0)
    deadline: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=1000)


class GoalRead(GoalBase):
    """Goal response schema."""

    id: int
    client_id: int
