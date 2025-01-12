from fastapi import APIRouter, Depends, HTTPException, Query
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


# @router.get(
#     "/by-activity/{activity_id}",
#     response_model=List[OrganizationResponse],
# )
# async def get_organizations_by_activity(
#     activity_id: int, db: AsyncSession = Depends(get_db)
# ):
#     """Search organizations by activity ID"""
#     service = OrganizationService(db)
#     organizations = await service.get_by_activity_tree(activity_id)
#     return organizations


@router.get(
    "/by-radius",
    response_model=List[OrganizationResponse],
)
async def get_organizations_by_radius(
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
        description="Долгота в формате SRID=4326, например: 55.753215",
    ),
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
        description="Широта (latitude) в формате SRID=4326, например: 37.792800",
    ),
    radius: float = Query(..., ge=0, le=100000, description="Радиус поиска в метрах"),
    db: AsyncSession = Depends(
        get_db,
    ),
):
    """Search organizations in the area around the given coordinates and radius (in meters)"""
    building_service = BuildingService(db)
    buildings = await building_service.get_buildings_in_radius(
        # latitude, longitude, radius
        longitude,
        latitude,
        radius,
    )

    # for debug
    print(f"\nFound buildings: {[b.id for b in buildings]}\n")

    org_service = OrganizationService(db)
    organizations = []
    for building in buildings:
        # for debug
        print(f"\nProcessing building: {building.id}\n")

        orgs = await org_service.get_by_building(building.id)

        organizations.extend(orgs)

    print(f"Total organizations found: {len(organizations)}")

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

    return [org.to_dict() for org in organizations]
