"""InBody-style assessment database model."""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class InBodyRecord(SQLModel, table=True):
    """Body composition assessment linked to a client."""

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", index=True)
    measurement_date: date = Field(index=True)
    weight_kg: float = Field(gt=0)
    body_fat_percentage: float = Field(ge=0, le=80)
    skeletal_muscle_mass_kg: float = Field(gt=0)
    bmi: Optional[float] = Field(default=None, gt=0)
    visceral_fat_level: Optional[int] = Field(default=None, ge=1, le=30)
    basal_metabolic_rate: Optional[int] = Field(default=None, gt=0)
    waist_hip_ratio: Optional[float] = Field(default=None, gt=0)

