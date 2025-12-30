from app.modules.auth import repository as repo
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from pydantic import EmailStr, SecretStr
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.concurrency import run_in_threadpool



async def login_user(session: AsyncSession, email: EmailStr, password: SecretStr) -> str:
    user = await repo.get_user_by_email(session, email)
    #cambiar verify password a RUN IN THREADPOOL
    if not user or not await run_in_threadpool(
        verify_password, 
        password.get_secret_value(), 
        user.hashed_password
        ):
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
            )
    return create_access_token(data={"sub": str(user.user_id), "role": user.role})

    
