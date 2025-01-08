from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True
