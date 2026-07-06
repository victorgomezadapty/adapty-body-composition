"""Client CRUD endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.client import Client
from app.models.goal import Goal
from app.models.inbody_record import InBodyRecord
from app.models.plan import Plan
from app.routers.helpers import apply_updates, get_client_or_404
from app.schemas.client_schema import ClientCreate, ClientRead, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    session: Session = Depends(get_session),
) -> Client:
    """Create a client."""
    existing_client = session.exec(
        select(Client).where(Client.email == payload.email)
    ).first()
    if existing_client:
        raise HTTPException(status_code=409, detail="Client email already exists")

    client = Client(**payload.model_dump())
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.get("", response_model=list[ClientRead])
def list_clients(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    main_goal: Optional[str] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_session),
) -> list[Client]:
    """List clients with pagination and optional filters."""
    statement = select(Client)

    if main_goal:
        statement = statement.where(Client.main_goal == main_goal)

    if search:
        statement = statement.where(
            or_(
                Client.first_name.contains(search),
                Client.last_name.contains(search),
                Client.email.contains(search),
            )
        )

    return list(session.exec(statement.offset(skip).limit(limit)).all())


@router.get("/{client_id}", response_model=ClientRead)
def get_client(
    client_id: int,
    session: Session = Depends(get_session),
) -> Client:
    """Get one client."""
    return get_client_or_404(session, client_id)


@router.patch("/{client_id}", response_model=ClientRead)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    session: Session = Depends(get_session),
) -> Client:
    """Update a client."""
    client = get_client_or_404(session, client_id)
    updates = payload.model_dump(exclude_unset=True)

    if "email" in updates:
        existing_client = session.exec(
            select(Client).where(Client.email == updates["email"], Client.id != client_id)
        ).first()
        if existing_client:
            raise HTTPException(status_code=409, detail="Client email already exists")

    apply_updates(client, updates)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    session: Session = Depends(get_session),
) -> None:
    """Delete a client and related MVP records."""
    client = get_client_or_404(session, client_id)

    for model in (InBodyRecord, Goal, Plan):
        related_items = session.exec(select(model).where(model.client_id == client_id)).all()
        for item in related_items:
            session.delete(item)

    session.delete(client)
    session.commit()

