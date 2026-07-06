"""Request and response schemas."""

from app.schemas.client_schema import ClientCreate, ClientRead, ClientUpdate
from app.schemas.goal_schema import GoalCreate, GoalRead, GoalUpdate
from app.schemas.inbody_schema import (
    InBodyRecordCreate,
    InBodyRecordRead,
    InBodyRecordUpdate,
)
from app.schemas.plan_schema import PlanCreate, PlanRead, PlanUpdate
from app.schemas.report_schema import (
    ClientProgressSummaryRead,
    ProgressSummaryRead,
    ReportRead,
)

__all__ = [
    "ClientCreate",
    "ClientProgressSummaryRead",
    "ClientRead",
    "ClientUpdate",
    "GoalCreate",
    "GoalRead",
    "GoalUpdate",
    "InBodyRecordCreate",
    "InBodyRecordRead",
    "InBodyRecordUpdate",
    "PlanCreate",
    "PlanRead",
    "PlanUpdate",
    "ProgressSummaryRead",
    "ReportRead",
]
