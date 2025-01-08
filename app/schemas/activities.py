from typing import Optional

from pydantic import BaseModel, field_validator, Field, ConfigDict

from app.core.config import settings
from app.models.organizations import Organization


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    parent_id: int | None = None


class ActivityCreate(ActivityBase):
    @field_validator("parent_id")
    def validate_parent_id(cls, parent_id: int | None, values: dict) -> int | None:
        """Validate that parent_id is not the same as the activity_id"""
        if parent_id is not None and parent_id == values.get("id"):
            raise ValueError("Activity cannot be its own parent")
        return parent_id


class Activity(ActivityBase):
    id: int
    level: int = Field(default=1, ge=1, le=settings.MAX_ACTIVITY_DEPTH)
    children: list["Activity"] | None = None
    parent: "Activity" | None = None
    organizations: list["Organization"] | None = None

    model_config = ConfigDict(from_attributes=True)
