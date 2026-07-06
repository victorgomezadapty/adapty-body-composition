"""Plan CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.plan import Plan
from app.routers.helpers import apply_updates, get_client_or_404
from app.schemas.plan_schema import PlanCreate, PlanRead, PlanUpdate

router = APIRouter(tags=["plans"])


@router.post(
    "/clients/{client_id}/plans",
    response_model=PlanRead,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    client_id: int,
    payload: PlanCreate,
    session: Session = Depends(get_session),
) -> Plan:
    """Create a client plan."""
    get_client_or_404(session, client_id)

    plan = Plan(client_id=client_id, **payload.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.get("/clients/{client_id}/plans", response_model=list[PlanRead])
def list_client_plans(
    client_id: int,
    session: Session = Depends(get_session),
) -> list[Plan]:
    """List plans for a client."""
    get_client_or_404(session, client_id)
    return list(session.exec(select(Plan).where(Plan.client_id == client_id)).all())


@router.patch("/plans/{plan_id}", response_model=PlanRead)
def update_plan(
    plan_id: int,
    payload: PlanUpdate,
    session: Session = Depends(get_session),
) -> Plan:
    """Update a plan."""
    plan = session.get(Plan, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    apply_updates(plan, payload.model_dump(exclude_unset=True))
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: int,
    session: Session = Depends(get_session),
) -> None:
    """Delete a plan."""
    plan = session.get(Plan, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    session.delete(plan)
    session.commit()

