"""InBody-style assessment request and response schemas."""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class InBodyRecordBase(SQLModel):
    """Shared InBody-style assessment fields."""

    measurement_date: date
    weight_kg: float = Field(gt=0)
    body_fat_percentage: float = Field(ge=0, le=80)
    skeletal_muscle_mass_kg: float = Field(gt=0)
    bmi: Optional[float] = Field(default=None, gt=0)
    visceral_fat_level: Optional[int] = Field(default=None, ge=1, le=30)
    basal_metabolic_rate: Optional[int] = Field(default=None, gt=0)
    waist_hip_ratio: Optional[float] = Field(default=None, gt=0)


class InBodyRecordCreate(InBodyRecordBase):
    """Payload used to create an assessment."""


class InBodyRecordUpdate(SQLModel):
    """Payload used to update an assessment."""

    measurement_date: Optional[date] = None
    weight_kg: Optional[float] = Field(default=None, gt=0)
    body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=80)
    skeletal_muscle_mass_kg: Optional[float] = Field(default=None, gt=0)
    bmi: Optional[float] = Field(default=None, gt=0)
    visceral_fat_level: Optional[int] = Field(default=None, ge=1, le=30)
    basal_metabolic_rate: Optional[int] = Field(default=None, gt=0)
    waist_hip_ratio: Optional[float] = Field(default=None, gt=0)


class InBodyRecordRead(InBodyRecordBase):
    """Assessment response schema."""

    id: int
    client_id: int
