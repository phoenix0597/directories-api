from typing import AsyncGenerator
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.db.session import AsyncSessionLocal
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
    return api_key


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
