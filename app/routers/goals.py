"""Goal CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.goal import Goal
from app.routers.helpers import apply_updates, get_client_or_404
from app.schemas.goal_schema import GoalCreate, GoalRead, GoalUpdate

router = APIRouter(tags=["goals"])


@router.post(
    "/clients/{client_id}/goals",
    response_model=GoalRead,
    status_code=status.HTTP_201_CREATED,
)
def create_goal(
    client_id: int,
    payload: GoalCreate,
    session: Session = Depends(get_session),
) -> Goal:
    """Create a client goal."""
    get_client_or_404(session, client_id)

    goal = Goal(client_id=client_id, **payload.model_dump())
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@router.get("/clients/{client_id}/goals", response_model=list[GoalRead])
def list_client_goals(
    client_id: int,
    session: Session = Depends(get_session),
) -> list[Goal]:
    """List goals for a client."""
    get_client_or_404(session, client_id)
    return list(session.exec(select(Goal).where(Goal.client_id == client_id)).all())


@router.patch("/goals/{goal_id}", response_model=GoalRead)
def update_goal(
    goal_id: int,
    payload: GoalUpdate,
    session: Session = Depends(get_session),
) -> Goal:
    """Update a goal."""
    goal = session.get(Goal, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")

    apply_updates(goal, payload.model_dump(exclude_unset=True))
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    session: Session = Depends(get_session),
) -> None:
    """Delete a goal."""
    goal = session.get(Goal, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")

    session.delete(goal)
    session.commit()

