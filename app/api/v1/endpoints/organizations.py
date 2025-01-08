from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db, verify_api_key
from app.services.organization import OrganizationService
from app.schemas.organization import Organization
from app.services.building import BuildingService

router = APIRouter()


@router.get(
    "/by-building/{building_id}",
    response_model=List[Organization],
    dependencies=[Depends(verify_api_key)],
)
async def get_organizations_by_building(
    building_id: int, db: AsyncSession = Depends(get_db)
):
    """Search organizations by building ID"""
    service = OrganizationService(db)
    organizations = await service.get_by_building(building_id)
    return organizations


@router.get(
    "/by-activity/{activity_id}",
    response_model=List[Organization],
    dependencies=[Depends(verify_api_key)],
)
async def get_organizations_by_activity(
    activity_id: int, db: AsyncSession = Depends(get_db)
):
    """Search organizations by activity ID"""
    service = OrganizationService(db)
    organizations = await service.get_by_activity_tree(activity_id)
    return organizations


@router.get(
    "/by-radius",
    response_model=List[Organization],
    dependencies=[Depends(verify_api_key)],
)
async def get_organizations_by_radius(
    latitude: float, longitude: float, radius: float, db: AsyncSession = Depends(get_db)
):
    """Search organizations in the area around the given coordinates and radius"""
    building_service = BuildingService(db)
    buildings = await building_service.get_buildings_in_radius(
        latitude, longitude, radius
    )

    org_service = OrganizationService(db)
    organizations = []
    for building in buildings:
        orgs = await org_service.get_by_building(building.id)
        organizations.extend(orgs)
    return organizations


@router.get(
    "/search", response_model=List[Organization], dependencies=[Depends(verify_api_key)]
)
async def search_organizations(name: str, db: AsyncSession = Depends(get_db)):
    """Search organizations by name"""
    service = OrganizationService(db)
    organizations = await service.search_by_name(name)
    return organizations
