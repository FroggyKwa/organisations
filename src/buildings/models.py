from sqlalchemy import Column, Integer, String, Float, Index
from src.models import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

Index("idx_buildings_lon_lat", Building.longitude, Building.latitude)
