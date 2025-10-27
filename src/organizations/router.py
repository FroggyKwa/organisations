from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from . import schemas, service, exceptions

from src.database import get_db
from .dependencies import get_organization_by_id

from src.buildings.dependencies import get_building_by_id
from src.buildings import models as buildings_models
from src.activities import models as activities_models
from src.activities.dependencies import get_activity_by_id

from src.utils import schemas as utils_schemas


router = APIRouter()


@router.get("/", response_model=list[schemas.OrganizationRead])
async def get_organizations(db: Session = Depends(get_db)) -> schemas.OrganizationRead:
    """
    Get all organizations
    """
    return await service.get_organizations(db)


@router.post("/", response_model=schemas.OrganizationRead)
async def create_organization(
    organization_data: schemas.OrganizationCreate, db: Session = Depends(get_db)
) -> schemas.OrganizationRead:
    """
    Create a new organization
    """
    return await service.create_organization(db, organization_data)


@router.get("/{id}", response_model=schemas.OrganizationRead)
async def get_organization(
    organization=Depends(get_organization_by_id),
) -> schemas.OrganizationRead:
    """
    Get an organization by id
    """
    return organization


@router.put("/{id}", response_model=schemas.OrganizationRead)
async def update_organization(
    new_data: schemas.OrganizationUpdate,
    organization=Depends(get_organization_by_id),
    db: Session = Depends(get_db),
) -> schemas.OrganizationRead:
    """
    Update an organization by id
    """
    return await service.update_organization(db, organization, new_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization=Depends(get_organization_by_id), db: Session = Depends(get_db)
) -> None:
    """
    Delete an organization by id
    """
    if organization is None:
        raise exceptions.organization_not_found()
    await service.delete_organization(db, organization)


@router.get("/by_building/{building_id}", response_model=list[schemas.OrganizationRead])
async def get_organizations_by_building(
    building: buildings_models.Building = Depends(get_building_by_id),
    db: Session = Depends(get_db),
):
    """
    Get all organizations by building
    """
    return await service.get_organizations_by_building(building, db)


@router.get("/by_activity/{activity_id}", response_model=list[schemas.OrganizationRead])
async def get_organizations_by_activity(
    activity: activities_models.Activity = Depends(get_activity_by_id),
    db: Session = Depends(get_db),
):
    """
    Get all organizations by activity_id
    """
    return await service.get_organizations_by_activity(activity, db)


@router.get("/by_name/{name}", response_model=list[schemas.OrganizationRead])
async def get_organizations_by_activity(
    name: str,
    db: Session = Depends(get_db),
):
    """
    Get all organizations by name
    """
    return await service.get_organizations_by_name(name, db)


@router.get("/in_bbox/", response_model=list[schemas.OrganizationRead])
async def get_organizations_by_activity(
    bbox: utils_schemas.BBoxQuery = Depends(),
    db: Session = Depends(get_db),
):
    """
    Get all organizations by bbox
    """
    return await service.get_organizations_in_bbox(db, bbox)


@router.get("/in_radius/", response_model=list[schemas.OrganizationRead])
def organizations_in_radius(
    circle: utils_schemas.CircleQuery = Depends(),
    db: Session = Depends(get_db),
):
    """
    Get all organizations in followed radius using Haversine formula
    (great-circle distance between two points on a sphere)
    """
    return service.get_organizations_in_radius(db, circle)
