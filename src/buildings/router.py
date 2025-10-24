from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import schemas, service, exceptions
from src.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.BuildingRead])
def get_buildings(db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    return service.get_buildings(db)


@router.get("/{id}", response_model=schemas.BuildingRead)
def get_building(id: int, db: Session = Depends(get_db)) -> schemas.BuildingRead:
    return service.get_building(db, id)


@router.put("/{id}", response_model=schemas.BuildingRead)
def update_building(id: int, db: Session = Depends(get_db)) -> schemas.BuildingRead:
    building = service.get_building(db, id)
    if building is None:
        raise exceptions.building_not_found()
    return service.update_building(db, id, building)


@router.delete("/{id}", response_model=schemas.BuildingRead)
def delete_building(id: int, db: Session = Depends(get_db)) -> None:
    building = service.get_building(db, id)
    if building is None:
        raise exceptions.building_not_found()
    return service.delete_building(db, building)


@router.post("/", response_model=schemas.BuildingRead)
def create_building(
    building_data: schemas.BuildingCreate, db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    return service.create_building(db, building_data)
