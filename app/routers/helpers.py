"""Shared router helpers."""

from fastapi import HTTPException
from sqlmodel import Session

from app.models.client import Client


def get_client_or_404(session: Session, client_id: int) -> Client:
    """Return a client or raise a 404 error."""
    client = session.get(Client, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def apply_updates(model: object, updates: dict[str, object]) -> None:
    """Apply PATCH-style updates to a SQLModel object."""
    for field_name, value in updates.items():
        setattr(model, field_name, value)

