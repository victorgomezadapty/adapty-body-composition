"""SQLModel database models."""

from app.models.client import Client
from app.models.goal import Goal
from app.models.inbody_record import InBodyRecord
from app.models.plan import Plan

__all__ = ["Client", "Goal", "InBodyRecord", "Plan"]
