from fastapi import HTTPException

def organization_not_found():
    return HTTPException(status_code=404, detail="Organization not found")

def phone_not_found():
    return HTTPException(status_code=404, detail="Phone not found")

