from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, service, exceptions, models
from src.database import get_db
from .dependencies import get_building_by_id

router = APIRouter()


@router.get("/", response_model=list[schemas.BuildingRead])
async def get_buildings(db: Session = Depends(get_db)) -> schemas.BuildingRead:
    return await service.get_buildings(db)


@router.post("/", response_model=schemas.BuildingRead)
async def create_building(
    building_data: schemas.BuildingCreate, db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    return await service.create_building(db, building_data)


@router.get("/{id}", response_model=schemas.BuildingRead)
async def get_building(
    building: models.Building = Depends(get_building_by_id), db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    return building


@router.put("/{id}", response_model=schemas.BuildingRead)
async def update_building(
    new_data: schemas.BuildingUpdate,
    building: models.Building = Depends(get_building_by_id),
    db: Session = Depends(get_db),
) -> schemas.BuildingRead:
    return await service.update_building(db, building, new_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building: models.Building = Depends(get_building_by_id), db: Session = Depends(get_db)
) -> None:
    if building is None:
        raise exceptions.building_not_found()
    return await service.delete_building(db, building)
