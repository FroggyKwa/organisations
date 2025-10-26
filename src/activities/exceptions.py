from fastapi import HTTPException

def activity_not_found():
    return HTTPException(status_code=404, detail="Activity not found")