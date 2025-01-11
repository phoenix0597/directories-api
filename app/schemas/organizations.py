import re
from typing import TYPE_CHECKING, List
from pydantic import BaseModel, Field, ConfigDict, field_validator

if TYPE_CHECKING:
    from app.schemas.buildings import Building
    from app.schemas.activities import ActivityResponse

pattern = re.compile(r"^(?=.{1,16}$)\+?(\d{1,3}-)+\d{1,3}$")


class OrganizationBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Organization name, e.g. ООО 'Рога и Копыта'",
    )
    building_id: int = Field(..., gt=0)


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
        None,
        min_items=1,
        description="List of activity IDs",
    )


class OrganizationResponse(OrganizationBase):
    id: int
    building: "Building"
    activities: List["ActivityResponse"] | None = None
    phones: List["str"] | None = None

    @field_validator("phones")
    def validate_phones(cls, v):
        if not all(pattern.match(phone.strip("'")) for phone in v):
            raise ValueError(
                "Phone number should contain only 9-16 digits and start with or without + sign"
            )
        return v

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )


# Allow forward references
from app.schemas.buildings import Building  # noqa
from app.schemas.activities import ActivityResponse  # noqa

OrganizationResponse.model_rebuild()
