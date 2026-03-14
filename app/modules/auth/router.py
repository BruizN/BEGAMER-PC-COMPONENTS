from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Header
import redis.asyncio as redis
from app.core.redis import get_redis_client
from app.modules.cart.service import merge_guest_cart_into_user_cart
from app.modules.auth.schemas import TokenOut, LoginRequest
from app.core.dependencies import SessionDep #Dependencia de sesion asincrona
from app.modules.auth.service import login_user
from app.modules.auth import repository as repo

router = APIRouter()


@router.post(
    "/login", 
    response_model=TokenOut, 
    summary="Log in with email and password"
    )
async def login(
    session: SessionDep, 
    body: LoginRequest,
    background_tasks: BackgroundTasks,
    x_guest_session_id: str | None = Header(default=None, alias="X-Guest-Session-ID"),
    redis_client: redis.Redis = Depends(get_redis_client)
):

    token = await login_user(session, body.email, body.password)
    if x_guest_session_id:
        user = await repo.get_user_by_email(session, body.email)
        if user:
            background_tasks.add_task(
                merge_guest_cart_into_user_cart,
                redis_client=redis_client,
                guest_session_id=x_guest_session_id,
                user_id=str(user.user_id)
            )

    return {"access_token": token, "token_type": "bearer"}





