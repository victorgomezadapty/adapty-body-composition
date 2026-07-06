"""Plan database model."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Plan(SQLModel, table=True):
    """Basic client plan for training, nutrition, rehab, or hybrid work."""

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", index=True)
    plan_type: str = Field(index=True, max_length=80)
    weekly_training_sessions: Optional[int] = Field(default=None, ge=0, le=14)
    calorie_target: Optional[int] = Field(default=None, gt=0)
    protein_target_g: Optional[int] = Field(default=None, gt=0)
    notes: Optional[str] = Field(default=None, max_length=1000)
