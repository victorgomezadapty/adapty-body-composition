"""Client request and response schemas."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ClientBase(SQLModel):
    """Shared client fields."""

    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=40)
    gender: str = Field(min_length=1, max_length=40)
    birth_date: Optional[date] = None
    main_goal: str = Field(min_length=1, max_length=80)


class ClientCreate(ClientBase):
    """Payload used to create a client."""


class ClientUpdate(SQLModel):
    """Payload used to update a client."""

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    email: Optional[str] = Field(default=None, min_length=3, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=40)
    gender: Optional[str] = Field(default=None, min_length=1, max_length=40)
    birth_date: Optional[date] = None
    main_goal: Optional[str] = Field(default=None, min_length=1, max_length=80)


class ClientRead(ClientBase):
    """Client response schema."""

    id: int
    created_at: datetime
