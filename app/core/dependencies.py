from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.modules.auth.models import User
from app.core.config import settings
from app.core.security import http_bearer
from app.modules.auth import repository as repo
from app.core.db import get_db
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt
import uuid6

SessionDep = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(
    session: SessionDep,
    token_auth: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> User:
    token = token_auth.credentials

    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_alg]
            )
        user_id_str = payload.get("sub")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token invalido"
                )

        user_uuid = uuid6.UUID(user_id_str)
    
    except jwt.PyJWKError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expirado o invalido"
            )
        
    user = await repo.get_user_by_id(session, user_uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no encontrado"
            ) 
    
    return user