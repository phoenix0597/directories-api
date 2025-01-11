from __future__ import annotations  # Это нужно для рекурсивных ссылок
from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel, field_validator, Field, ConfigDict
from pydantic import ValidationInfo

from app.core.config import settings


if TYPE_CHECKING:
    from app.models.organizations import Organization  # noqa
    from app.models.activities import Activity  # noqa


from typing import List, Optional
from app.models.activities import Activity


def activity_to_dict(activity: Activity) -> dict:
    return {
        "id": activity.id,
        "name": activity.name,
        "level": activity.level,
        # "parent": activity_to_dict(activity.parent) if activity.parent else None,
        "parent_id": activity.parent_id,
        # "children": (
        #     [activity_to_dict(child) for child in activity.children]
        #     if activity.children
        #     else []
        # ),
    }


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    # parent: Optional["ActivityResponse"] = None


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


class ActivityResponse(ActivityBase):
    id: int
    level: int = Field(default=1, ge=1, le=settings.MAX_ACTIVITY_DEPTH)
    children: Optional[list["ActivityResponse"]] = None
    parent: Optional["ActivityResponse"] = None
    # organizations: list["Organization"] | None = None
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, populate_by_name=True
    )


# Activity.model_rebuild()
