import uuid
from decimal import Decimal
from fastapi import HTTPException, status
import redis.asyncio as redis
from sqlmodel.ext.asyncio.session import AsyncSession

from app.modules.cart import schemas as cart_schemas
from app.modules.catalog import service as catalog_service


USER_CART_TTL = 7 * 24 * 60 * 60
GUEST_CART_TTL = 24 * 60 * 60


def _get_cart_key_and_ttl(identity: tuple[str, str]) -> tuple [str, int]:
    """
    Genera la clave de Redis y el TTL correcto basándose en la identidad.
    """
    user_type, user_id = identity
    cart_key = f"cart:{user_type}:{user_id}"

    ttl = USER_CART_TTL if user_type == "user" else GUEST_CART_TTL
    return cart_key, ttl

async def add_item_to_cart(
    redis_client: redis.Redis,
    session: AsyncSession,
    identity: tuple[str, str],
    item_data: cart_schemas.CartItemAdd
) -> dict:
    cart_key, ttl = _get_cart_key_and_ttl(identity)
    variant_id_str = str(item_data.variant_id)

    variant = await catalog_service.get_variant(session, item_data.variant_id)

    if variant.stock < item_data.quantity:
        raise HTTPException(status_code=409, detail=f"Just {variant.stock} left!")


    # Consultar en Redis si este ítem ya estaba en el carrito
    current_quantity_bytes = await redis_client.hget(cart_key, variant_id_str)

    current_quantity = int(current_quantity_bytes) if current_quantity_bytes else 0
    new_quantity = current_quantity + item_data.quantity

    if new_quantity > 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="You cannot have more than 10 units of this product"
        )
    
    await redis_client.hset(cart_key, variant_id_str, new_quantity)
    await redis_client.expire(cart_key, ttl)

    return {"message": "Item added to cart", "current_quantity": new_quantity}