from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from . import schemas, service, exceptions, models
from src.database import get_db
from .dependencies import get_building_by_id

router = APIRouter()


@router.get("/", response_model=list[schemas.BuildingRead])
async def get_buildings(db: Session = Depends(get_db)) -> schemas.BuildingRead:
    """
    Get all buildings
    """
    return await service.get_buildings(db)


@router.post("/", response_model=schemas.BuildingRead)
async def create_building(
    building_data: schemas.BuildingCreate, db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    """
    Create a new building
    """
    return await service.create_building(db, building_data)


@router.get("/{building_id}", response_model=schemas.BuildingRead)
async def get_building(
    building: models.Building = Depends(get_building_by_id), db: Session = Depends(get_db)
) -> schemas.BuildingRead:
    """
    Get building by id
    """
    return building


@router.put("/{building_id}", response_model=schemas.BuildingRead)
async def update_building(
    new_data: schemas.BuildingUpdate,
    building: models.Building = Depends(get_building_by_id),
    db: Session = Depends(get_db),
) -> schemas.BuildingRead:
    """
    Update building by id
    """
    return await service.update_building(db, building, new_data)


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building: models.Building = Depends(get_building_by_id), db: Session = Depends(get_db)
) -> None:
    """
    Delete building by id
    """
    if building is None:
        raise exceptions.building_not_found()
    return await service.delete_building(db, building)
