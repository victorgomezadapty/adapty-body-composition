"""Plan request and response schemas."""

from typing import Optional

from sqlmodel import Field, SQLModel


class PlanBase(SQLModel):
    """Shared plan fields."""

    plan_type: str = Field(min_length=1, max_length=80)
    weekly_training_sessions: Optional[int] = Field(default=None, ge=0, le=14)
    calorie_target: Optional[int] = Field(default=None, gt=0)
    protein_target_g: Optional[int] = Field(default=None, gt=0)
    notes: Optional[str] = Field(default=None, max_length=1000)


class PlanCreate(PlanBase):
    """Payload used to create a plan."""


class PlanUpdate(SQLModel):
    """Payload used to update a plan."""

    plan_type: Optional[str] = Field(default=None, min_length=1, max_length=80)
    weekly_training_sessions: Optional[int] = Field(default=None, ge=0, le=14)
    calorie_target: Optional[int] = Field(default=None, gt=0)
    protein_target_g: Optional[int] = Field(default=None, gt=0)
    notes: Optional[str] = Field(default=None, max_length=1000)


class PlanRead(PlanBase):
    """Plan response schema."""

    id: int
    client_id: int
