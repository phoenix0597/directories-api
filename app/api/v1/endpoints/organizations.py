from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db, verify_api_key
from app.services.organizations import OrganizationService
from app.schemas.organizations import OrganizationResponse
from app.services.buildings import BuildingService

router = APIRouter(
    tags=["Organizations"],
    prefix="/api/v1/organizations",
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "/by-building/{building_id}",
    response_model=List[OrganizationResponse],
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
    response_model=List[OrganizationResponse],
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
    response_model=List[OrganizationResponse],
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
    "/search/{name}",
    response_model=List[OrganizationResponse],
)
async def search_organizations(name: str, db: AsyncSession = Depends(get_db)):
    """Search organizations by name"""
    service = OrganizationService(db)
    organizations = await service.search_by_name(name)

    # Убедимся, что данные о здании загружены
    for org in organizations:
        if org.building is None:
            raise HTTPException(status_code=404, detail="Building not found")

    return jsonable_encoder([org.to_dict() for org in organizations])
    # return organizations
