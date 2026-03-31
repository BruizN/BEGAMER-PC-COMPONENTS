from pydantic import BaseModel, Field
import uuid
from decimal import Decimal


class CartItemAdd(BaseModel):
    """
    Esquema para agregar un nuevo ítem al carrito
    """
    variant_id: uuid.UUID
    quantity: int = Field(gt=0, le=10, description="Quantity to add (maximum 10 per transaction)")

class CartItemUpdate(BaseModel):
    """
    Esquema para actualizar la cantidad exacta de un ítem
    """
    quantity: int = Field(ge=0, le=10, description="New exact quantity (0 will remove the item)")


class CartItemResponse(BaseModel):
    """
    Representa una línea individual dentro del carrito.
    Cruza la cantidad de Redis con los datos reales de PostgreSQL.
    """
    variant_id: uuid.UUID
    product_id: uuid.UUID
    name: str                   
    sku: str                    
    image_url: str | None = None 
    
    # Precios y cálculos
    unit_price: Decimal         
    quantity: int               
    subtotal: Decimal           # unit_price * quantity

class CartResponse(BaseModel):
    """
    Representa el carrito completo.
    """
    cart_id: str                
    items: list[CartItemResponse] = []
    
    # La suma de todos los subtotales
    total_price: Decimal = Decimal("0.00")