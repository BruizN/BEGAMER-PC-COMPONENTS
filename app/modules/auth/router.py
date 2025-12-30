from fastapi import APIRouter
from app.modules.auth.schemas import TokenOut, LoginRequest
from app.core.dependencies import SessionDep #Dependencia de sesion asincrona
from app.modules.auth.service import login_user

router = APIRouter()


@router.post(
    "/login", 
    response_model=TokenOut, 
    summary="Inicia sesion con email y contraseña"
    )
async def login(session: SessionDep, body: LoginRequest):
    token = await login_user(session, body.email, body.password)
    return {"access_token": token, "token_type": "bearer"}





