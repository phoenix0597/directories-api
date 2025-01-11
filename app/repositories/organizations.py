from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload

from app.models.activities import Activity
from app.models.organizations import Organization
from typing import List
from geoalchemy2.functions import ST_X, ST_Y, ST_AsText
from pprint import pprint

from app.models.buildings import Building
from app.schemas.activities import ActivityResponse
from app.schemas.organizations import OrganizationResponse


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _base_query(self):
        return select(
            Organization,
            func.ST_X(func.ST_AsText(Building.location)).label("longitude"),
            func.ST_Y(func.ST_AsText(Building.location)).label("latitude"),
        ).join(Building)

    async def get_by_building(self, building_id: int) -> List[OrganizationResponse]:
        query = (
            self._base_query()
            .where(Organization.building_id == building_id)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
            )
        )
        result = await self.session.execute(query)
        # return result.scalars().all()
        return [self._process_result(row) for row in result]

    async def get_by_activity(self, activity_id: int) -> List[OrganizationResponse]:
        query = (
            self._base_query()
            .join(Organization.activities)
            .where(Organization.activities.any(id=activity_id))
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
            )
        )
        result = await self.session.execute(query)
        return [self._process_result(row) for row in result]

    async def search_by_name(self, name: str) -> List[OrganizationResponse]:
        query = (
            self._base_query()
            .where(Organization.name.ilike(f"%{name}%"))
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities).selectinload(Activity.parent),
            )
        )

        result = await self.session.execute(query)
        organizations = [self._process_result(row) for row in result]
        print("\n\n\n\n")
        [pprint(org.to_dict()) for org in organizations]
        print("\n\n\n\n")

        # # explicit load activities
        # for org in organizations:
        #     await self.session.refresh(org, ["activities"])

        return organizations

    def _process_result(self, row):
        organization, longitude, latitude = row
        if organization.building:
            organization.building.longitude = longitude
            organization.building.latitude = latitude

        print(
            f"\n\n\n\nOrganization ID: {organization.id}, Activities: {organization.activities}"
        )

        return organization
