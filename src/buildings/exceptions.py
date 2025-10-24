from fastapi import HTTPException

def building_not_found():
    return HTTPException(status_code=404, detail="Building not found")