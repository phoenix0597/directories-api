from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2.functions import (
    ST_DWithin,
    ST_GeogFromText,
)
from geoalchemy2.types import Geography
from app.models.buildings import Building
from typing import List


class BuildingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_buildings_in_radius(
        self,
        latitude: float,
        longitude: float,
        radius: float,
    ) -> List[Building]:
        # ) -> List[dict]:
        # point = f"SRID=4326;POINT({latitude} {longitude})"
        point = f"SRID=4326;POINT({longitude} {latitude})"
        query = (
            select(
                Building,
                func.ST_Distance(
                    Building.location.cast(Geography), func.ST_GeogFromText(point)
                ).label("distance"),
            )
            .where(ST_DWithin(Building.location, ST_GeogFromText(point), radius))
            .order_by("distance")
        )

        # for debug
        print(f"\n\nSQL query: \n\n{query}\n\n")
        print(
            f"\n\nParameters: latitude={latitude}, longitude={longitude}, radius={radius}\n\n"
        )

        result = await self.session.execute(query)
        buildings = result.scalars().all()

        # for debug
        print(f"\n\nBuildings in radius: {buildings}\n\n")

        # for debug
        for building in buildings:
            print(
                f"\n\nBuilding: {building}, building as dict: {building.to_dict()}\n\n"
            )

        return buildings

    async def get_by_id(self, building_id: int) -> Building:
        query = select(Building).where(Building.id == building_id)
        result = await self.session.execute(query)

        # for debug
        print(f"\n\nSQL query: \n\n{query}\n\n")
        print(f"\n\nBuilding: {result.scalar_one_or_none()}\n\n")

        return result.scalar_one_or_none().to_dict()
