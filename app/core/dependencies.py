from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends, Header, HTTPException, status
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

def _get_user_id_from_token(token: str, auto_error: bool = True) -> str | None:
    """
    Decodifica el JWT y extrae el ID del usuario
    Si auto_error es True, lanza HTTPExceptions. Si es False, devuelve None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg]
        )
        user_id_str = payload.get("sub")

        if not user_id_str and auto_error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User Token")

        return user_id_str

    except jwt.ExpiredSignatureError:
        if auto_error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
        return None
    except jwt.PyJWTError:
        if auto_error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        return None


async def get_current_user(
    session: SessionDep,
    token_auth: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> User:

    user_id_str = _get_user_id_from_token(token_auth.credentials, auto_error=True)
    user = await repo.get_user_by_id(session, uuid6.UUID(user_id_str))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
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
    token_auth: HTTPAuthorizationCredentials | None = Depends(http_bearer_optional)
) -> User | None:
    if not token_auth:
        return None

    user_id_str = _get_user_id_from_token(token_auth.credentials, auto_error=False)
    if not user_id_str:
        return None

    return await repo.get_user_by_id(session, uuid6.UUID(user_id_str))

CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]




async def get_cart_indentifier(
    token: HTTPAuthorizationCredentials | None = Depends(http_bearer_optional),
    x_guest_session_id: str | None = Header(default=None, alias="X-Guest-Session-ID")
) -> tuple[str, str]:
    """
    Identifica al dueño del carrito.
    Retorna: ("user", "uuid") o ("guest", "uuid").
    """
    if token:
        user_id = _get_user_id_from_token(token.credentials, auto_error=True)
        return ("user", user_id)
    
    if x_guest_session_id:
        return ("guest", x_guest_session_id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="A valid token or the 'X-Guest-Session-ID' header is needed in order to use the cart."
    )

CartIdentifier = Annotated[tuple[str, str], Depends(get_cart_indentifier)]