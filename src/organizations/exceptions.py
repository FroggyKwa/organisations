from fastapi import HTTPException

def organization_not_found():
    return HTTPException(status_code=404, detail="Building not found")