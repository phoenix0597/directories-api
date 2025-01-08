from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin, ST_MakePoint
from app.models.buildings import Building
from typing import List


class BuildingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_buildings_in_radius(
        self, latitude: float, longitude: float, radius: float
    ) -> List[Building]:
        point = f"SRID=4326;POINT({longitude} {latitude})"
        query = select(Building).where(
            ST_DWithin(Building.location, ST_MakePoint(longitude, latitude), radius)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, building_id: int) -> Building:
        query = select(Building).where(Building.id == building_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
