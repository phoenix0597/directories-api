from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, field_validator, Field, ConfigDict
from pydantic import ValidationInfo

from app.core.config import settings

if TYPE_CHECKING:
    from app.models.organizations import Organization


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    parent: Optional["Activity"] = None


class ActivityCreate(ActivityBase):
    parent_id: Optional[int] = Field(None, gt=0)

    @field_validator("parent_id", mode="before")
    def validate_parent_id(
        cls, parent_id: int | None, info: ValidationInfo
    ) -> int | None:
        """Validate that parent_id is not the same as the activity_id"""
        data = info.data
        if parent_id is not None and parent_id == data.get("id"):
            raise ValueError("Activity cannot be its own parent")
        return parent_id


class Activity(ActivityBase):
    id: int
    level: int = Field(default=1, ge=1, le=settings.MAX_ACTIVITY_DEPTH)
    children: Optional[list["Activity"]] = None
    # parent: Optional["Activity"] = None
    organizations: list["Organization"] | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


# Activity.model_rebuild()
