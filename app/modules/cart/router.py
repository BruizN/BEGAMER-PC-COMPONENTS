from fastapi import APIRouter, Depends, status
import redis.asyncio as redis
import uuid

from app.core.dependencies import SessionDep, CartIdentifier
from app.core.redis import get_redis_client


from app.modules.cart import schemas, service

cart_router = APIRouter()

@cart_router.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    summary="Add an Item to cart"
)
async def add_item(
    item_data: schemas.CartItemAdd,
    identity: CartIdentifier,
    session: SessionDep,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Add a variant to the temporary cart.
    Requires a JWT token or the 'X-Guest-Session-ID' header.
    """
    return await service.add_item_to_cart(redis_client, session, identity, item_data)

@cart_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=schemas.CartResponse,
    summary="View current cart"
)
async def view_cart(
    identity: CartIdentifier,
    session: SessionDep,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Returns the list of items in the cart by cross-referencing the quantities
    in Redis with the actual prices and names in PostgreSQL.
    """
    return await service.get_cart(redis_client, session, identity)

@cart_router.patch(
    "/items/{variant_id}", 
    status_code=status.HTTP_200_OK,
    summary="Update the quantity of an item"
)
async def update_item(
    variant_id: uuid.UUID,
    update_data: schemas.CartItemUpdate,
    identity: CartIdentifier,
    session: SessionDep,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Update the exact quantity of a variant in the cart.
    If quantity = 0 is entered, the item will be removed.
    """
    return await service.update_item_quantity(
        redis_client, session, identity, variant_id, update_data
    )


@cart_router.delete(
    "/items/{variant_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove an item from the cart"
)
async def remove_item(
    variant_id: uuid.UUID,
    identity: CartIdentifier,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    """
    Physically remove a variant of the cart in Redis.
    """
    await service.remove_item_from_cart(redis_client, identity, variant_id)
    return