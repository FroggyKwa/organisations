from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from . import schemas, service, exceptions
from src.database import get_db
from .dependencies import get_organization_by_id

router = APIRouter()


@router.get("/", response_model=list[schemas.OrganizationRead])
async def get_organizations(db: Session = Depends(get_db)) -> schemas.OrganizationRead:
    return await service.get_organizations(db)


@router.post("/", response_model=schemas.OrganizationRead)
async def create_organization(
    organization_data: schemas.OrganizationCreate, db: Session = Depends(get_db)
) -> schemas.OrganizationRead:
    return await service.create_organization(db, organization_data)


@router.get("/{id}", response_model=schemas.OrganizationRead)
async def get_organization(
    organization=Depends(get_organization_by_id),
) -> schemas.OrganizationRead:
    return organization


@router.put("/{id}", response_model=schemas.OrganizationRead)
async def update_organization(
    new_data: schemas.OrganizationUpdate,
    organization=Depends(get_organization_by_id),
    db: Session = Depends(get_db),
) -> schemas.OrganizationRead:
    return await service.update_organization(db, organization, new_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization=Depends(get_organization_by_id), db: Session = Depends(get_db)
) -> None:
    if organization is None:
        raise exceptions.organization_not_found()
    await service.delete_organization(db, organization)
