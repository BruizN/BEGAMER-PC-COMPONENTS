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

    variant = await catalog_service.get_variant(session, item_data.variant_id, only_active=True)

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


async def get_cart(
    redis_client: redis.Redis,
    session: AsyncSession,
    identity: tuple[str, str]
) -> cart_schemas.CartResponse:

    cart_key, _ = _get_cart_key_and_ttl(identity)
    cart_data = await redis_client.hgetall(cart_key)

    response = cart_schemas.CartResponse(cart_id=cart_key)

    if not cart_data:
        return response
    
    total_price = Decimal("0.00")

    for variant_id_str, quantity_str in cart_data.items():
        quantity = int (quantity_str)
        variant_uuid = uuid.UUID(variant_id_str)

        try:
            variant = await catalog_service.get_variant(session, variant_uuid, only_active=True)

            main_image_url = None
            if variant.images:
                main_img = next((img for img in variant.images if img.is_main), variant.images[0])
                main_image_url = main_img.image_url
            elif variant.product.images:
                main_img = next((img for img in variant.product.images if img.is_main), variant.product.images[0])
                main_image_url = main_img.image_url
            
            subtotal = variant.price * Decimal(quantity)
            total_price += subtotal

            item_response = cart_schemas.CartItemResponse(
                variant_id=variant.variant_id,
                product_id=variant.product_id,
                name=variant.product.name,
                sku=variant.sku,
                image_url=main_image_url,
                unit_price=variant.price,
                quantity=quantity,
                subtotal=subtotal
            )
            response.items.append(item_response)

        except HTTPException:
            # Si la variante ya no existe en la BD se borra silenciosamente del carrito del usuario en Redis
            await redis_client.hdel(cart_key, variant_id_str)

    response.total_price = total_price
    return response


async def update_item_quantity(
    redis_client: redis.Redis,
    session: AsyncSession,
    identity: tuple[str, str],
    variant_id: uuid.UUID,
    update_data: cart_schemas.CartItemUpdate
) -> dict:

    cart_key, ttl = _get_cart_key_and_ttl(identity)
    variant_id_str = str(variant_id)

    if update_data.quantity == 0:
        await redis_client.hdel(cart_key, variant_id_str)
        return {"message": "Item removed from cart"}

    await catalog_service.get_variant(session, variant_id, only_active=True)

    await redis_client.hset(cart_key, variant_id_str, update_data.quantity)
    await redis_client.expire(cart_key, ttl)

    return {"message": "Quantity updated", "new_quantity": update_data.quantity}


async def remove_item_from_cart(
    redis_client: redis.Redis,
    identity: tuple[str, str],
    variant_id: uuid.UUID
) -> None:

    cart_key, _ = _get_cart_key_and_ttl(identity)
    await redis_client.hdel(cart_key, str(variant_id))