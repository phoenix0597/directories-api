from app.repositories.organizations import OrganizationRepository
from app.services.activities import ActivityService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.organizations import Organization


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.repository = OrganizationRepository(session)
        self.activity_service = ActivityService(session)

    async def get_by_building(self, building_id: int) -> List[Organization]:
        return await self.repository.get_by_building(building_id)

    async def get_by_activity_tree(self, activity_id: int) -> List[Organization]:
        """Gets organizations by activity, including all child activities"""
        activity_ids = await self.activity_service.get_activity_tree(activity_id)
        organizations = []
        for act_id in activity_ids:
            orgs = await self.repository.get_by_activity(act_id)
            organizations.extend(orgs)
        return list(set(organizations))  # Убираем дубликаты

    async def search_by_name(self, name: str) -> List[Organization]:
        return await self.repository.search_by_name(name)
