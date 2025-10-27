from pydantic import BaseModel

class BBoxQuery(BaseModel):
    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float


class CircleQuery(BaseModel):
    center_lat: float
    center_lon: float
    radius: float
