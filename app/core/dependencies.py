from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.modules.auth.models import User
from app.core.config import settings
from app.core.security import http_bearer, http_bearer_optional
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
                detail="Invalid User Token"
                )

        user_uuid = uuid6.UUID(user_id_str)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )
    
    except jwt.InvalidTokenError: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
        
    user = await repo.get_user_by_id(session, user_uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
            ) 
    
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Administrator privileges are required"
        )
    return current_user

CurrentAdmin = Annotated[User, Depends(get_current_admin)]


async def get_current_user_optional(
    session: SessionDep,
    token_auth: HTTPAuthorizationCredentials = Depends(http_bearer_optional)
) -> User | None:
    if not token_auth:
        return None

    token = token_auth.credentials

    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_alg]
            )
        user_id_str = payload.get("sub")

        if user_id_str is None:
            return None

        user_uuid = uuid6.UUID(user_id_str)

    except jwt.ExpiredSignatureError:
        return None
    
    except jwt.InvalidTokenError: 
        return None
        
    user = await repo.get_user_by_id(session, user_uuid)

    if not user:
        return None
    
    return user

CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
