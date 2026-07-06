"""InBody-style assessment CRUD endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.inbody_record import InBodyRecord
from app.routers.helpers import apply_updates, get_client_or_404
from app.schemas.inbody_schema import (
    InBodyRecordCreate,
    InBodyRecordRead,
    InBodyRecordUpdate,
)

router = APIRouter(tags=["inbody records"])


@router.post(
    "/clients/{client_id}/inbody-records",
    response_model=InBodyRecordRead,
    status_code=status.HTTP_201_CREATED,
)
def create_inbody_record(
    client_id: int,
    payload: InBodyRecordCreate,
    session: Session = Depends(get_session),
) -> InBodyRecord:
    """Create an InBody-style assessment for a client."""
    get_client_or_404(session, client_id)

    record = InBodyRecord(client_id=client_id, **payload.model_dump())
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.get("/clients/{client_id}/inbody-records", response_model=list[InBodyRecordRead])
def list_client_inbody_records(
    client_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
) -> list[InBodyRecord]:
    """List a client's InBody-style assessments."""
    get_client_or_404(session, client_id)
    statement = (
        select(InBodyRecord)
        .where(InBodyRecord.client_id == client_id)
        .order_by(InBodyRecord.measurement_date)
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


@router.get("/inbody-records", response_model=list[InBodyRecordRead])
def list_inbody_records(
    client_id: Optional[int] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[InBodyRecord]:
    """List all assessments, optionally filtered by client."""
    statement = select(InBodyRecord).order_by(
        InBodyRecord.client_id,
        InBodyRecord.measurement_date,
    )
    if client_id is not None:
        get_client_or_404(session, client_id)
        statement = statement.where(InBodyRecord.client_id == client_id)
    return list(session.exec(statement.offset(skip).limit(limit)).all())


@router.get("/inbody-records/{record_id}", response_model=InBodyRecordRead)
def get_inbody_record(
    record_id: int,
    session: Session = Depends(get_session),
) -> InBodyRecord:
    """Get one InBody-style assessment."""
    record = session.get(InBodyRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="InBody record not found")
    return record


@router.patch("/inbody-records/{record_id}", response_model=InBodyRecordRead)
def update_inbody_record(
    record_id: int,
    payload: InBodyRecordUpdate,
    session: Session = Depends(get_session),
) -> InBodyRecord:
    """Update an InBody-style assessment."""
    record = session.get(InBodyRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="InBody record not found")

    apply_updates(record, payload.model_dump(exclude_unset=True))
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.delete("/inbody-records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inbody_record(
    record_id: int,
    session: Session = Depends(get_session),
) -> None:
    """Delete one InBody-style assessment."""
    record = session.get(InBodyRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="InBody record not found")

    session.delete(record)
    session.commit()

