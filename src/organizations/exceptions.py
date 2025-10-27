from fastapi import HTTPException

def organization_not_found():
    return HTTPException(status_code=404, detail="Organization not found")

def phone_not_found():
    return HTTPException(status_code=404, detail="Phone not found")

def latitude_incorrect():
    return HTTPException(status_code=400, detail="Invalid latitude")

def longitude_incorrect():
    return HTTPException(status_code=400, detail="Invalid longitude")

def radius_incorrect():
    return HTTPException(status_code=400, detail="Radius must be positive")
