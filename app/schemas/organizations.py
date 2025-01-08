from typing import TYPE_CHECKING, List
from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from .buildings import Building
    from .activities import Activity
    from .phones import Phone


class OrganizationBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Organization name, e.g. ООО 'Рога и Копыта'",
    )
    building_id: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = Field(
        ..., min_items=1, description="List of activity IDs"
    )


class OrganizationUpdate(OrganizationBase):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Organization name, e.g. ООО 'Рога и Копыта'",
    )
    building_id: int | None = Field(None, gt=0)
    activity_ids: List[int] | None = Field(
        None, min_items=1, description="List of activity IDs"
    )


class Organization(OrganizationBase):
    id: int
    building: "Building"
    activities: List["Activity"] | None = None
    phones: List["Phone"] | None = None
