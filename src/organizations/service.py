from typing import Any, Coroutine

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import schemas, models, exceptions

from src.buildings import models as buildings_models

from src.activities import models as activities_models
import src.activities.exceptions as activities_exceptions

from src.utils import schemas as utils_schemas


async def get_organizations(db: Session):
    return db.query(models.Organization).all()


async def update_organization(
    db: Session, organization: models.Organization, new_data: schemas.OrganizationUpdate
) -> models.Organization:
    if organization is None:
        raise exceptions.organization_not_found()

    update_data = new_data.model_dump(exclude_unset=True)
    if "name" in update_data:
        organization.name = update_data["name"]
    if "building_id" in update_data:
        organization.building_id = update_data["building_id"]

    if "phone_numbers" in update_data:
        organization.phones = [
            models.Phone(number=num) for num in update_data["phone_numbers"]
        ]

    if "activity_ids" in update_data:
        print(update_data["activity_ids"])
        activities = (
            db.query(activities_models.Activity)
            .filter(activities_models.Activity.id.in_(update_data["activity_ids"]))
            .all()
        )
        organization.activities = activities

    db.commit()
    db.refresh(organization)
    return organization


async def delete_organization(db: Session, organization: models.Organization) -> None:
    db.delete(organization)
    db.commit()


async def create_organization(
    db: Session, organization: schemas.OrganizationCreate
) -> models.Organization:
    db_organization = models.Organization(
        **organization.model_dump(exclude={"activity_ids", "phones"})
    )

    if organization.activity_ids:
        activities = (
            db.query(activities_models.Activity)
            .filter(activities_models.Activity.id.in_(organization.activity_ids))
            .all()
        )
        if not activities:
            raise activities_exceptions.activity_not_found()
        db_organization.activities = activities

    if organization.phones:
        db_organization.phones = [
            models.Phone(number=p.number) for p in organization.phones
        ]

    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


async def get_organizations_by_building(
    building: models.Building, db: Session
) -> list[type[models.Organization]]:
    return db.query(models.Organization).filter_by(building_id=building.id).all()


async def get_organizations_by_activity(
    activity: activities_models.Activity, db: Session
) -> list[type[models.Organization]]:
    return (
        db.query(models.Organization)
        .join(models.Organization.activities)
        .filter(models.Organization.activities.any(id=activity.id))
        .all()
    )


async def get_organizations_by_name(
    name: str, db: Session
) -> list[type[models.Organization]]:
    return (
        db.query(models.Organization)
        .filter(models.Organization.name.ilike(f"%{name}%"))
        .all()
    )


async def get_organizations_in_bbox(
    db: Session, bbox: utils_schemas.BBoxQuery
) -> list[type[models.Organization]]:
    buildings = (
        db.query(models.Building.id)
        .filter(
            models.Building.latitude.between(bbox.min_latitude, bbox.max_latitude),
            models.Building.longitude.between(bbox.min_longitude, bbox.max_longitude),
        )
        .subquery()
    )
    return (
        db.query(models.Organization)
        .filter(models.Organization.building_id.in_(buildings))
        .all()
    )


def get_organizations_in_radius(
    db: Session,
    circle: utils_schemas.CircleQuery,
) -> list[type[models.Organization]]:
    R = 6371
    if not (-90 <= circle.center_lat <= 90):
        raise exceptions.latitude_incorrect()
    if not (-180 <= circle.center_lon <= 180):
        raise exceptions.longitude_incorrect()
    if circle.radius_km <= 0:
        raise exceptions.radius_incorrect()

    R = 6371.0

    cos_product = func.cos(func.radians(circle.center_lat)) * func.cos(
        func.radians(buildings_models.Building.latitude)
    ) * func.cos(
        func.radians(buildings_models.Building.longitude)
        - func.radians(circle.center_lon)
    ) + func.sin(
        func.radians(circle.center_lat)
    ) * func.sin(
        func.radians(buildings_models.Building.latitude)
    )

    safe_arg = func.greatest(-1.0, func.least(1.0, cos_product))  # nan protection
    distance = R * func.acos(safe_arg)

    buildings_subq = (
        db.query(buildings_models.Building.id)
        .filter(distance <= float(circle.radius_km))
        .subquery()
    )

    return (
        db.query(models.Organization)
        .filter(models.Organization.building_id.in_(buildings_subq))
        .all()
    )
