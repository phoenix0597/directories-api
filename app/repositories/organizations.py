from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.models.organizations import Organization
from typing import List


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_building(self, building_id: int) -> List[Organization]:
        query = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                joinedload(Organization.phones),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_activity(self, activity_id: int) -> List[Organization]:
        query = (
            select(Organization)
            .join(Organization.activities)
            .where(Organization.activities.any(id=activity_id))
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_by_name(self, name: str) -> List[Organization]:
        query = (
            select(Organization)
            .where(Organization.name.ilike(f"%{name}%"))
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phones),
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
