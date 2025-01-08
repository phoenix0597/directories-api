from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
import re

if TYPE_CHECKING:
    from app.schemas.organizations import Organization


class PhoneBase(BaseModel):
    number: str = Field(
        ...,
        min_length=10,
        max_length=20,
        pattern=r"^\+?[1-9]\d{9,19}$",
        description="Phone number in international format, optionally starting with +",
    )
    organization_id: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int
    organization: "Organization" | None = None
