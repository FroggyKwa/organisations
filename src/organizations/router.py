from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas, service, exceptions
from src.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.OrganizationRead])
def get_organizations(db: Session = Depends(get_db)
) -> schemas.OrganizationRead:
    return service.get_organizations(db)


@router.get("/{id}", response_model=schemas.OrganizationRead)
def get_organization(id: int, db: Session = Depends(get_db)) -> schemas.OrganizationRead:
    return service.get_organization(db, id)


@router.put("/{id}", response_model=schemas.OrganizationRead)
def update_organization(id: int, new_data: schemas.OrganizationUpdate, db: Session = Depends(get_db)) -> schemas.OrganizationRead:
    return service.update_organization(db, id, new_data)


@router.delete("/{id}", response_model=schemas.OrganizationRead)
def delete_organization(id: int, db: Session = Depends(get_db)) -> None:
    organization = service.get_organization(db, id)
    if organization is None:
        raise exceptions.organization_not_found()
    return service.delete_organization(db, organization)


@router.post("/", response_model=schemas.OrganizationRead)
def create_organization(
    organization_data: schemas.OrganizationCreate, db: Session = Depends(get_db)
) -> schemas.OrganizationRead:
    return service.create_organization(db, organization_data)
