"""Client database model."""

from datetime import date, datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Client(SQLModel, table=True):
    """A coaching or physiotherapy client using synthetic demo data."""

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: str = Field(index=True, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=40)
    gender: str = Field(max_length=40)
    birth_date: Optional[date] = None
    main_goal: str = Field(index=True, max_length=80)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

