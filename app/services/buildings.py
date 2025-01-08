from app.repositories.buildings import BuildingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class BuildingService:
    def __init__(self, session: AsyncSession):
        self.repository = BuildingRepository(session)

    async def get_buildings_in_radius(
        self, latitude: float, longitude: float, radius: float
    ) -> List[dict]:
        buildings = await self.repository.get_buildings_in_radius(
            latitude, longitude, radius
        )
        return buildings
