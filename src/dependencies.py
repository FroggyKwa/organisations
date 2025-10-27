from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from src.config import settings


async def get_api_key(
    api_key_header: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))
):
    if api_key_header == settings.API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key",
    )
