from pydantic import BaseModel, Field, ConfigDict


class BuildingBase(BaseModel):
    address: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, populate_by_name=True
    )


Building.model_rebuild()
