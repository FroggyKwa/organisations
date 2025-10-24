from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models


def get_buildings(db: Session):
    return db.query(models.Building).all()


def get_building(db: Session, id: int):
    return db.query(models.Building).get(id)


def update_building(db: Session, building: models.Building) -> models.Building:

    for field, value in building.model_dump(exclude_unset=True).items():
        setattr(building, field, value)

    db.commit()
    db.refresh(building)
    return building

def delete_building(db: Session, building: models.Building) -> models.Building:
    db.delete(building)
    db.commit()
    return building


def create_building(db: Session, building: schemas.BuildingCreate) -> models.Building:
    db_building = models.Building(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building
