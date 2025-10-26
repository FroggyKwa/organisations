from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.buildings.models import Building
from src.activities.models import Activity
from src.models import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    building_id = Column(
        Integer,
        ForeignKey("buildings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    building = relationship(Building, backref="organizations")
    activities = relationship(
        Activity, secondary="organization_activity", back_populates="organizations"
    )
    phones = relationship(
        "Phone", back_populates="organization", cascade="all, delete-orphan"
    )


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship(Organization, back_populates="phones")
